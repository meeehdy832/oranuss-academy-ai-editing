#!/bin/bash
# Usage: stills.sh REMOTION_DIR OUT.jpg SEC1 SEC2 ... (max 8)
# Renders frames of the real composition at those seconds and tiles them into ONE half-size board
# (one image to look at instead of eight → far fewer tokens).
set -e
R="$1"; OUT="$2"; shift 2
T=$(mktemp -d); i=0
cd "$R"
for s in "$@"; do f=$(python3 -c "print(int(float('$s')*30))"); npx remotion still src/index.ts Explainer "$T/$i.png" --frame=$f --log=error >/dev/null; i=$((i+1)); done
n=$i; cols=2; [ $n -le 1 ] && cols=1
inputs=""; for j in $(seq 0 $((n-1))); do inputs="$inputs -i $T/$j.png"; done
if [ $n -eq 1 ]; then ffmpeg -v error -y -i "$T/0.png" -vf scale=960:-2 -q:v 4 "$OUT"; else
layout=$(python3 -c "
n=$n;c=2;print('|'.join(f'{(\"w0\" if i%c else \"0\")}_{\"+\".join([\"h0\"]*(i//c)) or \"0\"}' for i in range(n)))")
ffmpeg -v error -y $inputs -filter_complex "xstack=inputs=$n:layout=$layout:fill=black,scale=1600:-2" -q:v 4 "$OUT"; fi
rm -rf "$T"; echo "board: $OUT"
