#!/bin/bash
cd "$(dirname "$0")"; unset DRAFT
(for n in 2 10 6; do python3 build.py $n; done > flog_c.txt 2>&1; echo done >> flog_c.txt) &
(while pgrep -f "build.py 12" > /dev/null; do sleep 5; done; for n in 8 4; do python3 build.py $n; done > flog_d.txt 2>&1; echo done >> flog_d.txt) &
wait
