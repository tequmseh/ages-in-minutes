# Раскладка озвучки по фразам без распознавания речи: паузы (silencedetect -32 dB, 0.25 s) + длина фраз в слогах, DP.
# Запуск: python3 vo_align.py script.md timing.json (файлы озвучки и *.json пауз в /home/claude/vo_rome)
import re,json,sys,subprocess,math
script=open(sys.argv[1]).read()
secs=re.split(r'^### ',script,flags=re.M)[1:]
chap={}
for s in secs:
    title,body=s.split('\n',1)
    m=re.match(r'(\d+)\.',title); key=int(m.group(1)) if m else 'outro'
    chap[key]=re.sub(r'\[[^\]]+\]\s*','',body).strip()
chap[12]=chap[12]+'\n\n'+chap['outro']
def sentences(text):
    out=[]
    for para in text.split('\n\n'):
        out+=[p for p in re.split(r'(?<=[.!?:])\s+(?=[A-Z0-9“"])',para.strip()) if p]
    return out
def syl(s):
    n=0
    for tok in re.findall(r"[A-Za-zÀ-ÿ'-]+|\d[\d,]*",s):
        if tok[0].isdigit():
            d=len(tok.replace(',',''))
            n+= {1:1,2:2,3:4,4:4}.get(d, d+2)
        else:
            n+=max(1,len(re.findall(r'[aeiouy]+',tok.lower().rstrip('e') or tok.lower())))
    return max(1,n)
res={}
for k in range(13):
    ext='mp3'
    f=f'/home/claude/vo_rome/vo{k:02d}.{ext}'
    d=json.load(open(f+'.json'))
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
    pauses=[(a,b) for a,b in d['pauses'] if b-a>=0.25]
    lead=pauses[0][1] if pauses and pauses[0][0]<0.05 else 0.0
    tail=(dur-pauses[-1][0]) if pauses and abs(pauses[-1][1]-dur)<0.06 else 0.0
    inner=[p for p in pauses if p[0]>=0.05 and abs(p[1]-dur)>=0.06]
    S=sentences(chap[k]); w=[syl(s) for s in S]; n=len(S)
    # nodes: 0=start, 1..m=pauses, m+1=end
    nodes=[(lead,lead)]+inner+[(dur-tail,dur-tail)]; M=len(nodes)
    speech=(dur-tail-lead)-sum(b-a for a,b in inner)
    # iterate rate estimate
    rate=speech/sum(w)
    for it in range(3):
        INF=1e18
        dp=[[INF]*M for _ in range(n+1)]; bk=[[None]*M for _ in range(n+1)]
        dp[0][0]=0
        for i in range(n):           # sentences consumed so far
            for j in range(M):
                if dp[i][j]>=INF: continue
                for g in (1,2,3):    # group of g sentences between two nodes
                    if i+g>n: break
                    pred=sum(w[i:i+g])*rate + 0.25*(g-1)
                    for jj in range(j+1,M):
                        if (i+g==n)!=(jj==M-1): 
                            if jj==M-1: continue
                        span_speech=nodes[jj][0]-nodes[j][1]-sum(b-a for a,b in nodes[j+1:jj])
                        if span_speech>pred*2.2+2: break
                        c=((span_speech-pred)**2)/(pred+0.5)+0.6*(g-1)+0.05*(jj-j-1)
                        if dp[i][j]+c<dp[i+g][jj]:
                            dp[i+g][jj]=dp[i][j]+c; bk[i+g][jj]=(i,j,g)
        # backtrack
        segs=[]; i,j=n,M-1
        while i>0:
            pi,pj,g=bk[i][j]; segs.append((pi,g,pj,j)); i,j=pi,pj
        segs.reverse()
        # refine rate: total speech / syllables (unchanged), keep
    rows=[]
    for pi,g,pj,jj in segs:
        st=nodes[pj][1]; en=nodes[jj][0]
        tw=sum(w[pi:pi+g]); t=st
        for q in range(g):
            e=en if q==g-1 else t+(en-st)*w[pi+q]/tw
            rows.append({'i':pi+q+1,'start':round(t,2),'end':round(e,2),'snap':q==g-1,'text':S[pi+q]})
            t=e
    res[k]={'dur':round(dur,3),'lead':round(lead,2),'tail':round(tail,2),'words':len(chap[k].split()),'rows':rows,
            'cost':round(dp[n][M-1],2)}
json.dump(res,open(sys.argv[2],'w'),indent=1,ensure_ascii=False)
for k,v in res.items(): print(k,v['dur'],'cost',v['cost'],'est',sum(1 for r in v['rows'] if not r['snap']))
