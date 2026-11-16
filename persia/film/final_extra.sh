#!/bin/bash
# cold open (ch00) and the 15 s tail (ch13) at master settings; usage: final_extra.sh 00|13
cd "$(dirname "$0")"; mkdir -p out
ENC="-c:v libx264 -crf 14 -preset ${PRESET:-medium} -profile:v high -bf 2 -g 60 -r 60 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart"
M=../music/coldopen_weight_of_silence.wav
if [ "$1" = 00 ]; then
  VO=vo/00.mp3
  J=$(ffmpeg -hide_banner -i $VO -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | python3 -c "
import sys,json;e=sys.stdin.read();m=json.loads(e[e.rindex('{'):e.rindex('}')+1]);print(f\"measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}\")")
  ffmpeg -v error -y -i ../coldopen/gfx.mp4 -i $VO -i $M -i $M -filter_complex "[0:v]scale=2560:1440:flags=lanczos,setsar=1,format=yuv420p[v];[1:a]loudnorm=I=-14:TP=-1.5:LRA=11:$J:linear=true,aresample=48000[vo];[2:a]atrim=0:59.0,asetpts=PTS-STARTPTS[m1];[3:a]atrim=63.95:75,asetpts=PTS-STARTPTS[m2];[m1][m2]acrossfade=d=0.12:c1=tri:c2=tri,aresample=48000,volume=-13dB,adelay=200:all=1,afade=t=in:d=0.4,afade=t=out:st=65.4:d=1.6[mu];[vo][mu]amix=inputs=2:normalize=0:duration=longest,volume=-0.4dB,alimiter=limit=0.84,aformat=channel_layouts=stereo[a]" -map "[v]" -map "[a]" $ENC -t 67.0 out/ch00.tmp.mp4 && mv out/ch00.tmp.mp4 out/ch00.mp4
else
  ffmpeg -v error -y -loop 1 -framerate 60 -t 15 -i tail.png -ss 76.6 -t 15 -i $M -filter_complex "[0:v]fade=t=in:st=0:d=0.8,fade=t=out:st=14:d=1,scale=2560:1440:flags=lanczos,setsar=1,format=yuv420p[v];[1:a]aresample=48000,volume=-13dB,afade=t=in:d=1.5,afade=t=out:st=12.5:d=2.5,aformat=channel_layouts=stereo[a]" -map "[v]" -map "[a]" $ENC -t 15.0 out/ch13.tmp.mp4 && mv out/ch13.tmp.mp4 out/ch13.mp4
fi
