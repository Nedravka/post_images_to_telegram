import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

import requests

from utils import get_file_extension


NASA_API_LINK = 'https://api.nasa.gov/'


def fetch_earth_images(
        nasa_api_token,
        number_of_images,
        path_to_save
):

    Path(f'{path_to_save}').mkdir(parents=True, exist_ok=True)
    api_parameters = {
        'api_key': nasa_api_token,
    }

    api_response = requests.get(
        f'{NASA_API_LINK}EPIC/api/natural',
        params=api_parameters
    )
    api_response.raise_for_status()
    all_images_metadata = api_response.json()

    for image_metadata in all_images_metadata[:int(number_of_images)]:

        converted_date_to_datetime = (
            datetime.fromisoformat(image_metadata["date"])
        ).strftime('%Y/%m/%d')

        earth_image_url_response = requests.get(
            f'{NASA_API_LINK}EPIC/archive/natural/'
            f'{converted_date_to_datetime}/png/'
            f'{image_metadata["image"]}.png',
            params=api_parameters
        )
        earth_image_url_response.raise_for_status()

        with open(
                Path(f'{path_to_save}/{image_metadata["image"]}.png'),
                'wb'
        ) as picture:
            picture.write(earth_image_url_response.content)


def fetch_space_images(
        nasa_api_token,
        number_of_images,
        path_to_save
):

    Path(f'{path_to_save}').mkdir(parents=True, exist_ok=True)

    api_parameters = {
        'api_key': nasa_api_token,
        'count': number_of_images
    }
    api_response = requests.get(
        f'{NASA_API_LINK}planetary/apod',
        params=api_parameters
    )
    api_response.raise_for_status()

    all_images_metadata = api_response.json()

    for number, img_url in enumerate(all_images_metadata):

        image_url_response = requests.get(img_url['url'])
        image_url_response.raise_for_status()

        image_extension = get_file_extension(img_url["url"])

        with open(
                Path(f'{path_to_save}/nasa_img_{number}.{image_extension}'),
                'wb'
        ) as picture:
            picture.write(image_url_response.content)


if __name__ == '__main__':

    load_dotenv()
    nasa_api_token = os.getenv('NASA_APOD_API_TOKEN')
    number_of_images = os.getenv('NUMBER_OF_IMAGES', default=1)

    fetch_space_images(
        nasa_api_token,
        number_of_images,
        'images/nasa_images'
    )
    fetch_earth_images(
        nasa_api_token,
        number_of_images,
        'images/nasa_images_earth'
    )
