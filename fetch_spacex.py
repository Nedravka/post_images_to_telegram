from pathlib import Path

import requests


SPACEX_API_LINK = 'https://api.spacexdata.com/v3/launches/66'


def fetch_spacex_last_launch(path):

    Path(f'{path}').mkdir(parents=True, exist_ok=True)

    api_response = requests.get(SPACEX_API_LINK)
    api_response.raise_for_status()
    launch_metadata = api_response.json()

    for image in launch_metadata['links']['flickr_images']:
        image_response = requests.get(image)
        image_response.raise_for_status()
        *_, img_name = image.split('/')

        with open(
                Path(f'{path}/{img_name}'),
                'wb'
        ) as picture:
            picture.write(image_response.content)


if __name__ == '__main__':

    fetch_spacex_last_launch('images/spacex')
