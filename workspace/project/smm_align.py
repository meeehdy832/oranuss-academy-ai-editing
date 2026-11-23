# Developed by Mehdi ORANUSS | Powered by Claude
"""Align known script words to whisper word timings (difflib on normalized tokens). usage: python3 -I smm_align.py <dir> <script.txt>
Writes <dir>/words_aligned.json: [[start, end, word], ...] using the SCRIPT spelling."""
import json, sys, re, difflib, os
d, sp = sys.argv[1], sys.argv[2]
W = json.load(open(os.path.join(d, "words.json")))
S = open(sp, encoding="utf-8").read().split()
norm = lambda s: re.sub(r"[^\w]", "", s.lower().replace("ـ", ""))
a, b = [norm(x) for _, x in W], [norm(x) for x in S]
m = difflib.SequenceMatcher(None, a, b, autojunk=False)
t = [None] * len(S)
for tag, i1, i2, j1, j2 in m.get_opcodes():
    if tag == "equal" or (i2 - i1) == (j2 - j1):
        for k in range(j2 - j1): t[j1 + k] = W[i1 + k][0]
    elif i2 > i1:
        for k in range(j2 - j1): t[j1 + k] = W[i1][0] + (W[i2 - 1][0] - W[i1][0]) * k / max(1, j2 - j1)
for k in range(len(t)):                      # fill gaps
    if t[k] is None: t[k] = t[k - 1] + 0.2 if k else 0.0
out = [[round(t[k], 2), round(t[k + 1] if k + 1 < len(t) else t[k] + 0.4, 2), S[k]] for k in range(len(S))]
json.dump(out, open(os.path.join(d, "words_aligned.json"), "w"), ensure_ascii=False)
print(len(S), "words;", len(W), "whisper")
