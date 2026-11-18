# Замер озвучки: длительность, паузы (silencedetect -32 dB, 0.25 s), темп, громкость.
# Копирует файлы в /home/claude/vo_meso/voNN.mp3 и пишет рядом voNN.mp3.json с паузами (для vo_align.py).
# Запуск: python3 vo_measure.py <папка с mp3> <script.md> <vo_measure.json>
import subprocess,re,glob,json,os,sys,shutil
src,script,outp=sys.argv[1:4]
D='/home/claude/vo_meso'; os.makedirs(D,exist_ok=True)
words={}
t=open(script).read()
for p in re.split(r'^### ',t,flags=re.M)[1:]:
    title,body=p.split('\n',1)
    n=title.split('.')[0].strip()
    if n=='Outro': n='12o'
    words[n]=len(re.sub(r'\[[^\]]*\]','',body).split())
words['12']+=words.pop('12o')
out=[]
for f0 in sorted(glob.glob(src+'/*.mp3'),key=lambda x:int(re.search(r'-(\d+)\._',x).group(1))):
    n=re.search(r'-(\d+)\._',f0).group(1)
    f=f'{D}/vo{int(n):02d}.mp3'; shutil.copy(f0,f)
    pr=json.loads(subprocess.run(['ffprobe','-v','quiet','-print_format','json','-show_format','-show_streams',f],capture_output=True,text=True).stdout)
    dur=float(pr['format']['duration']); st=pr['streams'][0]
    log=subprocess.run(['ffmpeg','-hide_banner','-i',f,'-af','silencedetect=n=-32dB:d=0.25','-f','null','-'],capture_output=True,text=True).stderr
    s=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',log)]
    e=[float(a) for a in re.findall(r'silence_end: ([\d.]+)',log)]
    pauses=[[s[i], e[i] if i<len(e) else dur] for i in range(len(s))]
    pauses=[[max(0,a),b] for a,b in pauses]
    json.dump({'pauses':pauses},open(f+'.json','w'))
    lead=pauses[0][1] if pauses and pauses[0][0]<0.05 else 0.0
    tail=dur-pauses[-1][0] if pauses and abs(pauses[-1][1]-dur)<0.06 else 0.0
    inner=[(round(a,2),round(b-a,2)) for a,b in pauses if a>=0.05 and abs(b-dur)>=0.06]
    longp=[x for x in inner if x[1]>=1.2]
    loud=subprocess.run(['ffmpeg','-hide_banner','-i',f,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
    I=re.findall(r'I:\s+(-?[\d.]+) LUFS',loud)[-1]; P=re.findall(r'Peak:\s+(-?[\d.]+) dBFS',loud)[-1]
    sp=dur-lead-tail
    out.append(dict(ch=int(n),file=os.path.basename(f0),dur=round(dur,2),lead=round(lead,2),tail=round(tail,2),pauses=len(inner),long=longp,words=words[n],wpm=round(words[n]/(sp/60),1),I=I,P=P,sr=st['sample_rate'],br=pr['format']['bit_rate'],ch_n=st['channels']))
json.dump(out,open(outp,'w'),indent=1)
tot=sum(o['dur'] for o in out)
for o in out: print(o['ch'],o['dur'],'lead',o['lead'],'tail',o['tail'],'pauses',o['pauses'],'w',o['words'],'wpm',o['wpm'],o['I'],o['P'],o['sr'],o['ch_n'],'LONG',o['long'])
print('VO total',round(tot,2),'=',int(tot//60),'min',round(tot%60,1),'s; words',sum(o['words'] for o in out),'wpm',round(sum(o['words'] for o in out)/tot*60,1))
print('with 12 cards 42 s:',round(tot+42,1),'; +tail 10 s:',round(tot+52,1))
