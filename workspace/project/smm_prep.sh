#!/bin/zsh
# Developed by Mehdi ORANUSS | Powered by Claude
# SMM series prep: download voice NN, cut its script from SCRIPTS.md, whisper large-v3 word timings, align to script.
# usage: zsh project/smm_prep.sh  (reads project/work/smm/voice_urls.txt)
TOP=/Users/Apple/Downloads/editing-ai
while read NN URL; do
  D=$TOP/output/smm-10-scripts/$NN; mkdir -p $D
  [ -f $D/voice.mp3 ] || curl -sS -o $D/voice.mp3 "$URL"
  cp -n $TOP/output/smm-10-scripts/01/music.mp3 $D/music.mp3
  N=$((10#$NN))
  python3 - "$TOP/output/smm-10-scripts/SCRIPTS.md" "$N" "$D/script.txt" <<'PY'
import sys
t=open(sys.argv[1],encoding='utf-8').read(); n=sys.argv[2]
s=t.split(f'\n## {n}. ')[1].split('**Script:**')[1].split('**Visuals:**')[0].strip()
open(sys.argv[3],'w',encoding='utf-8').write(s)
PY
  ffmpeg -hide_banner -loglevel error -y -i $D/voice.mp3 -ar 16000 -ac 1 $D/voice16k.wav
  whisper-cli -m $TOP/project/models/ggml-large-v3.bin -l ar -f $D/voice16k.wav -ojf -of $D/whisper -ml 1 -sow > $D/whisper.log 2>&1
  python3 -c "
import json;d=json.load(open('$D/whisper.json'))
w=[(round(s['offsets']['from']/1000,2),s['text'].strip()) for s in d['transcription'] if s['text'].strip()]
json.dump(w,open('$D/words.json','w'),ensure_ascii=False)"
  echo -n "$NN "; python3 -I $TOP/project/smm_align.py $D $D/script.txt
done < $TOP/project/work/smm/voice_urls.txt
