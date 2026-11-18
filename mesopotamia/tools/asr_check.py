import json,re,subprocess,sys,numpy as np,soundfile as sf,sherpa_onnx,difflib
M='sherpa-onnx-whisper-base.en'
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f'{M}/base.en-encoder.int8.onnx',decoder=f'{M}/base.en-decoder.int8.onnx',tokens=f'{M}/base.en-tokens.txt',num_threads=2)
T=json.load(open('/home/claude/ages-in-minutes/mesopotamia/timing.json'))
norm=lambda s: re.findall(r"[a-z0-9']+",s.lower().replace('-',' ').replace(',',''))
bad=[];out={}
for k in sorted(T,key=int):
    wav=f'/tmp/vo{k}.wav'
    subprocess.run(['ffmpeg','-y','-v','error','-i',f'/home/claude/vo_meso/vo{int(k):02d}.mp3','-ar','16000','-ac','1',wav])
    a,sr=sf.read(wav,dtype='float32')
    for r in T[k]['rows']:
        s=max(0,r['start']-0.2); e=r['end']+0.2
        seg=a[int(s*sr):int(e*sr)]
        st=rec.create_stream(); st.accept_waveform(sr,seg); rec.decode_stream(st)
        hyp=st.result.text.strip()
        ratio=difflib.SequenceMatcher(None,norm(r['text']),norm(hyp)).ratio()
        out.setdefault(k,[]).append((r['i'],round(ratio,2),hyp))
        if ratio<0.75: bad.append((k,r['i'],round(ratio,2),r['start'],r['end'],r['text'],hyp))
json.dump(out,open('asr_rows.json','w'),ensure_ascii=False,indent=0)
print('rows',sum(len(v) for v in out.values()),'bad',len(bad))
for b in bad: print(b)
