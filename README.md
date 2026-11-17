# Ages in Minutes — конвейер сборки выпуска

Структуру папок не менять: скрипты ищут `maps/data` и `channel/` по относительным путям.
Эталон кода — persia/ (последний завершённый выпуск): движок карт, сборщик глав с режимом черновика, карточки, холодное открытие. carthage/ — прежняя версия, как основа не годится. План: общий код в core/, папки выпусков — только данные (см. скилл ages-in-minutes-episode).
Отрендеренные сцены карт Vikings лежат в ветке renders-vikings (в main видео не хранится): git fetch origin renders-vikings && git checkout FETCH_HEAD -- vikings/maps/out_look

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
    carthage/film/build.py    `python3 build.py 1 2 3` -> out/chNN.mp4, мастер 2560x1440, 60 кадров/с, crf 14; звук: голос -14 LUFS, ролики <= 7 %
    carthage/film/list.txt    порядок склейки: ffmpeg -f concat -safe 0 -i list.txt -c copy
    carthage/coldopen/        холодное открытие: coldopen.py (графика), coldopen2.py (поверх роликов)

    maps/engine.py, maps/scenes.py   карты пилота (Персия), старый вид
    egypt/                    выпуск 2: заставки, карты (старый вид), сценарий
    persia/script.md          сценарий пилота
    cards/, covers/, channel/ заставки пилота, оверлеи обложек, баннер и водяной знак

В репозиторий не входят: видео (rec/, out/), озвучка (vo/), музыка, модель rembg (isnet-general-use.onnx, качается с GitHub releases в ~/.u2net).
Для нового выпуска: взять код из persia/ (после переноса — из core/), заменить *_base.py, *_scenes.py, chapters.py, script.md.
