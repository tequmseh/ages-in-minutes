# Раскладка глав Aztecs — единственный источник чисел для layout.json, брифа и списка вставок.
# Граница отрезка: i — начало фразы i (середина паузы перед ней); (i,'..') — внутри фразы i перед словами '..'.
# Типы: MAP карта, CLIP ролик, INS вставка, PLATE плашка, CARD карточка.
# Запуск: python3 layout_src.py → ../layout.json + сводка.
import json,os,math
H=os.path.dirname(os.path.abspath(__file__)); E=os.path.dirname(H)
T=json.load(open(f'{E}/timing.json'))
L={}
L[0]=[(1,'CLIP','R01','Солдаты идут по дамбе через озеро. NOVEMBER 1519'),
(3,'CLIP','R02','Город на острове издали, храмы. TENOCHTITLAN'),
(5,'CLIP','R03','Каналы, каноэ. 200,000 PEOPLE · 4× LONDON'),
(7,'CLIP','R04','Кочевники у берега озера. WANDERERS NOBODY WANTED'),
(9,'CLIP','R05','Огороды на воде. FARMS BUILT ON WATER'),
((9,'money'),'CLIP','R06','Какао-бобы в ладонях. MONEY THAT GROWS ON TREES'),
((9,'a school'),'INS','V15','Кодекс Мендоса, воспитание. A SCHOOL FOR EVERY CHILD'),
((9,'a calendar'),'INS','V01','Камень Солнца. EVERY 52 YEARS'),
((9,'and a conquest'),'CLIP','R15','Корабли у побережья. NOT WON BY 500 SPANIARDS'),
(10,'CLIP','R02','Город на острове. THE AZTECS · IT TAKES TWENTY MINUTES')]
L[1]=[(1,'MAP','01a','Север: Астлан без точки. MESHEEKA · AZTLAN'),
(7,'INS','V02','Портрет Гумбольдта. 19TH CENTURY · HUMBOLDT'),
(9,'MAP','01b','Путь на юг в долину Мехико. HUITZILOPOCHTLI · 200 YEARS'),
(10,'INS','V03','Кодекс Бодурини, страница с жрецами. PRIESTS'),
(12,'MAP','01c','Долина Мехико: пять озёр. 2,200 M · LAKE TEXCOCO'),
(17,'MAP','01d','Кульуакан, Аскапоцалько, Тескоко. AROUND 1250')]
L[2]=[(1,'MAP','01d','Кочевания вокруг озера'),
(3,'CLIP','R08','Орёл на кактусе. EAGLE · PRICKLY PEAR'),
(5,'MAP','02a','Остров. 1325 · TENOCHTITLAN'),
(7,'INS','V04','Флаг Мексики. THE MEXICAN FLAG'),
(10,'INS','V05','Кодекс Мендоса, орёл без змеи. CODEX MENDOZA · 1541'),
(11,'INS','V06','Рисунок Дурана. DIEGO DURAN · 1581'),
(12,'CLIP','R09','Грязь и тростник. MUD AND REEDS'),
(15,'MAP','02a','Три преимущества острова'),
(19,'MAP','02b','Тлателолко на севере острова. TLATELOLCO'),
(22,'INS','V07','Акамапичтли, Кодекс Мендоса. 1375 · TLATOANI'),
(24,'MAP','02a','Дань Аскапоцалько. AZCAPOTZALCO')]
L[3]=[(1,'CLIP','R10','Колья и плетёные ветки в мелководье. CHINAMPA'),
(4,'INS','V08','Чинампы Сочимилько. CHINAMPAS'),
(7,'CLIP','R11','Каналы между чинампами, каноэ. CANALS'),
(9,'MAP','03a','Акведук из Чапультепека. CHAPULTEPEC · TWO CHANNELS'),
(12,'MAP','03a','Три дамбы: север, запад, юг. THREE CAUSEWAYS'),
(15,'MAP','03b','Дамба Несауалькойотля. 1449 · 16 KM'),
(22,'MAP','03b','Озеро больше не затапливает')]
L[4]=[(1,'MAP','04a','Аскапоцалько, 1427. TEZOZOMOC · MAXTLA'),
(6,'INS','V09','Ицкоатль, Кодекс Мендоса. ITZCOATL'),
(7,'MAP','04b','Тройственный союз. 1428 · TLACOPAN'),
(14,'PLATE','p4a','2/5 TENOCHTITLAN · 2/5 TEXCOCO · 1/5 TLACOPAN'),
(16,'INS','V10','Тлакаэлель. TLACAELEL'),
(19,'PLATE','p4b','THE WINNERS EDIT THE PAST · A CHOSEN PEOPLE')]
L[5]=[(1,'MAP','05a','Первый Моктесума, походы на восток и юг. 1440'),
(7,'MAP','05b','Держава до Соконуско. 1502 · AHUITZOTL'),
(14,'INS','V11','Кодекс Мендоса, лист дани. 38 PROVINCES'),
(17,'INS','V12','Перья, нефрит, бирюза. FEATHERS · JADE · TURQUOISE'),
(19,'PLATE','p5a','PAY · OR THE ARMY COMES BACK'),
(22,'MAP','05b','Мятежи'),
(24,'MAP','05c','Тарраски и Тласкала. TARASCANS · TLAXCALA')]
L[6]=[(1,'CLIP','R17','Идём по дамбе в город. 1519'),
(3,'MAP','06a','План Теночтитлана. 200,000'),
(6,'INS','V13','Модель Великого храма. THE GREAT TEMPLE'),
(9,'INS','V25','Слои храма. REBUILT SIX TIMES'),
(11,'MAP','06b','Рынок Тлателолко. TLATELOLCO'),
(14,'CLIP','R12','Рынок: товары, торговцы. 60,000?'),
(17,'INS','V14','Какао-бобы. 1 BEAN · 1 TOMATO'),
(22,'PLATE','p6a','1 → TOMATO · 3 → TURKEY EGG · 100 → TURKEY HEN')]
L[7]=[(1,'INS','V15','Кодекс Мендоса, воспитание, лист 1. CALMECAC'),
(5,'INS','V24','Кодекс Мендоса, воспитание, лист 2. TELPOCHCALLI'),
(11,'INS','V16','Кодекс Мендоса, первый пленник. FIRST CAPTIVE'),
(17,'INS','V17','Воин-орёл из Храма. EAGLE WARRIORS'),
(20,'CLIP','R07','Семья за столом. TOMATOES · CHILI · AVOCADO'),
(22,'PLATE','p7a','TOMATL · CHILLI · AHUACATL · CHOCOLATL · COYOTL')]
L[8]=[(1,'PLATE','p8a','THE DEBT TO THE GODS · 80,400 → THOUSANDS'),
(14,'MAP','08a','Великий храм, 2015. 600+'),
(17,'INS','V01','Камень Солнца. 365 · 260 · 52'),
(21,'CLIP','R13','Новый огонь на горе ночью. NEW FIRE · 1507')]
L[9]=[(1,'MAP','09a','Тласкала. FLOWER WAR'),
(3,'CLIP','R14','Воины в краске и перьях у поля. FLOWER WAR'),
(7,'MAP','09a','Войны цветов при Моктесуме I'),
(11,'MAP','09b','Враги вокруг империи'),
(15,'INS','V18','Моктесума II, Кодекс Мендоса. 1502'),
(18,'MAP','09b','Сильнейшая держава'),
(19,'CLIP','R15','Корабли у побережья. GULF COAST')]
L[10]=[(1,'INS','V19','Портрет Кортеса. HERNAN CORTES'),
(2,'MAP','10a','Куба → побережье. FEBRUARY 1519'),
(4,'INS','V20','Малинце, Ленсо де Тласкала. MALINTZIN'),
(10,'PLATE','p10b','SPANISH → MAYA → NAHUATL'),
(14,'MAP','10b','Побережье → Тласкала → Теночтитлан. AUGUST · 8 NOVEMBER 1519'),
(18,'INS','V21','Встреча, Ленсо де Тласкала'),
(20,'PLATE','p10a','QUETZALCOATL? · FIRST APPEARS 1552'),
(24,'INS','V18','Моктесума II. HOSTAGE')]
L[11]=[(1,'MAP','11a','Теночтитлан, Альварадо. SPRING 1520'),
(5,'PLATE','p11a','MAY 1520 · THE CITY RISES'),
(11,'MAP','11a','Дамба, Ночь печали. 30 JUNE 1520'),
(17,'PLATE','p11b','SMALLPOX · CUITLAHUAC · 80 DAYS'),
(21,'MAP','11b','Осада, 13 кораблей. MAY 1521'),
(25,'MAP','11b','Акведук и дамбы перерезаны'),
(28,'CLIP','R16','Каноэ на озере на рассвете. 13 AUGUST 1521'),
(30,'PLATE','p11c','500 SPANIARDS · TENS OF THOUSANDS OF ALLIES')]
L[12]=[(1,'MAP','12a','Мехико на руинах. 1521'),
(5,'MAP','12b','Озеро осушено. 1525 · LATE 19TH CENTURY'),
(8,'PLATE','p12a','1545 · UP TO 80%'),
(11,'INS','V22','Флорентийский кодекс. NAHUATL · 1.5 MILLION'),
(13,'INS','V08','Чинампы Сочимилько. XOCHIMILCO'),
(14,'INS','V23','Диск Койольшауки. 1978'),
(17,'INS','V04','Флаг Мексики. EAGLE · CACTUS'),
(18,'CARD','outro','Аутро-карточка; затемнение')]

