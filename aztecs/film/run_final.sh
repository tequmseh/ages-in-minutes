#!/bin/bash
# мастер 2560x1440, 60 fps: 13 глав в два потока, затем склейка без перекодирования
cd "$(dirname "$0")"; unset DRAFT
(for n in 0 2 4 6 8 10 12; do python3 build.py $n; done > flog_a.txt 2>&1) &
(for n in 1 3 5 7 9 11; do python3 build.py $n; done > flog_b.txt 2>&1) &
wait
for n in $(seq -w 0 12); do echo "file 'out/ch$n.mp4'"; done > list_final.txt
ffmpeg -loglevel error -y -f concat -safe 0 -i list_final.txt -c copy -movflags +faststart out/aztecs_master.mp4
echo done >> flog_a.txt
