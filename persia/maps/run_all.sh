#!/bin/bash
cd "$(dirname "$0")"; mkdir -p out_look
A=$(python3 pe_scenes.py list | awk 'NR%2==1 && $1!="total"{print $1}')
B=$(python3 pe_scenes.py list | awk 'NR%2==0 && $1!="total"{print $1}')
python3 pe_scenes.py render $A > log1.txt 2>&1 &
python3 pe_scenes.py render $B > log2.txt 2>&1 &
wait
