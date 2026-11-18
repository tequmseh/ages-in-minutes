# Вставки Mesopotamia V01–V31: что, где взять, тип. Окна показов — только из ../layout.json.
# Запуск: python3 inserts_src.py → ../layout_inserts.json + ../inserts.md
import json,os
H=os.path.dirname(os.path.abspath(__file__)); E=os.path.dirname(H)
L=json.load(open(f'{E}/layout.json'))
# kind: cut = вырезка PNG (rembg) на фон с мягкой тенью; full = кадр целиком (фото места, картина, рельеф кадрированием)
V={
'V01':('Ваза из Варки (Урук, ок. 3000 до н. э.), Иракский музей','cut','Commons: «Warka Vase» (фото Osama Shukir Muhammed Amin, CC BY-SA) — целиком, все три пояса'),
'V02':('Протоклинописная табличка о выдаче ячменя (Урук, ок. 3100–2900)','cut','Met 1988.433.1 или Met 327384 — Open Access CC0'),
'V03':('Клинописная табличка крупно, хорошо видны клинья (Ур III, ок. 2028)','cut','Met 327069 «record of rations of beer, bread, oil, and onions for messengers» — CC0'),
'V04':('Табличка Кушима (Урук III, MS 1717, бывшая коллекция Шёйен)','cut','Commons: «Kushim tablet». Если свободного фото нет (только аукцион с водяным знаком) — не брать, окно закрою плашкой'),
'V05':('Стела коршунов Эаннатума (Лувр): 1) целиком, 2) фрагмент со строем воинов','cut','Commons: «Stele of the Vultures Louvre» (фото Eric Gaba и др., CC BY-SA). Нужны оба: общий вид и крупный фрагмент со щитами и копьями. Фрагмент с головами в клювах крупно не брать'),
'V06':('Бронзовая голова аккадского правителя из Ниневии (Иракский музей)','cut','Commons: «Bronze head of an Akkadian ruler» / «Mask of Sargon». По правилу о портретах ставлю как Саргона'),
'V07':('Диск Энхедуанны (Пенсильванский музей, B16665)','cut','Commons: «Disk of Enheduanna» (CC BY-SA)'),
'V08':('Победная стела Нарам-Сина (Лувр, Sb 4)','cut','Commons: «Victory Stele of Naram-Sin» — целиком. Нужна и для карты 08d (врезка едет в Сузы)'),
'V09':('Зиккурат Ура сегодня (фото)','full','Commons: «Ziggurat of Ur 2005» — фото армии США, PD. Без людей и техники на переднем плане'),
'V10':('Табличка законов Ур-Намму (Стамбул, Ni 3191)','cut','Commons: «Code of Ur-Nammu Istanbul» (CC BY-SA)'),
'V11':('Закладная фигура Шульги с корзиной (медь)','cut','Met 324831 — CC0'),
'V12':('Хозяйственная табличка Ура III с оттиском печати («отгрузка ячменя», ок. 2029)','cut','Met 321819 — CC0'),
'V13':('Стела законов Хаммурапи (Лувр): верх с царём и Шамашем + целиком','cut','Commons: «Code of Hammurabi Louvre» — целиком, от основания до верха, ≥ 2000 px по высоте (нужен проход сверху вниз). Нужна и для карты 08d'),
'V14':('Старовавилонское частное письмо (табличка)','cut','Met 321706 (86.11.111) — CC0'),
'V15':('Табличка с жалобой Нанни на Эа-насира (Ур, ок. 1750)','cut','Commons: «Complaint tablet to Ea-nasir» — фото посетителя музея, CC BY-SA. Собственные снимки Британского музея (BY-NC-SA) не брать'),
'V16':('Школьная табличка-«линза»: образец учителя и копия ученика','cut','Met 321878 (86.11.251) — CC0'),
'V17':('YBC 7289: квадрат с диагоналями и √2 (Йель)','cut','Commons: «YBC 7289» (фото Bill Casselman; лицензию проверю по файлу)'),
'V18':('Плимптон 322 (Колумбийский университет)','cut','Commons: «Plimpton 322» (PD)'),
'V19':('Касситский кудурру (межевой камень с символами богов)','cut','Commons: «Kudurru Melishipak Louvre» или другой касситский кудурру; Met CC0, если найдётся'),
'V20':('Письмо из Амарны: царь Ассирии Ашшур-убаллит — фараону','cut','Met 24.2.11 — CC0. Это не письмо Бурна-Буриаша (EA 7 погибло в Берлине); на экране не подписываю его как EA 7'),
'V21':('Ламассу из Нимруда — крылатый бык с человеческой головой','cut','Met 32.143.1 — CC0. Он же референс для ролика R13'),
'V22':('Стела пира Ашшурнасирпала II (Мосульский музей)','cut','Commons: «Banquet Stele of Ashurnasirpal II»'),
'V23':('Рельеф с Тиглатпаласаром III (Нимруд)','cut','Commons: «Tiglath-Pileser III relief» — фото посетителя, CC BY-SA'),
'V24':('Рельеф осады Лахиша — фрагмент штурма стен','full','Commons: «Lachish relief» — кадрирую только штурм стен; посаженных на кол и казни в кадр не беру'),
'V25':('Призма Синаххериба (Тейлора или Чикагская)','cut','Commons: «Sennacherib prism» / «Taylor prism»'),
'V26':('Рельеф: Ашшурбанапал на колеснице на охоте','full','Commons: «Ashurbanipal lion hunt chariot» — кадр с царём и колесницей; умирающих львов (львица со стрелами) в кадр не беру'),
'V27':('Фото Джорджа Смита (1870-е)','full','Commons: «George Smith (assyriologist)» — PD'),
'V28':('Табличка о потопе (табличка XI «Эпоса о Гильгамеше», K.3375)','cut','Commons: «Flood Tablet Gilgamesh» — фото посетителя, CC BY-SA / PD'),
'V29':('Лев с дороги процессий в Вавилоне (глазурованный кирпич)','cut','Met 31.13.2 — CC0'),
'V30':('Стела Набонида','cut','Commons: «Stele of Nabonidus» (Британский музей — только фото посетителя, CC BY-SA)'),
'V31':('Питер Брейгель Старший, «Вавилонская башня» (1563, Вена)','full','Commons: «Pieter Bruegel the Elder – The Tower of Babel (Vienna)» — PD, Google Art Project'),
}
uses={}
for k,v in L.items():
    for a,b,ty,i,d in v['segs']:
        if ty=='INS' or (ty=='MAP' and any(x in d for x in ('V08','V13'))):
            ids=[i] if ty=='INS' else [x for x in ('V08','V13') if x in d]
            for j in ids: uses.setdefault(j,[]).append({'ch':int(k),'t0':a,'t1':b,'on':'map '+i if ty=='MAP' else 'frame','text':d})
