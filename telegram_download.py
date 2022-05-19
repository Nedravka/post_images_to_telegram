import datetime
import os
import json
from urllib.parse import urlsplit, unquote
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('nasa_apod_api')


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


def nasa_earth_images(TOKEN, path, n):
    counter = 0
    create_path(path)
    link_api_earth = 'https://api.nasa.gov/EPIC/'
    headers = {
        'api_key': TOKEN,
    }

    response = requests.get(f'{link_api_earth}api/natural', params=headers)
    response.raise_for_status()
    dict_response = json.loads(response.text)

    for i in dict_response[:n]:
        with open(f'{path}\\{i["image"]}.png', 'wb') as picture:
            converted_date_to_datetime = (datetime.datetime.fromisoformat(i["date"])).strftime('%Y/%m/%d')

            earth_image = requests.get(f'{link_api_earth}archive/natural/{converted_date_to_datetime}/'
                                       f'png/{i["image"]}.png',
                                       params=headers)
            earth_image.raise_for_status()
            picture.write(earth_image.content)
            counter += 1
            print('complete', counter)


def nasa_images(TOKEN, number_of_images, path):
    create_path(path)

    api = 'https://api.nasa.gov/planetary/apod'
    headers = {
        'api_key': TOKEN,
        'count': number_of_images
    }
    response_nasa_api = requests.get(api, params=headers)
    response_nasa_api.raise_for_status()

    dict_response_nasa_api = json.loads(response_nasa_api.text)

    for number, url_img in enumerate(dict_response_nasa_api):
        with open(f'{path}\\nasa_img_{number}.{file_extension(url_img["url"])}', 'wb') as file:
            img = requests.get(url_img['url'])
            file.write(img.content)


if __name__ == "__main__":
    path = 'images'
    link_api = 'https://api.spacexdata.com/v3/launches/66'
    test_url_file_extension = "https://example.com/txt/hello%20world.txt?v=9#python"
    fetch_spacex_last_launch(link_api, 'images')
    nasa_images(TOKEN, 3, 'nasa_images')
    nasa_earth_images(TOKEN, 'nasa_images_earth', 1)
