import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from config import BOT_API_KEY


# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_API_KEY)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! 👋\n"
        "Я эхо-бот — просто напиши мне что-нибудь, и я повторю."
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Просто напиши любое сообщение, и я его повторю!")


@dp.message(F.text)
async def echo(message: Message):
    await message.answer(message.text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())