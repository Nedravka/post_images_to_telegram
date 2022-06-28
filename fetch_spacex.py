from pathlib import Path

import requests

from utils import save_images

LINK_API_SPACEX = 'https://api.spacexdata.com/v3/launches/66'


def fetch_spacex_last_launch(link_api, path):

    Path(f'{path}').mkdir(parents=True, exist_ok=True)

    response_api_spacex = requests.get(link_api)
    response_api_spacex.raise_for_status()
    dict_api = response_api_spacex.json()

    for image in dict_api['links']['flickr_images']:
        response = requests.get(image)
        *_, img_name = image.split('/')

        # with open(f'{path}\\{img_name}', 'wb') as picture:
        #     picture.write(response.content)
        save_images(f'{path}\\{img_name}', response)


if __name__ == '__main__':

    fetch_spacex_last_launch(LINK_API_SPACEX, 'images/spacex')
