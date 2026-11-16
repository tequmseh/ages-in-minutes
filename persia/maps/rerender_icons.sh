#!/bin/bash
# re-render the scenes touched by the province-line fix and the city icons, then rebuild the draft
cd "$(dirname "$0")"
python3 pe_scenes.py render 07a_ionian_revolt 08a_marathon 09c_from_susa 04a_satrapies > log_r1.txt 2>&1 &
python3 pe_scenes.py render 06a_persepolis 09a_salamis 12b_the_answer 07b_mardonius 10c_kings_peace 11b_persepolis_burns 06b_materials 08c_the_army 02c_going_home 04b_kings_eyes 04c_languages 01c_twenty_years 11c_keeps 09b_plataea 05a_the_road 10a_persian_gold > log_r2.txt 2>&1 &
wait
cd ../film && ./run_draft.sh
for i in 01 02 03 04 05 06 07 08 09 10 11 12; do echo "file 'out_draft/ch$i.mp4'"; done > list_draft.txt
ffmpeg -loglevel error -y -f concat -safe 0 -i list_draft.txt -c copy -movflags +faststart /tmp/claude-0/-home-claude/6766839a-4a89-5481-9872-a3381d71ea5c/scratchpad/persia_draft2_ch1-12.mp4
echo ALLDONE
