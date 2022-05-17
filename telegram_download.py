import os
import json
from urllib.parse import urlsplit, unquote
from pathlib import Path


import requests


def create_path(path):
    Path(f'{path}').mkdir(parents=True, exist_ok=True)
    os.chdir(path)


def file_extension(url):
    name_of_file = urlsplit(url).path
    file_extansion = os.path.splitext(unquote(name_of_file))
    return file_extansion[-1]


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
    test_url_file_extension = "https://example.com/txt/hello%20world.txt?v=9#python"

    create_path(path)
    fetch_spacex_last_launch(link_api)
    print(file_extension(test_url_file_extension))
