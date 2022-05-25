import json
import os
from datetime import datetime

from dotenv import load_dotenv

from fetch_spacex import create_path, file_extension

import requests


LINK_NASA_API = 'https://api.nasa.gov/'


def nasa_earth_images(token_nasa_api, number_of_images, path_to_save):
    counter = 0
    create_path(path_to_save)
    headers = {
        'api_key': token_nasa_api,
    }

    response_nasa_api = requests.get(
        f'{LINK_NASA_API}EPIC/api/natural',
        params=headers
    )
    response_nasa_api.raise_for_status()
    serialize_response_nasa_api = json.loads(response_nasa_api.text)

    for image in serialize_response_nasa_api[:number_of_images]:
        print(image)
        with open(f'{path_to_save}\\{image["image"]}.png', 'wb') as picture:
            converted_date_to_datetime = (datetime.fromisoformat(image["date"])).\
                strftime('%Y/%m/%d')

            earth_image = requests.get(
                f'{LINK_NASA_API}EPIC/archive/natural/'
                f'{converted_date_to_datetime}/png/'
                f'{image["image"]}.png',
                params=headers
            )
            earth_image.raise_for_status()
            picture.write(earth_image.content)
            counter += 1
            print('complete', counter)


def nasa_images(token_nasa_api, number_of_images, path_to_save):
    create_path(path_to_save)

    headers = {
        'api_key': token_nasa_api,
        'count': number_of_images
    }
    response_nasa_api = requests.get(
        f'{LINK_NASA_API}planetary/apod',
        params=headers
    )
    response_nasa_api.raise_for_status()

    dict_response_nasa_api = json.loads(response_nasa_api.text)

    for number, url_img in enumerate(dict_response_nasa_api):

        with open(
                f'{path_to_save}\\nasa_img_{number}.'
                f'{file_extension(url_img["url"])}',
                'wb'
        ) as file:

            img = requests.get(url_img['url'])
            file.write(img.content)


if __name__ == '__main__':

    load_dotenv()
    token_nasa_api = os.getenv('nasa_apod_api')
    number_of_images = os.getenv('number_of_images', default=1)

    nasa_images(
        token_nasa_api,
        number_of_images,
        'images/nasa_images'
    )
    nasa_earth_images(
        token_nasa_api,
        1,
        'images/nasa_images_earth'
    )
