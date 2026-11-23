#!/usr/bin/env python3
"""Remove silences from a clip.

Two modes:
  --transcript words.json   keep only speech spans from the word timings (best; gaps > --gap are cut)
  (no transcript)           use ffmpeg silencedetect on the audio
Optional --drop "s-e,s-e" to remove extra ranges (false starts, filler) in source seconds.

Usage:
  python3 cut_silences.py in.mp4 out.mp4 [--transcript t.json] [--gap 0.35] [--pad 0.10]
       [--noise -35dB] [--drop 12.4-13.1] [--segments seg.json]
Writes the kept segments (source times) to --segments so captions can be remapped.
"""
import argparse, json, re, subprocess


def probe_dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", p]).decode().strip())


def speech_from_silencedetect(p, noise, mind):
    out = subprocess.run(["ffmpeg", "-i", p, "-af", f"silencedetect=noise={noise}:d={mind}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    dur = probe_dur(p)
    sil = list(zip(starts, ends + [dur] * (len(starts) - len(ends))))
    keep, cur = [], 0.0
    for s, e in sil:
        if s > cur:
            keep.append([cur, s])
        cur = e
    if cur < dur:
        keep.append([cur, dur])
    return keep, dur


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input"); ap.add_argument("output")
    ap.add_argument("--transcript"); ap.add_argument("--gap", type=float, default=0.35)
    ap.add_argument("--pad", type=float, default=0.10); ap.add_argument("--noise", default="-35dB")
    ap.add_argument("--drop", default=""); ap.add_argument("--segments")
    a = ap.parse_args()
    dur = probe_dur(a.input)
    if a.transcript:
        words = json.load(open(a.transcript))["words"]
        keep = []
        for w in words:
            if keep and w["s"] - keep[-1][1] <= a.gap:
                keep[-1][1] = w["e"]
            else:
                keep.append([w["s"], w["e"]])
    else:
        keep, dur = speech_from_silencedetect(a.input, a.noise, a.gap)
    keep = [[max(0, s - a.pad), min(dur, e + a.pad)] for s, e in keep]
    for r in filter(None, a.drop.split(",")):
        ds, de = map(float, r.split("-"))
        nk = []
        for s, e in keep:
            if e <= ds or s >= de:
                nk.append([s, e])
            else:
                if s < ds: nk.append([s, ds])
                if e > de: nk.append([de, e])
        keep = nk
    merged = []
    for s, e in sorted(keep):
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        elif e - s > 0.08:
            merged.append([s, e])
    parts, labels = [], []
    for i, (s, e) in enumerate(merged):
        parts.append(f"[0:v]trim={s:.3f}:{e:.3f},setpts=PTS-STARTPTS[v{i}];"
                     f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,"
                     f"afade=t=out:st={max(0, e - s - 0.01):.3f}:d=0.01[a{i}];")
        labels.append(f"[v{i}][a{i}]")
    fc = "".join(parts) + "".join(labels) + f"concat=n={len(merged)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.input, "-filter_complex", fc,
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
                    "-c:a", "aac", "-b:a", "192k", a.output], check=True)
    new = sum(e - s for s, e in merged)
    if a.segments:
        json.dump(merged, open(a.segments, "w"))
    print(json.dumps({"segments": len(merged), "source_s": round(dur, 2), "output_s": round(new, 2)}))


if __name__ == "__main__":
    main()
