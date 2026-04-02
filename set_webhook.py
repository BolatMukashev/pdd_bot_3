# set_webhook.py — запускается локально один раз
import asyncio
from aiogram import Bot
from config import FUNCTION_URL, BOT_TOKEN


async def main():
    bot = Bot(token=BOT_TOKEN)
    await bot.set_webhook(FUNCTION_URL)
    print("Webhook установлен!")
    await bot.session.close()

asyncio.run(main())