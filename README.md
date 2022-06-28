# Загрузка фотографий в Telegram
Набор скриптов которые позволяют скачать фотографии космоса и космических объектов
с помощью соответствующих API [NASA](https://api.nasa.gov/) 
и [SPACEX](https://docs.spacexdata.com), сохранить их в репозиторий на сервере и 
в дальнейшем опубликовать в канале Telegram через бота.
## Как установить
Достаточно скопировать репозиторий командой:

    git clone https://github.com/Nedravka/post_images_to_telegram.git

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

    pip install -r requirements.txt
## Как работать со скриптами скачивающими фотографии
#### Для скачивания фотографий с сайта NASA:
Необходимо зарегистрироваться на сайте [NASA](https://api.nasa.gov/) и получить API токен.
Далее в директории скрипта создать файл .env и прописать туда токен авторизации в формате:

    NASA_APOD_API = [ваш токен авторизации]
Туда же можно прописать количество фотографий для скачивания в формате:

    NUMBERS_OF_IMAGES = [цифра соответствующая необходимому количеству фотографий]
Или создать соответствующие переменные окружения в упомянутом формате другим способом, соответствующим вашей операционной системе.

Запустить скрипт командой:

    python fetch_nasa.py

#### Для скачивания фотографий с сайта SPACEX:   

Запустить скрипт командой:
    
    python fetch_spacex.py
    
## Как работать со скриптом загружающим фотографии в Telegram

Необходимо зарегистрировать бота по инструкции ["Регистрация бота в telegram"](https://way23.ru/регистрация-бота-в-telegram.html)
и сохранить полученный токен API бота в созданном файле .env в формате:

    TELEGRAM_BOT_API = [API токен бота]

Аналогично добавить id канала, куда будут загружаться фотографии в формате:
    
    CHAT_ID = [@id_канала]

Для корректировки задержки загрузки файлов в telegram канал можно также прописать переменную в файл .env  в формате:

    UPLOAD_PHOTO_DELAY = [время в секундах]
По умолчанию задержка установлена равной 24 часа.

Запустить скрипт командой:

    python telegram_upload.py

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](http://dvmn.org).
## Ссылки
Documentation NASA API: [https://api.nasa.gov/](https://api.nasa.gov/)

Documentation SPACEX API: [https://docs.spacexdata.com](https://docs.spacexdata.com)

Documentation Telegram bot API: [https://docs.djangoproject.com/en/1.11/](https://docs.djangoproject.com/en/1.11/)
   
Git: [https://git-scm.com/docs/git](https://git-scm.com/docs/git)
    
Source Code: [https://github.com/Nedravka/post_images_to_telegram.git](https://github.com/Nedravka/post_images_to_telegram.git)
