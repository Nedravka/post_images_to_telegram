import asyncio
import os

import telegram
from dotenv import load_dotenv


async def main():
    load_dotenv()
    token_api_bot = os.getenv('telegram_bot_api')
    bot = telegram.Bot(token_api_bot)
    async with bot:
        print(await bot.get_me())
        await bot.send_document(chat_id='@cosmo_and_me', document=open('nasa_images/nasa_img_1..jpg', 'rb'))

if __name__ == '__main__':
    asyncio.run(main())
