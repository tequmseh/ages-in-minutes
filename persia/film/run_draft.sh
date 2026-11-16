#!/bin/bash
# draft of all chapters: 1080p, fast encode, missing clips marked
cd "$(dirname "$0")"
(for c in 1 3 5 7 9 11; do DRAFT=1 python3 build.py $c; done) > log_a.txt 2>&1 &
(for c in 2 4 6 8 10 12; do DRAFT=1 python3 build.py $c; done) > log_b.txt 2>&1 &
wait
