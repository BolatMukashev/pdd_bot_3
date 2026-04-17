from ydb_logic import *
import asyncio


# yc iam create-token   (12 часов действует)
# ngrok http 127.0.0.1:8080 - поднять webhood локально на 8080 порту


async def add_new_fake_user(telegram_id: int, first_name: str, username: str, language_code: str):

    new_user = User(
        telegram_id=telegram_id,
        first_name=first_name,
        username=username,
        language_code=language_code,
    )

    async with UserClient() as client:
        user = await client.insert_user(new_user)

    print(f"✅ Пользователь {first_name} успешно добавлен в базу (ID: {telegram_id})")
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


if __name__ == "__main__":
    # asyncio.run(add_new_fake_user(12345678909, "Bolat", "kimi", "ru"))
    asyncio.run(get_user_by_id(12345678909))

