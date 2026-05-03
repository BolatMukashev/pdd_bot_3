# main.py
from aiogram import F, Router
from aiogram.types import Message, PollAnswer, LabeledPrice, PreCheckoutQuery
from aiogram.filters import CommandStart, Command
from ydb_functions import discount_check, get_discount_end_time, get_random_question, add_new_user, get_user_by_id, trial_check, add_new_payment, edit_user_field
from ydb_logic import QuestionsTables, User, Payment, PaymentType
from aiogram import Bot
from config import AMOUNT, ADMIN_ID
from languages import get_texts


commands_router = Router()
text_router = Router()
media_router = Router()
payment_router = Router()
poll_router = Router()


@commands_router.message(CommandStart())
async def cmd_start(message: Message):

    user_lang = message.from_user.language_code
    texts = await get_texts(user_lang)

    new_user = User(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username,
        language_code=user_lang,
    )

    await add_new_user(new_user)

    await message.answer(texts["TEXT"]["start"].format(full_name=message.from_user.full_name))


@commands_router.message(Command("theme"))
async def cmd_theme(message: Message):
    await message.answer("Вы выбрали тему оформления! (пока не работает)")


@commands_router.message(Command("books"))
async def cmd_books(message: Message):
    await message.answer("Вы выбрали список книг! (пока не работает)")


@commands_router.message(Command("donate"))
async def cmd_donate(message: Message):
    await message.answer("Вы выбрали поддержку проекта! (пока не работает)")


@text_router.message(F.text)
async def echo(message: Message):
    user_lang = message.from_user.language_code
    texts = await get_texts(user_lang)

    await message.answer(texts["TEXT"]["echo"])


@commands_router.message(Command("question"))
async def cmd_question(message: Message):
    # отправить quiz
    user_id = message.from_user.id
    user_lang = message.from_user.language_code
    texts = await get_texts(user_lang)
    
    user = await get_user_by_id(user_id)

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
        await message.answer(texts["TEXT"]["stop"])


@poll_router.poll_answer()
async def handle_poll_answer(poll_answer: PollAnswer, bot: Bot):
    # Отправить quiz в ответ на quiz
    chat_id = poll_answer.user.id
    user_lang = poll_answer.user.language_code
    texts = await get_texts(user_lang)

    user = await get_user_by_id(chat_id)
    is_trial_active = await trial_check(user)

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
        await bot.send_message(chat_id=chat_id, text=texts["TEXT"]["stop"])


@media_router.message(F.photo)
async def get_photo_file_id(message: Message):
    largest_photo = message.photo[-1]
    file_id = largest_photo.file_id
    print(file_id)
    await message.answer(f"file_id:\n{file_id}")


@commands_router.message(Command("pay"))
async def cmd_pay(message: Message):
    user_id = message.from_user.id
    user_lang = message.from_user.language_code
    texts = await get_texts(user_lang)
    user = await get_user_by_id(user_id)
    if user.is_paid:
        await message.answer(texts["TEXT"]["payment"]["already_paid"])
        return

    label = texts["TEXT"]["payment"]["label"]
    title = texts["TEXT"]["payment"]["title"]
    
    is_discount_active = await discount_check(user)

    if is_discount_active:
        amount = int(AMOUNT / 2)
        discount_end_time = await get_discount_end_time(user)
        description = texts["TEXT"]["payment"]["description_discount"].format(amount=amount, AMOUNT=AMOUNT, discount_end_time=discount_end_time)
    else:
        amount = AMOUNT
        description = texts["TEXT"]["payment"]["description"]

    if user_id == ADMIN_ID:
        amount = 1

    prices = [LabeledPrice(label=label, amount=amount)]
    pay_message = await message.answer_invoice(title=title,
                                                description=description,
                                                payload=f"payment|amount",
                                                provider_token="",
                                                currency="XTR",
                                                prices=prices)


# ------------------------------------------------------------------- ОПЛАТА -------------------------------------------------------


@payment_router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@payment_router.message(F.successful_payment)
async def on_successful_payment(message: Message):
    payload = message.successful_payment.invoice_payload
    user_id = message.from_user.id
    user_lang = message.from_user.language_code

    texts = await get_texts(user_lang) # получение текста на языке пользователя
    
    _, amount = payload.split("|") # получение данных

    # добавление платежа в бд
    new_payment = Payment(
        telegram_id=user_id,
        amount=int(amount),
        type=PaymentType.ACCESS.value
    )

    await add_new_payment(new_payment)

    await edit_user_field(user_id, "is_paid", True)

    # сообщение о приеме платежа
    await message.answer(texts["TEXT"]["payment"]["payment_accepted"])

