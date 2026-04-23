# main.py

from aiogram import F, Router
from aiogram.types import Message, PollAnswer
from aiogram.filters import CommandStart, Command
from ydb_functions import get_random_question
from ydb_logic import QuestionsTables
from aiogram import Bot


commands_router = Router()
text_router = Router()
media_router = Router()
payment_router = Router()
poll_router = Router()


@commands_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")


@text_router.message(F.text)
async def echo(message: Message):
    await message.answer(message.text)


@commands_router.message(Command("question"))
async def question(message: Message):
    random_question = await get_random_question(QuestionsTables.RU)
    if random_question.image:
        await message.answer_photo(random_question.image)

    await message.answer_poll(question=random_question.question,
                              question_photo=random_question.image,
                              options=random_question.options,
                              type="quiz",
                              correct_option_id=random_question.correct_option_id,
                              explanation=random_question.explanation,
                              description=str(random_question.id),
                              is_closed=False,
                              is_anonymous=False,
                              allows_multiple_answers=False)


@poll_router.poll_answer()
async def handle_poll_answer(poll_answer: PollAnswer, bot: Bot):
    random_question = await get_random_question(QuestionsTables.RU)

    option_ids = poll_answer.option_ids

    chat_id = poll_answer.user.id

    if random_question.image:
        await bot.send_photo(chat_id=chat_id, photo=(random_question.image))

    await bot.send_poll(chat_id=chat_id,
                        question=random_question.question,
                        options=random_question.options,
                        type="quiz",
                        correct_option_id=random_question.correct_option_id,
                        explanation=random_question.explanation,
                        description=str(random_question.id),
                        is_closed=False,
                        is_anonymous=False,
                        allows_multiple_answers=False)


@media_router.message(F.photo)
async def get_photo_file_id(message: Message):
    largest_photo = message.photo[-1]
    file_id = largest_photo.file_id
    print(file_id)
    await message.answer(f"file_id:\n{file_id}")

