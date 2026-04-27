from typing import Any

from ydb_logic import *
import asyncio
import random
from config import ADMIN_ID

# yc iam create-token   (12 часов действует)
# ngrok http 127.0.0.1:8080 - поднять webhood локально на 8080 порту


async def add_new_user(user: User) -> User:
    async with UserClient() as client:
        user = await client.insert_user(user)

    print(f"✅ Пользователь {user.full_name} успешно добавлен в базу (ID: {user.telegram_id})")
    return user


async def get_user_by_id(telegram_id: int) -> tuple[User, bool]:
    async with UserClient() as client:
        user = await client.get_user_by_id(telegram_id)
        if user is None:
            return None, False
        is_trial_active = await trial_check(user)
        print(user, is_trial_active)
    return user, is_trial_active


async def trial_check(user: User) -> bool:
        # Проверяем, не истек ли пробный период. Если true - пробный период активен, если false - пробный период истек
        from datetime import datetime, timezone
        trial_ends_at = UserClient.timestamp_to_datetime(user.trial_ends_at)
        now = datetime.now(timezone.utc)
        return now < trial_ends_at


async def get_user_time_utc5(user: User) -> str:
        from datetime import timedelta, timezone
        kz_tz = timezone(timedelta(hours=5))
        created_at = UserClient.timestamp_to_datetime(user.created_at).astimezone(kz_tz)
        trial_ends_at = UserClient.timestamp_to_datetime(user.trial_ends_at).astimezone(kz_tz)
        return created_at.strftime("%H:%M:%S %d-%m-%Y"), trial_ends_at.strftime("%H:%M:%S %d-%m-%Y")


async def add_new_question(question: Question, table_name: QuestionsTables) -> None:
    async with QuestionClient(table_name) as client:
        await client.insert_question(question)
    print(f"✅ Вопрос  успешно добавлен в базу")


async def get_questions_count(table_name: QuestionsTables) -> int:
    async with QuestionClient(table_name) as client:
        count = await client.get_questions_count()
        print(f"Всего вопросов: {count}")
        return count


async def get_question_by_id(id: int, table_name: QuestionsTables) -> Question:
    async with QuestionClient(table_name) as client:
        question = await client.get_question_by_id(id)
        print(question)
    return question


async def get_random_question(table_name: QuestionsTables) -> Question:
    count = await get_questions_count(table_name)
    random_num = random.randint(1, count)
    async with QuestionClient(table_name) as client:
        question = await client.get_question_by_id(random_num)
        print(question)
    return question


async def delete_question_by_id(id: int, table_name: QuestionsTables) -> None:
    async with QuestionClient(table_name) as client:
        await client.delete_question(id)
    print(f"✅ Вопрос с ID {id} успешно удален из базы")


async def get_user_info(telegram_id: int):
    user, is_trial_active = await get_user_by_id(telegram_id)
    created_at, trial_ends_at = await get_user_time_utc5(user)
    print(f"Пользователь: {user}\n" \
          f"Пробный период активен: {is_trial_active}\n" \
          f"Дата создания: {created_at}\n" \
          f"Дата окончания пробного периода: {trial_ends_at}")
    

async def edit_user_field(telegram_id: int, field_name: str, new_value: Any) -> None:
    async with UserClient() as client:
        await client.update_user_fields(telegram_id, **{field_name: new_value})
    print(f"✅ Поле {field_name} пользователя с ID {telegram_id} успешно обновлено на {new_value}")
    

async def add_new_payment(payment: Payment) -> Payment:
    async with PaymentClient() as client:
        payment = await client.insert_payment(payment)
    print(f"✅ Платеж успешно добавлен в базу (ID: {payment.id})")
    return payment


if __name__ == "__main__":
    new_user = User(
        telegram_id=12345678909,
        full_name="Bolat",
        username="kimi",
        language_code="ru",
    )

    # asyncio.run(add_new_user(new_user)
    # asyncio.run(get_user_by_id(12345678909))
    # asyncio.run(get_user_by_id(12345678909))

    new_question = Question(
         id=1301,
         question="город в Казахстане1?",
         options=["Астана", "Лондон1", "Париж"],
         correct_option_id=0,
         explanation="Потому что Астана - столица Казахстана",
         image="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Astana_Collage.png/2560px-Astana_Collage.png",
         image_dark="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Astana_Collage.png/2560px-Astana_Collage.png"
    )

    # asyncio.run(delete_question_by_id(1301, QuestionsTables.RU))

    # asyncio.run(get_random_question(QuestionsTables.RU))

    # asyncio.run(get_user_info(int(ADMIN_ID)))

    new_payment = Payment(
        telegram_id=12345678909,
        amount=1000,
        product_id=2,
        type=PaymentType.PAY.value
    )

    # asyncio.run(add_new_payment(new_payment))


    # asyncio.run(edit_user_field(ADMIN_ID, "is_paid", True))





