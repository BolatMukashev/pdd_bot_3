from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from config import TEST_BOT_TOKEN
import asyncio
from aiogram import Bot, Dispatcher


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


if __name__ == "__main__":

    bot = Bot(token=TEST_BOT_TOKEN)
    dp = Dispatcher()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_router(commands_router)
    dp.include_router(text_router)
    dp.include_router(payment_router)
    dp.include_router(media_router)

    async def main():
        await dp.start_polling(bot)

    asyncio.run(main())
