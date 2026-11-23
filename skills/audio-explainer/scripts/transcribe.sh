#!/bin/bash
# Usage: transcribe.sh AUDIO_OR_VIDEO WORKDIR [lang=ar]
# Word-timed transcript in ~2 min for 16 min of audio (whisper large-v3-turbo on the Mac GPU; -mc 0 stops repeat loops).
# Writes WORKDIR/voice.wav (48k stereo, for the mix), words_clean.json, transcript_20s.txt. Prints only a summary.
set -e
IN="$1"; W="$2"; LANG_="${3:-ar}"
MODEL="${WHISPER_MODEL:-/Users/Apple/Downloads/editing-ai/project/models/ggml-large-v3-turbo.bin}"
mkdir -p "$W"
ffmpeg -v error -y -i "$IN" -vn -ac 1 -ar 16000 "$W/voice16k.wav"
ffmpeg -v error -y -i "$IN" -vn -ac 2 -ar 48000 "$W/voice.wav"
whisper-cli -m "$MODEL" -f "$W/voice16k.wav" -l "$LANG_" -mc 0 -ml 1 -sow -oj -of "$W/words" -np > "$W/whisper.log" 2>&1
python3 - "$W" <<'EOF'
import json, sys, collections
W = sys.argv[1]
d = json.load(open(f"{W}/words.json"))
w = [{"start": s["offsets"]["from"] / 1000, "end": s["offsets"]["to"] / 1000, "text": s["text"].strip()} for s in d["transcription"] if s["text"].strip()]
json.dump(w, open(f"{W}/words_clean.json", "w"), ensure_ascii=False)
blocks = collections.OrderedDict()
for x in w: blocks.setdefault(int(x["start"] // 20) * 20, []).append(x["text"])
open(f"{W}/transcript_20s.txt", "w").write("\n".join(f"{k:>4}s {' '.join(v)}" for k, v in blocks.items()))
g = collections.Counter(tuple(x["text"] for x in w[i:i + 4]) for i in range(len(w) - 4)).most_common(1)
loop = g and g[0][1] > 6
print(f"{len(w)} words, {w[-1]['end']:.1f}s · transcript: {W}/transcript_20s.txt" + ("  ⚠ possible repeat loop: " + " ".join(g[0][0]) if loop else ""))
EOF
