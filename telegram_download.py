import os
import json
from pathlib import Path


import requests


def create_path(path):
    Path(f'{path}').mkdir(parents=True, exist_ok=True)
    os.chdir(path)


def fetch_spacex_last_launch(link_api):
    api_json = requests.get(link_api)
    api_json.raise_for_status()
    dict_api = json.loads(api_json.text)

    for image in dict_api['links']['flickr_images']:
        response = requests.get(image)
        img_name = image.split('/')
        with open(img_name[-1], 'wb') as picture:
            picture.write(response.content)


if __name__ == "__main__":

    path = 'images'
    link_api = 'https://api.spacexdata.com/v3/launches/66'
    create_path(path)
    fetch_spacex_last_launch(link_api)