assert set(V)>=set(uses) and set(uses)==set(V),(set(V)^set(uses))
J={'_note':'Единственный источник вставок Mesopotamia. Окна — из layout.json (секунды от начала озвучки главы). kind: cut — вырезка PNG на фон с мягкой тенью; full — кадр целиком. files — заполняются после получения материалов. Изображения в git не лежат.',
   'inserts':{i:{'what':V[i][0],'kind':V[i][1],'source':V[i][2],'uses':uses[i],'files':[]} for i in sorted(V)}}
json.dump(J,open(f'{E}/layout_inserts.json','w'),indent=1,ensure_ascii=False)
f=lambda x:f"{x:.1f}".replace('.',',')
out=['| № | Что | Тип | Где взять | Куда (глава: секунды) |','|---|---|---|---|---|']
for i in sorted(V):
    w='; '.join(f"гл. {u['ch']}: {f(u['t0'])}–{f(u['t1'])}"+(' (на карте)' if u['on']!='frame' else '') for u in uses[i])
    out.append(f"| {i} | {V[i][0]} | {'вырезка' if V[i][1]=='cut' else 'кадр целиком'} | {V[i][2]} | {w} |")
open(f'{E}/inserts.md','w').write('\n'.join(out))
print(len(V),'inserts,',sum(len(u) for u in uses.values()),'shows')
