from config import TEST_BOT_TOKEN
from main import commands_router, text_router, payment_router, media_router
from aiogram import Bot, Dispatcher
import asyncio


async def on_startup():
    print("✅ Бот запущен!")


async def on_shutdown():
    print("🛑 Бот остановлен!")


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