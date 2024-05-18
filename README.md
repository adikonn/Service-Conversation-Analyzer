# РЖД Анализ Служебных переговоров
Хакатон Цифровой Прорыв
## Команда Procrastination
Состав:

- Муратшин Динияр [@tww1st](https://t.me/tww1st)
- Гарифуллин Тимур [@Murkat07](https://t.me/Murkat07)
- Калмурзин Адилет [@aishiluu](https://t.me/aishiluu)

## Установка
Скачайте Microsoft C++ Build Tools (необходимо для билда некоторых библиотек)

```bash
$ git clone https://github.com/Murkat-git/Service-Conversation-Analyzer
$ cd Service-Conversation-Analyzer
$ cp example.env .env
$ mkdir music
$ conda env create -n conversation-analyzer -f environment.yml
$ docker compose pull
```
Заполните токены в .env

## Использование
```bash
$ docker compose up -d
$ conda activate conversation-analyzer
$ python transcribe.py
```
