import asyncio
import datetime
import json
import os
import time
from pathlib import Path
from urllib.parse import unquote, urlsplit

from dotenv import load_dotenv

import requests

import telegram


LINK_API_SPACEX = 'https://api.spacexdata.com/v3/launches/66'


def create_path(path):
    return Path(f'{path}').mkdir(parents=True, exist_ok=True)


def file_extension(url):
    name_of_file = urlsplit(url).path
    file_extansion = os.path.splitext(unquote(name_of_file))
    return file_extansion[-1]


def fetch_spacex_last_launch(link_api, path):
    create_path(path)
    api_json = requests.get(link_api)
    api_json.raise_for_status()
    dict_api = json.loads(api_json.text)

    for image in dict_api['links']['flickr_images']:
        response = requests.get(image)
        img_name = image.split('/')
        with open(f'{path}\\{img_name[-1]}', 'wb') as picture:
            picture.write(response.content)


def nasa_earth_images(token_nasa_api, path, n):
    counter = 0
    create_path(path)
    link_api_earth = 'https://api.nasa.gov/EPIC/'
    headers = {
        'api_key': token_nasa_api,
    }

    response = requests.get(f'{link_api_earth}api/natural', params=headers)
    response.raise_for_status()
    dict_response = json.loads(response.text)

    for i in dict_response[:n]:
        with open(f'{path}\\{i["image"]}.png', 'wb') as picture:
            converted_date_to_datetime = (datetime.datetime.
                                          fromisoformat(i["date"])).\
                strftime('%Y/%m/%d')

            earth_image = requests.get(f'{link_api_earth}archive/natural/'
                                       f'{converted_date_to_datetime}/'
                                       f'png/{i["image"]}.png',
                                       params=headers)
            earth_image.raise_for_status()
            picture.write(earth_image.content)
            counter += 1
            print('complete', counter)


def nasa_images(token_nasa_api, number_of_images, path):
    create_path(path)

    api = 'https://api.nasa.gov/planetary/apod'
    headers = {
        'api_key': token_nasa_api,
        'count': number_of_images
    }
    response_nasa_api = requests.get(api, params=headers)
    response_nasa_api.raise_for_status()

    dict_response_nasa_api = json.loads(response_nasa_api.text)

    for number, url_img in enumerate(dict_response_nasa_api):
        with open(f'{path}\\nasa_img_{number}.'
                  f'{file_extension(url_img["url"])}', 'wb') as file:
            img = requests.get(url_img['url'])
            file.write(img.content)


def generate_path_to_image(directory_with_images):
    path_to_directory_with_images = Path(__file__).parent.\
                                    joinpath(directory_with_images)
    images_folders = os.walk(path_to_directory_with_images, topdown=False)
    path_image_generator = (f'{root}\\{file_name}'
                            for root, dirs, list_of_files in images_folders
                            for file_name in list_of_files)
    for path in path_image_generator:
        yield path


async def post_photo_to_telegram(telegram_bot_api, path_to_image):
    bot = telegram.Bot(telegram_bot_api)
    async with bot:
        await bot.send_document(
            chat_id='@cosmo_and_me',
            document=open(path_to_image, 'rb')
        )


def main():
    load_dotenv()
    token_nasa_api = os.getenv('nasa_apod_api')
    telegram_bot_api = os.getenv('telegram_bot_api')
    fetch_spacex_last_launch(LINK_API_SPACEX, 'images/spasex')
    nasa_images(token_nasa_api, 3, 'images/nasa_images')
    nasa_earth_images(token_nasa_api, 'images/nasa_images_earth', 1)
    path_to_image = generate_path_to_image('images')
    while True:
        try:
            asyncio.run(post_photo_to_telegram(telegram_bot_api,
                                               next(path_to_image)
                                               ))
            time.sleep(int(os.getenv('upload_photo_delay')))
        except StopIteration:
            print('Скрипт остановлен. Загрузите новые фото.')
            break


if __name__ == "__main__":
    main()
