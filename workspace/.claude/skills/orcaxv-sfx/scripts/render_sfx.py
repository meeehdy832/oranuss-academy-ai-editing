#!/usr/bin/env python3
"""Mix OrcaXV Essentials 100 sound effects into a video (or audio) file with ffmpeg.

Usage:
  python3 render_sfx.py --video in.mp4 --cues cues.json --library "/path/OrcaXV SFX Pack" --out out.mp4
  python3 render_sfx.py --cues cues.json --library ... --sheet       # print cue sheet only

cues.json = list of cues:
  [{"t": 3.20, "id": "WH-012", "align": "peak", "gain_db": -6, "note": "cut to B-roll"},
   {"t": 7.00, "id": "RS-004", "align": "end"},
   {"t": 9.50, "id": "PO-003"}]

  t        time in the video (seconds, or "mm:ss.xx")
  id       sound id from references/catalog.tsv
  align    "peak" (default): the loudest moment of the sound lands on t  -> whooshes, impacts, risers-with-hit
           "start": the sound starts at t                                -> ambience, clicks, pops
           "end":   the sound ends at t                                  -> pure risers / reverse riser
  gain_db  volume change for this sound (default depends on its level: loud -8, normal -5, quiet -2)
  trim     optional max length in seconds (fade-out 0.15s at the end)
"""
import argparse, csv, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(HERE, 'catalog.tsv')
DEFAULT_GAIN = {'loud': -8.0, 'normal': -5.0, 'quiet': -2.0}


def load_catalog():
    with open(CATALOG, newline='', encoding='utf-8') as f:
        return {r['id']: r for r in csv.DictReader(f, delimiter='\t')}


def to_sec(t):
    if isinstance(t, (int, float)):
        return float(t)
    parts = [float(p) for p in str(t).split(':')]
    s = 0.0
    for p in parts:
        s = s * 60 + p
    return s


def fmt(t):
    m, s = divmod(max(t, 0), 60)
    return f"{int(m):02d}:{s:05.2f}"


def has_audio(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index',
                          '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip()
    return bool(out)


def duration(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
                         capture_output=True, text=True).stdout.strip()
    return float(out or 0)


def plan(cues, cat, library):
    rows = []
    for c in cues:
        s = cat.get(c['id'])
        if not s:
            sys.exit(f"Unknown sound id: {c['id']}")
        t = to_sec(c['t'])
        dur = float(s['dur_s'])
        peak = float(s['peak_s']) if s['peak_s'] not in ('', 'None') else 0.0
        trim = float(c['trim']) if c.get('trim') else None
        eff = min(dur, trim) if trim else dur
        align = c.get('align', 'peak')
        start = t - peak if align == 'peak' else t - eff if align == 'end' else t
        skip = 0.0
        if start < 0:              # sound would start before the video: cut its head
            skip, start = -start, 0.0
        gain = float(c.get('gain_db', DEFAULT_GAIN.get(s['level'], -5.0)))
        rows.append(dict(cue=c, s=s, t=t, start=start, skip=skip, gain=gain, trim=trim,
                         file=os.path.join(library, s['path'])))
    return rows


def sheet(rows):
    print(f"{'TIME':>9}  {'PLACE AT':>9}  {'GAIN':>6}  ID      SOUND  (file)")
    for r in sorted(rows, key=lambda r: r['t']):
        print(f"{fmt(r['t']):>9}  {fmt(r['start']):>9}  {r['gain']:>+5.1f}dB  {r['s']['id']}  "
              f"{r['s']['name']}  ({r['s']['path']})  {r['cue'].get('note', '')}")


def render(video, rows, out, base_gain_db=0.0):
    missing = [r['file'] for r in rows if not os.path.exists(r['file'])]
    if missing:
        sys.exit("Missing sound files:\n" + "\n".join(missing))
    vdur = duration(video)
    args = ['ffmpeg', '-y', '-v', 'error', '-i', video]
    for r in rows:
        args += ['-i', r['file']]
    parts, labels = [], []
    if has_audio(video):
        parts.append(f"[0:a]aresample=48000,aformat=channel_layouts=stereo,volume={base_gain_db}dB[base]")
    else:
        parts.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{vdur}[base]")
    for i, r in enumerate(rows, start=1):
        chain = f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo"
        if r['skip']:
            chain += f",atrim=start={r['skip']:.3f},asetpts=PTS-STARTPTS"
        if r['trim']:
            chain += f",atrim=0:{r['trim']},afade=t=out:st={max(r['trim'] - 0.15, 0):.3f}:d=0.15"
        ms = int(round(r['start'] * 1000))
        chain += f",volume={r['gain']}dB,adelay={ms}|{ms}[s{i}]"
        parts.append(chain)
        labels.append(f"[s{i}]")
    n = len(rows) + 1
    parts.append(f"[base]{''.join(labels)}amix=inputs={n}:duration=first:dropout_transition=0:normalize=0,"
                 f"alimiter=limit=0.95[aout]")
    fc = ';'.join(parts)
    is_audio_only = os.path.splitext(out)[1].lower() in ('.wav', '.mp3', '.m4a', '.aac')
    tail = (['-map', '[aout]'] if is_audio_only else
            ['-map', '0:v?', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest'])
    cmd = args + ['-filter_complex', fc] + tail + [out]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 and 'normalize' in res.stderr:      # very old ffmpeg without amix normalize
        fc = fc.replace(':normalize=0', '')
        cmd = args + ['-filter_complex', fc] + tail + [out]
        res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(res.stderr[-3000:])
    print(f"Rendered {out} with {len(rows)} sound effects.")


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--cues', required=True)
    ap.add_argument('--library', default=os.path.join(os.path.dirname(HERE), 'sounds'))
    ap.add_argument('--video')
    ap.add_argument('--out')
    ap.add_argument('--base-gain-db', type=float, default=0.0, help='volume change for the original audio')
    ap.add_argument('--sheet', action='store_true', help='only print the cue sheet')
    a = ap.parse_args()
    rows = plan(json.load(open(a.cues)), load_catalog(), a.library)
    sheet(rows)
    if not a.sheet:
        if not (a.video and a.out):
            sys.exit('--video and --out are required to render')
        render(a.video, rows, a.out, a.base_gain_db)
