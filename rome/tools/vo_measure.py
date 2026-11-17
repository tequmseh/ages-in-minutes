import subprocess,re,glob,json,os,sys
words={}
t=open('/home/claude/ages-in-minutes/rome/script.md').read()
for p in re.split(r'^### ',t,flags=re.M)[1:]:
    title,body=p.split('\n',1)
    n=title.split('.')[0].strip()
    if n=='Outro': n='12o'
    words[n]=len(re.sub(r'\[[^\]]*\]','',body).split())
words['12']+=words.pop('12o')
out=[]
for f in sorted(glob.glob('/mnt/user-data/uploads/*.mp3'),key=lambda x:int(re.search(r'-(\d+)\._',x).group(1))):
    n=re.search(r'-(\d+)\._',f).group(1)
    pr=json.loads(subprocess.run(['ffprobe','-v','quiet','-print_format','json','-show_format','-show_streams',f],capture_output=True,text=True).stdout)
    dur=float(pr['format']['duration']); st=pr['streams'][0]
    log=subprocess.run(['ffmpeg','-hide_banner','-i',f,'-af','silencedetect=n=-32dB:d=0.25','-f','null','-'],capture_output=True,text=True).stderr
    s=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',log)]
    e=[(float(a),float(b)) for a,b in re.findall(r'silence_end: ([\d.]+) \| silence_duration: ([\d.]+)',log)]
    lead= e[0][0] if s and s[0]<0.05 else 0.0
    tail= dur-s[-1] if s and (len(e)<len(s) or e[-1][0]>dur-0.05) else 0.0
    inner=[(round(a-d,2),round(d,2)) for a,d in e if a-d>0.05 and a<dur-0.05]
    longp=[x for x in inner if x[1]>=1.2]
    loud=subprocess.run(['ffmpeg','-hide_banner','-i',f,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
    I=re.findall(r'I:\s+(-?[\d.]+) LUFS',loud)[-1]; P=re.findall(r'Peak:\s+(-?[\d.]+) dBFS',loud)[-1]
    sp=dur-lead-tail
    out.append(dict(ch=int(n),file=os.path.basename(f),dur=round(dur,2),lead=round(lead,2),tail=round(tail,2),pauses=len(inner),long=longp,words=words[n],wpm=round(words[n]/(sp/60),1),I=I,P=P,sr=st['sample_rate'],br=pr['format']['bit_rate'],ch_n=st['channels']))
json.dump(out,open('/home/claude/rome_vo/measure.json','w'),indent=1)
tot=sum(o['dur'] for o in out)
for o in out: print(o['ch'],o['dur'],'lead',o['lead'],'tail',o['tail'],'pauses',o['pauses'],'w',o['words'],'wpm',o['wpm'],o['I'],o['P'],o['sr'],o['br'],o['ch_n'],'LONG',o['long'])
print('VO total',round(tot,2), round(tot/60,2))
print('with 12 cards', round(tot+42,2), 'min', round((tot+42)/60,2))
