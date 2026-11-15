# Ages in Minutes — конвейер сборки выпуска

Структуру папок не менять: скрипты ищут `maps/data` и `channel/` по относительным путям.
Карфаген (выпуск 3) — эталон: новый вид карт, сборщик глав, холодное открытие поверх роликов.

    maps/data/                геометрия Natural Earth (суша 10m/50m, реки) — общая для всех выпусков
    channel/                  логотип
    carthage/cards.py         заставки глав (3,5 с)
    carthage/maps/engine.py   движок карт (Pillow + numpy -> ffmpeg), общий
    carthage/maps/look.py     принятый вид карт: рельефный шум, зелёная суша, тёмное море, зерно, виньетка
    carthage/maps/ca_base.py  цвета, города, полигоны регионов выпуска
    carthage/maps/ca_scenes.py сцены карт выпуска; `python3 ca_scenes.py list | still имя@t`
    carthage/maps/run_look.py `python3 run_look.py render <сцены>` -> out_look/
    carthage/film/gfxlib.py   текст, плашки, вырезки (obj), полнокадровые фото (photo)
    carthage/film/chapters.py графика и раскладка по времени всех глав (SPECS)
    carthage/film/build.py    `python3 build.py 1 2 3` -> out/chNN.mp4; звук: голос -14 LUFS, ролики <= 7 %
    carthage/film/list.txt    порядок склейки: ffmpeg -f concat -safe 0 -i list.txt -c copy
    carthage/coldopen/        холодное открытие: coldopen.py (графика), coldopen2.py (поверх роликов)

    maps/engine.py, maps/scenes.py   карты пилота (Персия), старый вид
    egypt/                    выпуск 2: заставки, карты (старый вид), сценарий
    persia/script.md          сценарий пилота
    cards/, covers/, channel/ заставки пилота, оверлеи обложек, баннер и водяной знак

В репозиторий не входят: видео (rec/, out/), озвучка (vo/), музыка, модель rembg (isnet-general-use.onnx, качается с GitHub releases в ~/.u2net).
Для нового выпуска: скопировать папку carthage под новым именем, заменить *_base.py, *_scenes.py, chapters.py, script.md.
