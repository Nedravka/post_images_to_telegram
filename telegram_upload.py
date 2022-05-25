import asyncio
import os
import time
from pathlib import Path

from dotenv import load_dotenv

import telegram


def generate_path_to_image(directory_with_images):
    path_to_directory_with_images = Path(__file__).parent.\
                                    joinpath(directory_with_images)
    images_folders = os.walk(path_to_directory_with_images, topdown=False)
    path_image_generator = (f'{root}\\{file_name}'
                            for root, dirs, list_of_files in images_folders
                            for file_name in list_of_files)
    for path in path_image_generator:
        yield path


async def post_photo_to_telegram(telegram_bot_api, path_to_image):
    bot = telegram.Bot(telegram_bot_api)
    async with bot:
        await bot.send_document(
            chat_id='@cosmo_and_me',
            document=open(path_to_image, 'rb')
        )


def main():
    load_dotenv()
    telegram_bot_api = os.getenv('telegram_bot_api')
    path_to_image = generate_path_to_image('images')
    while True:
        try:
            asyncio.run(post_photo_to_telegram(telegram_bot_api,
                                               next(path_to_image)
                                               ))
            time.sleep(int(os.getenv('upload_photo_delay', default=86400)))
        except StopIteration:
            print('Скрипт остановлен. Загрузите новые фото.')
            break


if __name__ == "__main__":
    main()
