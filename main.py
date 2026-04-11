from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import Bot


commands_router = Router()
text_router = Router()
media_router = Router()
payment_router = Router()


@commands_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")


@text_router.message(F.text)
async def echo(message: Message):
    await message.answer(message.text)


@commands_router.message(Command("question"))
async def question(message: Message):
    await message.answer_photo()
    await message.answer_poll()

@media_router.message(F.photo)
async def get_photo_file_id(message: Message):
    largest_photo = message.photo[-1]
    file_id = largest_photo.file_id
    print(file_id)
    await message.answer(f"file_id:\n{file_id}")

