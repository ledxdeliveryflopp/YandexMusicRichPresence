# YandexMusicRichPresence


**Discord RPC для показа музыки которую вы сейчас слушаете в десктопном приложении Яндекс музыка.
Загрузка треков и информации о них происходит через API яндекс музыки.**

![plot](/static/md/discord.png)

Приложение представляет из себя API и asar архив с измененными скриптами(для отслеживания запуска и паузы музыки)

## Требования
Работа проверена Windows 10, на других версиях и платформах работать будет(у самой API нет требования к платформе).

Если вы не будете использовать ехе файл то:
1. Python >=3.12

## Как скачать и использовать Exe?
IDK

## Как использовать без exe?(а зачем?)

1. pip install poetry.
2. poetry install
3. python main.py

>Чтобы скомпилировать скрипт с помощью [Nuitka](https://pypi.org/project/nuitka/), выполните данную команду:  
`nuitka --standalone --windows-icon-from-ico=static\icon\icon.ico main.py`


## TODO
1. Добавить активности для плейлистов и тд(на подобии простаивания)
2. иногда может ставится произвольно пауза(в основом на музыке из плейлистов)
3. иногда после паузы идет не верный расчет оставшегося времени
   
------------
Инструменты используемые в приложении
1. FastApi
2. Poetry
3. Pypresence
4. Nuitka