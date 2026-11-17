#!/bin/bash
# cold open (ch00) at master settings: graphics from ../coldopen/gfx.mp4 + voice + music. usage: final_extra.sh  (DRAFT=1 for 1080p fast)
cd "$(dirname "$0")"; OD=out; SZ=2560:1440; CRF=14; PR=${PRESET:-medium}
if [ -n "$DRAFT" ]; then OD=out_draft; SZ=1920:1080; CRF=21; PR=veryfast; fi
mkdir -p $OD
ENC="-c:v libx264 -crf $CRF -preset $PR -profile:v high -bf 2 -g 60 -r 60 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart"
M=../music/coldopen_the_raid_begins.wav; VO=../vo/vo00.mp3; D=52.0
J=$(ffmpeg -hide_banner -i $VO -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | python3 -c "
import sys,json;e=sys.stdin.read();m=json.loads(e[e.rindex('{'):e.rindex('}')+1]);print(f\"measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}\")")
# music: 49.0 s track stretched 4 % (limit 6 %) to carry the title; about 14 dB under the voice
ffmpeg -v error -y -i ../coldopen/gfx.mp4 -i $VO -i $M -filter_complex "[0:v]scale=$SZ:flags=lanczos,setsar=1,format=yuv420p[v];[1:a]loudnorm=I=-14:TP=-1.5:LRA=11:$J:linear=true,aresample=48000[vo];[2:a]aresample=48000,atempo=0.96,volume=${MUS:--11.5}dB,afade=t=in:d=0.3,afade=t=out:st=49.6:d=2.2[mu];[vo][mu]amix=inputs=2:normalize=0:duration=longest,volume=-0.4dB,alimiter=limit=0.84,aformat=channel_layouts=stereo[a]" -map "[v]" -map "[a]" $ENC -t $D $OD/ch00.tmp.mp4 && mv $OD/ch00.tmp.mp4 $OD/ch00.mp4
