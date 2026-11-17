#!/bin/bash
# master of all chapters and the cold open: 2560x1440, crf 14, two queues
cd "$(dirname "$0")"
(bash final_extra.sh; for c in 1 3 5 7 9 11; do python3 build.py $c; done) > log_fa.txt 2>&1 &
(for c in 2 4 6 8 10 12; do python3 build.py $c; done) > log_fb.txt 2>&1 &
wait
