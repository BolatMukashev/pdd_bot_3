from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command


commands_router = Router()
text_router = Router()
media_router = Router()
payment_router = Router()


async def on_startup():
    print("✅ Бот запущен!")


async def on_shutdown():
    print("🛑 Бот остановлен!")


@commands_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")


@text_router.message(F.text)
async def echo(message: Message):
    await message.answer(message.text)
