from pathlib import Path

import requests


API_SPACEX_LINK = 'https://api.spacexdata.com/v3/launches/66'


def fetch_spacex_last_launch(api_link, path):

    Path(f'{path}').mkdir(parents=True, exist_ok=True)

    api_spacex_response = requests.get(api_link)
    api_spacex_response.raise_for_status()
    api_spacex_response_json = api_spacex_response.json()

    for image in api_spacex_response_json['links']['flickr_images']:
        last_launch_image = requests.get(image)
        *_, img_name = image.split('/')

        with open(
                f'{path}\\{img_name}',
                'wb'
        ) as picture:
            picture.write(last_launch_image.content)


if __name__ == '__main__':

    fetch_spacex_last_launch(API_SPACEX_LINK, 'images/spacex')
