# Ручные поправки границ фраз после сверки распознаванием (asr_check.py). Запуск после vo_align.py:
# python3 timing_fix.py timing.json
import json,sys
p=sys.argv[1]; T=json.load(open(p))
FIX={ # глава: {номер фразы: (start, end)} — None оставляет прежнее значение
 '3':{3:(None,9.66),4:(10.23,None)},
 '4':{12:(None,47.01),13:(47.60,49.99),14:(50.49,None)},
 '7':{4:(None,16.72),5:(17.16,None)},
 '10':{20:(None,99.20),21:(99.81,None)},
}
for k,d in FIX.items():
    for r in T[k]['rows']:
        if r['i'] in d:
            s,e=d[r['i']]
            if s is not None: r['start']=s
            if e is not None: r['end']=e
            r['snap']=True
json.dump(T,open(p,'w'),indent=1,ensure_ascii=False)
