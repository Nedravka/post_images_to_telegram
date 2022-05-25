import json
import os
from pathlib import Path
from urllib.parse import unquote, urlsplit

import requests


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


if __name__ == '__main__':

    fetch_spacex_last_launch(LINK_API_SPACEX, 'images/spasex')
