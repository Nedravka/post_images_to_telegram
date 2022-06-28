import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

import requests

from utils import get_file_extension, save_images


LINK_NASA_API = 'https://api.nasa.gov/'


def fetch_nasa_earth_images(token_nasa_api, number_of_images, path_to_save):

    Path(f'{path_to_save}').mkdir(parents=True, exist_ok=True)
    headers = {
        'api_key': token_nasa_api,
    }

    response_nasa_api = requests.get(
        f'{LINK_NASA_API}EPIC/api/natural',
        params=headers
    )
    response_nasa_api.raise_for_status()
    serialize_response_nasa_api = response_nasa_api.json()

    for image in serialize_response_nasa_api[:number_of_images]:

        converted_date_to_datetime = (datetime.fromisoformat(image["date"])). \
            strftime('%Y/%m/%d')

        earth_image = requests.get(
            f'{LINK_NASA_API}EPIC/archive/natural/'
            f'{converted_date_to_datetime}/png/'
            f'{image["image"]}.png',
            params=headers
        )
        earth_image.raise_for_status()

        save_images(
            f'{path_to_save}\\{image["image"]}.png',
            'wb',
            earth_image
        )


def fetch_nasa_images(token_nasa_api, number_of_images, path_to_save):

    Path(f'{path_to_save}').mkdir(parents=True, exist_ok=True)

    headers = {
        'api_key': token_nasa_api,
        'count': number_of_images
    }
    response_nasa_api = requests.get(
        f'{LINK_NASA_API}planetary/apod',
        params=headers
    )
    response_nasa_api.raise_for_status()

    dict_response_nasa_api = response_nasa_api.json()

    for number, url_img in enumerate(dict_response_nasa_api):

        img = requests.get(url_img['url'])

        save_images(
            f'{path_to_save}\\nasa_img_{number}.'
            f'{get_file_extension(url_img["url"])}',
            'wb',
            img
        )


if __name__ == '__main__':

    load_dotenv()
    token_nasa_api = os.getenv('NASA_APOD_API')
    number_of_images = os.getenv('NUMBER_OF_IMAGES', default=1)

    fetch_nasa_images(
        token_nasa_api,
        number_of_images,
        'images/nasa_images'
    )
    fetch_nasa_earth_images(
        token_nasa_api,
        1,
        'images/nasa_images_earth'
    )
