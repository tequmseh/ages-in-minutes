# Бриф реконструкций Aztecs → ../brief.md (формат брифа Mesopotamia). Окна и длины — из ../layout.json.
import json,os,math
E=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L=json.load(open(f'{E}/layout.json'))
W={}
for k,c in L.items():
    for t0,t1,ty,i,d in c['segs']:
        if ty=='CLIP': W.setdefault(i,[]).append((int(k),t0,t1))
TAIL=('All visible surfaces are plain adobe, plaster, packed earth, stone, reed, wood and cotton cloth. Photorealistic documentary still, raw natural colors, true-to-life textures and skin, slight film grain, the look of real footage from a field documentary camera.')
f=lambda x: f'{x:.1f}'.replace('.',',')
R={}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'brief_data.py')).read())
out=['# Бриф реконструкций Aztecs R01–R17\n']
for r in sorted(R):
    d=R[r]; w=W[r]; ln=math.ceil(max(b-a for _,a,b in w)+1)
    ws=' · '.join(f'гл. {g}: {f(a)}–{f(b)} ({f(b-a)} с)' for g,a,b in w)
    out+=[f'### {r}. {d["t"]} — {ln} с','',f'**Окна:** {ws}. Длина файла = самое длинное окно + 1 с.','',
      f'**Проверка эпохи:** {d["era"]}','',f'**Референс:** {d["ref"]}','',
      '**Стартовый кадр (Nano Banana 2, 16:9, 2K):**','','```',d['sf']+' '+TAIL,'```','',
      f'**Движение (Grok Imagine Video, {ln} с):**','','```',f'{d["mv"]} Camera: {d["cam"]} Sound: {d["snd"]}, no music, no speech.','```','',
      f'**Кадр → движение:** {d["lk"]}','']
open(f'{E}/brief.md','w').write('\n'.join(out))
print(len(R),'роликов',sorted(set(W)-set(R)),sorted(set(R)-set(W)))
