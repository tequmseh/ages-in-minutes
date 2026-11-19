# Контур острова Теночтитлан-Тлателолко для плана города: обведённые по карте Wikimedia острова (lakes.json: №12 Теночтитлан, №14 Тлателолко),
# расширенные поясом намывных земель и чинампами и слитые в один остров (в 1519 г. города соединены). Площадь сверяется с источниками: 8–13,5 км².
# Запуск: python3 city.py  -> city.json (shapely нужен только здесь, не при рендере).
import json, os
from shapely.geometry import Polygon
from shapely.ops import unary_union
HERE = os.path.dirname(os.path.abspath(__file__))
KX, KY = 104.9, 111.0
lk = json.load(open(os.path.join(HERE, "lakes.json")))
isl = {i: o["ring"] for i, o in enumerate(lk) if o["hole"]}   # номера как в lakes.json
def km(r): return Polygon([(x * KX, y * KY) for x, y in r]).buffer(0)
core = {12: 0.42, 14: 0.35}                                   # км: ширина пояса намывных земель вокруг обведённого острова
parts = [km(isl[i]).buffer(b) for i, b in core.items()]
city = unary_union(parts)
for i, r in isl.items():                                    # острова, которые задеты городом, входят в него
    if i not in core and km(r).intersects(city): city = unary_union([city, km(r).buffer(0.2)])
city = city.buffer(0.18).buffer(-0.18)                         # закрыть узкие заливы между кварталами
city = city.simplify(0.02)
ring = [(round(x / KX, 5), round(y / KY, 5)) for x, y in city.exterior.coords]
json.dump({"ring": ring, "area_km2": round(city.area, 2)}, open(os.path.join(HERE, "city.json"), "w"))
minx, miny, maxx, maxy = city.bounds
print("area km2", round(city.area, 2), "bbox km", round(maxx - minx, 2), "x", round(maxy - miny, 2), "pts", len(ring), "type", city.geom_type)
