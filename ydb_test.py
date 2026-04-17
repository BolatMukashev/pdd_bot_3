from ydb_logic import *
import asyncio
import random


# yc iam create-token   (12 часов действует)
# ngrok http 127.0.0.1:8080 - поднять webhood локально на 8080 порту


async def add_new_fake_user(user: User):
    async with UserClient() as client:
        user = await client.insert_user(user)

    print(f"✅ Пользователь {user.first_name} успешно добавлен в базу (ID: {user.telegram_id})")
    return user


async def get_user_by_id(telegram_id: int):
    async with UserClient() as client:
        user = await client.get_user_by_id(telegram_id)
        print(user)
        create_time = await get_user_create_time(user)
        print(create_time)
    return user


async def get_user_create_time(user: User):
        from datetime import timedelta, timezone
        kz_tz = timezone(timedelta(hours=5))
        dt = UserClient.timestamp_to_datetime(user.created_at).astimezone(kz_tz)
        return dt.strftime("%H:%M:%S %Y-%m-%d")


async def add_new_fake_question(question: Question, table_name: QuestionsTables = QuestionsTables.RU.value):
    async with QuestionClient(table_name) as client:
        await client.insert_question(question)
    print(f"✅ Вопрос  успешно добавлен в базу")


async def get_questions_count(table_name: QuestionsTables = QuestionsTables.RU.value):
    async with QuestionClient(table_name) as client:
        count = await client.get_questions_count()
        print(f"Всего вопросов: {count}")
        return count
    

async def get_question_by_id(id: int, table_name: QuestionsTables = QuestionsTables.RU.value):
    async with QuestionClient(table_name) as client:
        question = await client.get_question_by_id(id)
        print(question)
    return question


async def get_random_question(table_name: QuestionsTables = QuestionsTables.RU.value):
    count = await get_questions_count(table_name)
    random_num = random.randint(1, count)
    async with QuestionClient(table_name) as client:
        question = await client.get_question_by_id(random_num)
        print(question)
    return question


if __name__ == "__main__":
    new_user = User(
        telegram_id=12345678909,
        first_name="Bolat",
        username="kimi",
        language_code="ru",
    )
    # asyncio.run(add_new_fake_user(new_user)
    # asyncio.run(get_user_by_id(12345678909))
    # asyncio.run(get_user_by_id(12345678909))

    new_question = Question(
         id=2,
         question="город в Казахстане?",
         options=["Астана", "Лондон", "Париж"],
         correct_option_id=0
    )

    # asyncio.run(add_new_fake_question(new_question))

    asyncio.run(get_random_question())

