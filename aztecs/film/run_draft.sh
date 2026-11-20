#!/bin/bash
# черновик 1080p: главы в два потока (список глав аргументами, по умолчанию все 13), затем склейка и копия 720p
cd "$(dirname "$0")"; export DRAFT=1; L=(${@:-0 1 2 3 4 5 6 7 8 9 10 11 12}); A=(); B=()
for i in "${!L[@]}"; do if (( i % 2 )); then B+=(${L[$i]}); else A+=(${L[$i]}); fi; done
(for n in "${A[@]}"; do python3 build.py $n; done > log_a.txt 2>&1) &
(for n in "${B[@]}"; do python3 build.py $n; done > log_b.txt 2>&1) &
wait
for n in $(seq -w 0 12); do [ -f out_draft/ch$n.mp4 ] && echo "file 'out_draft/ch$n.mp4'"; done > list_draft.txt
ffmpeg -loglevel error -y -f concat -safe 0 -i list_draft.txt -c copy out_draft/aztecs_draft_1080.mp4 && ffmpeg -loglevel error -y -i out_draft/aztecs_draft_1080.mp4 -vf scale=1280:720:flags=lanczos -c:v libx264 -crf 25 -preset fast -c:a aac -b:a 128k -movflags +faststart out_draft/aztecs_draft_720.mp4
echo done >> log_a.txt
