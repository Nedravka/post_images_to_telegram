import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

import requests

from utils import get_file_extension, save_images


NASA_API_LINK = 'https://api.nasa.gov/'


def fetch_nasa_images_earth(
        nasa_api_token,
        number_of_images,
        path_to_save
):

    Path(f'{path_to_save}').mkdir(parents=True, exist_ok=True)
    nasa_api_parameters = {
        'api_key': nasa_api_token,
    }

    nasa_api_response = requests.get(
        f'{NASA_API_LINK}EPIC/api/natural',
        params=nasa_api_parameters
    )
    nasa_api_response.raise_for_status()
    nasa_api_response_json = nasa_api_response.json()

    for image in nasa_api_response_json[:number_of_images]:

        converted_date_to_datetime = (datetime.fromisoformat(image["date"])). \
            strftime('%Y/%m/%d')

        earth_image = requests.get(
            f'{NASA_API_LINK}EPIC/archive/natural/'
            f'{converted_date_to_datetime}/png/'
            f'{image["image"]}.png',
            params=nasa_api_parameters
        )
        earth_image.raise_for_status()

        save_images(
            f'{path_to_save}\\{image["image"]}.png',
            'wb',
            earth_image
        )


def fetch_nasa_images_space(
        nasa_api_token,
        number_of_images,
        path_to_save
):

    Path(f'{path_to_save}').mkdir(parents=True, exist_ok=True)

    nasa_api_parameters = {
        'api_key': nasa_api_token,
        'count': number_of_images
    }
    nasa_api_response = requests.get(
        f'{NASA_API_LINK}planetary/apod',
        params=nasa_api_parameters
    )
    nasa_api_response.raise_for_status()

    nasa_api_response_dict = nasa_api_response.json()

    for number, url_img in enumerate(nasa_api_response_dict):

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

    fetch_nasa_images_space(
        token_nasa_api,
        number_of_images,
        'images/nasa_images'
    )
    fetch_nasa_images_earth(
        token_nasa_api,
        number_of_images,
        'images/nasa_images_earth'
    )
