#!/bin/bash
cd "$(dirname "$0")"; unset DRAFT
(for n in 0 1 3 5 7 9; do python3 build.py $n; done > flog_a.txt 2>&1; echo done >> flog_a.txt) &
(while ! grep -q done /tmp/rb.log; do sleep 10; done; for n in 11 12 10 8 6 4; do python3 build.py $n; done > flog_b.txt 2>&1; echo done >> flog_b.txt) &
wait
