#!/bin/bash
# черновик 1080p: 13 глав в два потока, затем склейка и копия 720p
cd "$(dirname "$0")"; export DRAFT=1
(for n in 0 2 4 6 8 10 12; do python3 build.py $n; done > log_a.txt 2>&1) &
(for n in 1 3 5 7 9 11; do python3 build.py $n; done > log_b.txt 2>&1) &
wait
for n in $(seq -w 0 12); do echo "file 'out_draft/ch$n.mp4'"; done > list_draft.txt
ffmpeg -loglevel error -y -f concat -safe 0 -i list_draft.txt -c copy out_draft/mesopotamia_draft_1080.mp4 && ffmpeg -loglevel error -y -i out_draft/mesopotamia_draft_1080.mp4 -vf scale=1280:720:flags=lanczos -c:v libx264 -crf 25 -preset fast -c:a aac -b:a 128k -movflags +faststart out_draft/mesopotamia_draft_720.mp4
echo done >> log_a.txt
