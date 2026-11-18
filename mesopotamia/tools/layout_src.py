# Раскладка глав Mesopotamia — единственный источник чисел для layout.json, брифа и списка вставок.
# Граница отрезка задаётся фразой озвучки, а не секундой:
#   i        — начало фразы i (середина паузы перед ней; для i=1 — 0)
#   (i,'..') — внутри фразы i, перед словами '..' (линейно по буквам)
# t1 отрезка = t0 следующего; последний отрезок идёт до конца главы.
# Типы: MAP карта, CLIP ролик, INS вставка (предмет/фото), PLATE плашка (типографика), CARD карточка.
# Запуск: python3 layout_src.py  → ../layout.json + сводка роликов, вставок, плашек и карт.
import json,os,math,re
H=os.path.dirname(os.path.abspath(__file__)); E=os.path.dirname(H)
T=json.load(open(f'{E}/timing.json'))

L={
0:[(1,'CLIP','R11','Астроном на крыше ночью. 60 SECONDS · 60 MINUTES'),
(3,'CLIP','R02','Канал и поле ячменя. SOUTHERN IRAQ · 4,000 YEARS AGO'),
(4,'CLIP','R03','Урук сверху. THE FIRST CITIES · THE FIRST WRITTEN LAWS · THE OLDEST EPIC POEM'),
(5,'CLIP','R04','Писец давит знаки в глину. AN ACCOUNTANT'),
((6,'a baby'),'CLIP','R07','Корзина в тростнике на реке. A BABY IN A BASKET'),
((6,'the oldest customer'),'CLIP','R09','Двор медника. THE OLDEST CUSTOMER COMPLAINT'),
((6,'a party'),'CLIP','R13','Ворота дворца с ламассу, гости. 69,000 GUESTS'),
((6,'a library'),'CLIP','R16','Горящий дворец ночью. A LIBRARY THAT SURVIVED BECAUSE IT BURNED'),
((6,'and a tower'),'CLIP','R17','Вавилон сверху, зиккурат. THE TOWER OF BABEL'),
(7,'CLIP','R01','Тростниковые дома и лодки на болотах. MUD AND REEDS → MESOPOTAMIA · IT TAKES TWENTY MINUTES')],
1:[(1,'MAP','01a','Горы Турции → две реки → залив. EUPHRATES · TIGRIS · PERSIAN GULF · MESOPOTAMIA — BETWEEN THE RIVERS · IRAQ'),
(6,'PLATE','p1a','ALMOST NO RAIN · NO STONE · NO TIMBER · NO METAL'),
(9,'CLIP','R01','Болота. WATER, MUD AND REEDS'),
(10,'PLATE','p1b','NILE · SUMMER · ON TIME ↔ TIGRIS & EUPHRATES · APRIL–MAY · THE BARLEY IS RIPENING'),
(14,'CLIP','R02','Крестьяне поднимают вал канала, вода идёт в поле. CANALS · BANKS'),
(16,'MAP','01b','Юг: сеть каналов зеленеет. THE RICHEST FARMLAND ON EARTH'),
(17,'MAP','01c','Точки деревень по югу, затем Эриду у берега залива. 5000 BC · ERIDU'),
(21,'PLATE','p1c','Ряды-слои растут снизу вверх (18 полос). EIGHTEEN TEMPLES')],
2:[(1,'MAP','02a','Наезд на Урук на Евфрате. 3500 BC · URUK'),
(3,'CLIP','R03','Урук сверху. 3100 BC · 50,000 PEOPLE · THE LARGEST CITY ON EARTH'),
(5,'MAP','02b','План Урука: два храмовых квартала. AN · INANNA'),
(6,'INS','V01','Ваза из Варки. BARLEY · OIL · BEER'),
(7,'PLATE','p2a','Ряды точек. THOUSANDS OF JARS · HUNDREDS OF WORKERS'),
(10,'CLIP','R04','Писец давит знаки в мокрую глину. 3300 BC'),
(11,'INS','V02','Протоклинописная табличка. A SHEEP · A JAR · BARLEY · NUMBERS'),
(15,'MAP','02c','Урук и Египет на одной карте. THE OLDEST WRITING ON EARTH · TO KEEP ACCOUNTS'),
(18,'INS','V03','Клинописная табличка крупно, клинья. CUNEIFORM · CUNEUS — WEDGE · 3,000 YEARS'),
(21,'INS','V04','Табличка Кушима. 29,086 · 37 MONTHS · KUSHIM → A NAME OR A JOB TITLE? · AN ACCOUNTANT')],
3:[(1,'MAP','03a','Шумер: города по словам озвучки. UR · LAGASH · UMMA · KISH · NIPPUR · SUMERIAN'),
(5,'PLATE','p3a','EACH CITY BELONGS TO ITS GOD · THE RULER — THE GOD\'S STEWARD'),
(7,'CLIP','R05','Зиккурат над городом. ZIGGURAT'),
(8,'MAP','03b','Лагаш и Умма, полоса Гуэдены. GU\'EDENA — THE EDGE OF THE PLAIN · THE EARLIEST WAR BETWEEN STATES'),
(12,'INS','V05','Стела коршунов целиком. 2450 BC · EANNATUM · LAGASH'),
(13,'CLIP','R06','Строй Лагаша перед боем: щиты сомкнуты, копья вперёд'),
(14,'INS','V05','Стела коршунов, фрагмент со строем. THE STELE OF THE VULTURES · THE OLDEST WAR MONUMENT'),
(16,'MAP','03b','Граница проведена, дважды нарушена. AGAIN · AND AGAIN'),
(19,'PLATE','p3b','GILGAMESH · KING OF URUK · NO INSCRIPTION FOUND'),
(21,'MAP','02b','План Урука, обводится стена. URUK\'S GREAT WALL · THE OLDEST GREAT STORY')],
4:[(1,'MAP','04a','Север, Киш; Аккад — область, не точка. 2334 BC'),
(2,'INS','V06','Бронзовая голова аккадского царя. SARGON — TRUE KING'),
(4,'CLIP','R07','Корзина из тростника плывёт по реке'),
(7,'PLATE','p4a','AKKI · A WATER-DRAWER · A GARDENER'),
(9,'MAP','04b','Киш → Урук → Ниппур. CUPBEARER · LUGALZAGESI · THE GATE OF ENLIL'),
(12,'MAP','04c','Аккад и Шумер одним цветом; знак вопроса на месте Аккада. AKKAD + SUMER · NEVER FOUND'),
(15,'INS','V07','Диск Энхедуанны. UR · ENHEDUANNA · THE FIRST AUTHOR KNOWN BY NAME'),
(19,'INS','V08','Стела Нарам-Сина. NARAM-SIN · KING OF THE FOUR QUARTERS · A GOD'),
(22,'CLIP','R08','Потрескавшиеся поля, пустая деревня. 2200 BC · DROUGHT'),
(24,'MAP','04d','Гутии с гор Загроса. GUTIANS'),
(25,'PLATE','p4b','THE CURSE OF AKKAD: THE GREAT FIELDS GAVE NO GRAIN… THE FLOODED FIELDS GAVE NO FISH')],
5:[(1,'MAP','05a','Ур подсвечен. UR'),
(2,'CLIP','R05','Зиккурат Ура. 2112 BC · UR-NAMMU'),
(3,'INS','V09','Фото зиккурата Ура сегодня. STILL STANDS TODAY'),
(4,'INS','V10','Табличка законов Ур-Намму. THE OLDEST LAW CODE · 300 YEARS BEFORE HAMMURABI'),
(5,'PLATE','p5a','SURPRISINGLY MILD → A TOOTH = 2 SHEKELS OF SILVER'),
(8,'INS','V11','Закладная фигура Шульги. SHULGI · 48 YEARS'),
(9,'PLATE','p5b','ROADS · WEIGHTS · CALENDAR · ARMY'),
(10,'INS','V12','Хозяйственная табличка Ура III. TENS OF THOUSANDS OF TABLETS'),
(12,'MAP','05b','Ниппур → Ур и обратно, линия бега. A GOD · 160 KM · AND BACK · ONE DAY'),
(14,'MAP','05c','Амореи с запада, Элам на Ур. AMORITES · GRAIN ×60 · 2004 BC · ELAM'),
(18,'PLATE','p5c','SUMERIAN → THE SCHOOLS · 2,000 YEARS · LIKE LATIN')],
6:[(1,'MAP','06a','Вавилон на Евфрате. AMORITES · BABYLON'),
(4,'INS','V13','Стела Хаммурапи, верх: царь перед Шамашем. 1792 BC · HAMMURABI'),
(5,'MAP','06b','Вавилон забирает весь юг. ALL OF SOUTHERN MESOPOTAMIA · CAPITAL FOR 1,000+ YEARS'),
(7,'INS','V13','Стела целиком, проход сверху вниз. 2 METRES · SHAMASH · 282 LAWS'),
(10,'PLATE','p6a','AN EYE FOR AN EYE · THE BUILDER SHALL BE PUT TO DEATH'),
(13,'PLATE','p6b','EQUAL → AN EYE · COMMONER → 1 MINA OF SILVER · SLAVE → HALF HIS PRICE · WHO YOU WERE'),
(18,'INS','V14','Старовавилонское письмо в конверте. LETTERS ON CLAY'),
(19,'CLIP','R09','Двор медника: слитки, гонец с табличкой. 1750 BC · UR · NANNI · EA-NASIR'),
(20,'INS','V15','Табличка с жалобой Эа-насиру + строки цитаты. FINE COPPER · BAD INGOTS · CONTEMPT · FINE QUALITY'),
(23,'CLIP','R09','Тот же двор. THE HOUSE OF EA-NASIR?'),
(24,'INS','V15','Табличка жалобы. THE OLDEST CUSTOMER COMPLAINT ON RECORD')],
7:[(1,'CLIP','R10','Дом табличек: ученики пишут, учитель. THE TABLET HOUSE'),
(3,'INS','V16','Школьная табличка. COPYING · CANED FOR MISTAKES'),
(4,'PLATE','p7a','60 → 2 · 3 · 4 · 5 · 6 · 10 · 12 · 15 · 20 · 30 (по словам)'),
(7,'PLATE','p7b','60 MINUTES · 60 SECONDS · 360°'),
(8,'INS','V17','YBC 7289. √2 = 1.414213'),
(10,'INS','V18','Плимптон 322. RIGHT-ANGLED TRIANGLES · WHOLE NUMBERS'),
(11,'PLATE','p7c','Шкала: 1800 BC → PYTHAGORAS · 1,000+ YEARS LATER'),
(13,'CLIP','R11','Астроном на крыше ночью, табличка в руках. THE MOON AND THE PLANETS'),
(15,'PLATE','p7d','OMENS → THE LONGEST SERIES OF OBSERVATIONS IN THE ANCIENT WORLD · GREEK ASTRONOMERS')],
8:[(1,'MAP','08a','Царство Хаммурапи сжимается; хетты: Хаттуса → Вавилон → домой. 1595 BC · MURSILI · MARDUK'),
(4,'MAP','08b','Касситы с Загроса. KASSITES · 400+ YEARS'),
(6,'INS','V19','Касситский кудурру. MORE BABYLONIAN THAN THE BABYLONIANS'),
(7,'MAP','08c','Великие державы и линии писем. EGYPT · HITTITES · MITANNI · ASSYRIA · BABYLON · AKKADIAN'),
(10,'INS','V20','Письмо из Амарны (не EA 7 — оно утрачено). BURNA-BURIASH → AKHENATEN · 40 MINAS → NOT EVEN 10'),
(12,'MAP','08d','Элам: Сузы → Вавилон и обратно; на карте врезки V08 и V13 едут в Сузы. 1158 BC · SHUTRUK-NAHHUNTE · SUSA → IRAN · THE LOUVRE')],
9:[(1,'MAP','09a','Ашшур на Тигре. ASHUR · ASSYRIANS'),
(3,'MAP','09a','Стрелки походов каждый год. 900s BC'),
(4,'CLIP','R12','Две колесницы на равнине. CHARIOTS · CAVALRY · SIEGE ENGINES · IRON'),
(5,'MAP','09a','Нимруд. ASHURNASIRPAL II · NIMRUD'),
(6,'INS','V21','Ламассу из Нимруда'),
(7,'CLIP','R13','Ворота дворца, гости с факелами'),
((7,'and lists'),'INS','V22','Стела пира. 69,574 GUESTS · TEN DAYS'),
(8,'PLATE','p9a','10,000 JARS OF BEER · 10,000 SKINS OF WINE'),
(9,'PLATE','p9b','FEAR · THE CITIES THEY BURNED · THE REBELS THEY PUNISHED'),
(11,'INS','V23','Рельеф Тиглатпаласара III. TIGLATH-PILESER III'),
(12,'CLIP','R14','Колонна переселенцев: семья, повозка, двое конвойных'),
(13,'MAP','09b','Стрелки переселений по державе; Самария. ≈ 4,000,000 · 720s BC · ISRAEL · THE TEN LOST TRIBES'),
(16,'MAP','09c','Иудея. 701 BC · SENNACHERIB · LACHISH'),
(17,'INS','V24','Рельеф осады Лахиша (только штурм стен)'),
(18,'MAP','09c','Иерусалим в кольце. JERUSALEM'),
(19,'INS','V25','Призма Синаххериба. HEZEKIAH · LIKE A BIRD IN A CAGE'),
(20,'MAP','09c','Стрелка домой. NEVER TOOK THE CITY · TRIBUTE')],
10:[(1,'INS','V26','Рельеф: Ашшурбанапал на колеснице (без раненых львов). ASHURBANIPAL · 668 BC'),
(2,'MAP','10a','Ассирия в наибольших границах. THE NILE → THE MOUNTAINS OF IRAN'),
(3,'INS','V26','Тот же рельеф. NINEVEH · LIONS'),
(4,'PLATE','p10a','HE COULD READ · AND HE COLLECTED'),
(6,'CLIP','R15','Писцы раскладывают таблички по корзинам. OMENS · SPELLS · MEDICINE · DICTIONARIES · EPICS'),
(7,'MAP','10b','Ниневия. THE GREATEST LIBRARY OF THE ANCIENT NEAR EAST'),
(8,'MAP','10c','631 BC; вавилоняне и мидяне на Ниневию; держава гаснет. 612 BC · BABYLONIANS · MEDES'),
(11,'CLIP','R16','Горящий дворец ночью, крыша рушится. THE FIRE SAVED THE LIBRARY'),
(13,'PLATE','p10b','30,000+ TABLETS · THE 1850s · THE BRITISH MUSEUM'),
(14,'INS','V27','Фото Джорджа Смита. 1872 · GEORGE SMITH'),
(15,'INS','V28','Табличка о потопе. A BOAT · A FLOOD · A MOUNTAIN · BIRDS · OLDER THAN THE BIBLE'),
(17,'PLATE','p10c','HE JUMPED UP… AND BEGAN TO TAKE OFF HIS CLOTHES'),
(18,'INS','V28','Табличка о потопе. TABLET XI · THE EPIC OF GILGAMESH'),
(19,'MAP','02b','План Урука со стеной. ENKIDU · NEVER TO DIE'),
(20,'CLIP','R03','Урук сверху, стена. THE WALL OF HIS CITY')],
11:[(1,'MAP','11a','Вавилония в наибольших границах. 605 BC · NEBUCHADNEZZAR II'),
(3,'CLIP','R18','Ворота Иштар: синий кирпич, быки и драконы'),
(4,'INS','V29','Лев с дороги процессий. THE PROCESSIONAL WAY'),
((4,'leads to the temple'),'CLIP','R17','Вавилон сверху, Этеменанки. ETEMENANKI · 91 M × 91 M × 91 M'),
(6,'INS','V31','«Вавилонская башня» Брейгеля (1563). THE TOWER OF BABEL'),
(7,'PLATE','p11a','THE HANGING GARDENS? · NO CUNEIFORM TEXT · NEVER FOUND'),
(9,'MAP','11b','Вавилон и Ниневия. SENNACHERIB\'S GARDENS?'),
(11,'MAP','11c','Иерусалим → Вавилон. 587 BC'),
(12,'PLATE','p11b','BY THE RIVERS OF BABYLON, THERE WE SAT DOWN AND WEPT'),
(13,'INS','V30','Стела Набонида. NABONIDUS'),
(14,'MAP','11d','Оазис Тейма в Аравии. TEN YEARS · BELSHAZZAR'),
(15,'PLATE','p11c','Шкала: NARAM-SIN ~2250 BC ← NABONIDUS ~550 BC · THE FIRST ARCHAEOLOGIST'),
(18,'MAP','11e','Персы, Вавилон открывает ворота. 539 BC · CYRUS')],
12:[(1,'MAP','12a','Александр → Вавилон. 331 BC · JUNE 323 BC'),
(3,'CLIP','R11','Астроном на крыше. THEIR DIARY OF THE SKY'),
(4,'MAP','12b','Селевкия на Тигре, Вавилон бледнеет. SELEUCIA'),
(5,'PLATE','p12a','CLAY AND WEDGES → INK AND THE ALPHABET'),
(7,'CLIP','R19','Последний писец Урука при лампе. AD 79 · URUK'),
(8,'PLATE','p12b','Шкала: 3300 BC URUK → AD 79 URUK'),
(9,'PLATE','p12c','APRIL 2003 · THE IRAQ MUSEUM · 15,000 OBJECTS'),
(11,'INS','V01','Ваза из Варки. 5,000 YEARS · IN PIECES · RESTORED'),
(14,'INS','V02','Протоклинописная табличка. WRITING'),
(16,'INS','V13','Стела Хаммурапи. WRITTEN LAW'),
(17,'PLATE','p12d','60 MINUTES · 360°'),
(18,'INS','V28','Табличка о потопе. A FLOOD · THE FEAR OF DEATH'),
(19,'CLIP','R01','Болота на рассвете. A PLAIN OF MUD BETWEEN TWO RIVERS'),
(20,'CARD','outro','Аутро-карточка: SUBSCRIBE · WHICH CIVILIZATION NEXT?; затемнение')],
}

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
inch=sum(sh([x for x in v if x[0]!=0]) for v in clips.values())
print('CLIPS files',len(clips),'shows',sum(len(v) for v in clips.values()),'sec in chapters',round(inch,1),'cold open',round(sum(sh([x for x in v if x[0]==0]) for v in clips.values()),1))
for i in sorted(clips):
    v=clips[i]; mx=max(x[3] for x in v)
    print(i,'len',math.ceil(mx+1),'| '+' ; '.join(f'гл{x[0]} {x[1]}–{x[2]} ({x[3]})' for x in v))
print('INS',len(ins),'shows',sum(len(v) for v in ins.values()),'sec',round(sum(sh(v) for v in ins.values()),1))
print('PLATES',len(plates),'MAPS',len(maps),sorted(maps))
