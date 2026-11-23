#!/usr/bin/env python3
"""Word-level transcript (ms timings) with faster-whisper.

Usage:
  pip install faster-whisper
  python3 transcribe.py input.mp4 out.json [--model small|medium|large-v3] [--lang ar|fr|en]
Writes out.json: {"language":..,"words":[{"w":"..","s":1.23,"e":1.50}],"segments":[..]}
and out.txt with "[s-e] text" lines.
Darija: use --lang ar with medium or large-v3 for best results; review the text by hand.
"""
import argparse, json, os, sys

ap = argparse.ArgumentParser()
ap.add_argument("input"); ap.add_argument("out")
ap.add_argument("--model", default="medium"); ap.add_argument("--lang", default=None)
a = ap.parse_args()
try:
    from faster_whisper import WhisperModel
except ImportError:
    sys.exit("pip install faster-whisper (needs the model download from huggingface.co on first run)")

m = WhisperModel(a.model, device="auto", compute_type="int8")
segs, info = m.transcribe(a.input, language=a.lang, word_timestamps=True, vad_filter=True)
words, segments = [], []
for s in segs:
    segments.append({"s": round(s.start, 3), "e": round(s.end, 3), "text": s.text.strip()})
    for w in (s.words or []):
        words.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)})
json.dump({"language": info.language, "words": words, "segments": segments}, open(a.out, "w"), ensure_ascii=False, indent=1)
with open(os.path.splitext(a.out)[0] + ".txt", "w") as f:
    for s in segments:
        f.write(f"[{s['s']:.2f}-{s['e']:.2f}] {s['text']}\n")
print(f"{len(words)} words, language={info.language}")
