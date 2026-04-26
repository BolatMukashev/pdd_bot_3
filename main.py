# main.py

from aiogram import F, Router
from aiogram.types import Message, PollAnswer
from aiogram.filters import CommandStart, Command
from ydb_functions import get_random_question, add_new_user, get_user_by_id, trial_check
from ydb_logic import QuestionsTables, User
from aiogram import Bot


commands_router = Router()
text_router = Router()
media_router = Router()
payment_router = Router()
poll_router = Router()


@commands_router.message(CommandStart())
async def cmd_start(message: Message):
    new_user = User(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username,
        language_code=message.from_user.language_code,
    )

    await add_new_user(new_user)
    await message.answer(f"Привет, {message.from_user.full_name}!")
    await message.answer("Нажми на /question, чтобы получить вопрос!")


@text_router.message(F.text)
async def echo(message: Message):
    await message.answer("Нажми на /question, чтобы получить вопрос!")


@commands_router.message(Command("question"))
async def question(message: Message):
    # отправить quiz
    user_id = message.from_user.id
    user, is_trial_active = await get_user_by_id(user_id)
    if user is None:
        new_user = User(telegram_id=message.from_user.id,
                        full_name=message.from_user.full_name,
                        username=message.from_user.username,
                        language_code=message.from_user.language_code)

        user = await add_new_user(new_user)
        is_trial_active = await trial_check(user)

    if user.is_paid or is_trial_active:
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
    else:
        await message.answer("Ваш пробный период истек.\n" \
        "Пожалуйста, произведите оплату, чтобы продолжить использовать бота\n" \
        "Оплатить: /pay")


@poll_router.poll_answer()
async def handle_poll_answer(poll_answer: PollAnswer, bot: Bot):
    # Отправить quiz в ответ на quiz
    chat_id = poll_answer.user.id
    user, is_trial_active = await get_user_by_id(chat_id)
    if user is None:
        new_user = User(telegram_id=chat_id,
                        full_name=poll_answer.user.full_name,
                        username=poll_answer.user.username,
                        language_code=poll_answer.user.language_code)

        user = await add_new_user(new_user)
        is_trial_active = await trial_check(user)

    if user.is_paid or is_trial_active:
        random_question = await get_random_question(QuestionsTables.RU)
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
        
    else:
        await bot.send_message(chat_id=chat_id, text="Ваш пробный период истек.\n" \
        "Пожалуйста, произведите оплату, чтобы продолжить использовать бота\n" \
        "Оплатить: /pay")


@media_router.message(F.photo)
async def get_photo_file_id(message: Message):
    largest_photo = message.photo[-1]
    file_id = largest_photo.file_id
    print(file_id)
    await message.answer(f"file_id:\n{file_id}")