def bnd(k,b):
    rows={r['i']:r for r in T[str(k)]['rows']}
    if isinstance(b,tuple):
        i,w=b; r=rows[i]; p=r['text'].find(w); assert p>=0,(k,b)
        return round(r['start']+(r['end']-r['start'])*p/len(r['text'])-0.1,2)
    if b==1: return 0.0
    return round((rows[b-1]['end']+rows[b]['start'])/2,2)
out={}; clips={}; ins={}; plates=[]; maps=set()
for k,segs in L.items():
    dur=T[str(k)]['dur']; t=[bnd(k,s[0]) for s in segs]+[dur]
    assert t==sorted(t),(k,t)
    out[k]={'dur':dur,'segs':[[t[j],t[j+1],*segs[j][1:]] for j in range(len(segs))]}
    for t0,t1,ty,i,d in out[k]['segs']:
        w=round(t1-t0,2)
        if ty=='CLIP': clips.setdefault(i,[]).append((k,t0,t1,w,d))
        if ty=='INS': ins.setdefault(i,[]).append((k,t0,t1,w,d))
        if ty=='PLATE': plates.append(i)
        if ty=='MAP': maps.add(i)
json.dump(out,open(f'{E}/layout.json','w'),indent=1,ensure_ascii=False)
sh=lambda xs: sum(x[3] for x in xs)
print('CLIPS files',len(clips),'shows',sum(len(v) for v in clips.values()),'sec in chapters',round(sum(sh([x for x in v if x[0]!=0]) for v in clips.values()),1),'cold open',round(sum(sh([x for x in v if x[0]==0]) for v in clips.values()),1))
for i in sorted(clips):
    v=clips[i]; print(i,'len',math.ceil(max(x[3] for x in v)+1),'| '+' ; '.join(f'гл{x[0]} {x[1]}–{x[2]} ({x[3]})' for x in v))
print('INS',len(ins),'shows',sum(len(v) for v in ins.values()),'sec',round(sum(sh(v) for v in ins.values()),1))
for i in sorted(ins): print(i,[ (x[0],x[3]) for x in ins[i]])
print('PLATES',len(plates),'MAPS',len(maps),sorted(maps))
