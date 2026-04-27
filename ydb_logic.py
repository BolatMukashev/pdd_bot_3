import asyncio
import ydb
from enum import Enum
from typing import Optional, Dict, Any, List
from config import YDB_ENDPOINT, YDB_PATH, YDB_TOKEN
from dataclasses import dataclass
from datetime import datetime, timezone
import json


# yc iam create-token   (12 часов действует)
# ngrok http 127.0.0.1:8080 - поднять webhood локально на 8080 порту
# пропускная способность базы - 50 запросов/секунду сейчас


__all__ = ['YDBClient',
           'User',
           'UserClient',
           'Payment',
           'PaymentClient',
           'PaymentType',
           'Question',
           'QuestionClient',
           'QuestionsTables'
           ]


# ---------------------------------------------------------- БАЗОВЫЙ КЛАСС ---------------------------------------------------------


class YDBClient:
    def __init__(self, endpoint: str = YDB_ENDPOINT, database: str = YDB_PATH, token: str = YDB_TOKEN):
        """
        Инициализация клиента YDB
        """
        self.endpoint = endpoint
        self.database = database
        self.token = token
        self.driver = None
        self.pool = None
        self.credentials = ydb.AccessTokenCredentials(self.token) # ydb.iam.MetadataUrlCredentials()
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def connect(self):
        """
        Создание соединения с YDB и инициализация пула сессий
        """
        if self.driver is not None:
            return  # уже подключены
            
        driver_config = ydb.DriverConfig(
            self.endpoint, 
            self.database,
            credentials=self.credentials,
            root_certificates=ydb.load_ydb_root_certificate(),
        )
        
        self.driver = ydb.aio.Driver(driver_config)
        
        try:
            await self.driver.wait(timeout=5)
            self.pool = ydb.aio.QuerySessionPool(self.driver)
            print("Successfully connected to YDB")
        except TimeoutError:
            print("Connect failed to YDB")
            print("Last reported errors by discovery:")
            print(self.driver.discovery_debug_details())
            await self.driver.stop()
            self.driver = None
            raise
    
    async def close(self):
        """
        Закрытие соединения с YDB
        """
        if self.pool:
            await self.pool.stop()
            self.pool = None
        
        if self.driver:
            await self.driver.stop()
            self.driver = None
            print("YDB connection closed")
    
    def _ensure_connected(self):
        """
        Проверка, что соединение установлено
        """
        if self.driver is None or self.pool is None:
            raise RuntimeError("YDB client is not connected. Call connect() first or use as async context manager.")
    
    async def table_exists(self, table_name: str) -> bool:
        """
        Проверка существования таблицы
        """
        self._ensure_connected()
        try:
            await self.pool.execute_with_retries(f"SELECT 1 FROM `{table_name}` LIMIT 0;")
            return True
        except ydb.GenericError:
            return False
    
    async def create_table(self, table_name: str, schema: str):
        """
        Создание таблицы с заданной схемой (если она не существует)
        """
        self._ensure_connected()
        print(f"\nChecking if table {table_name} exists...")
        try:
            await self.pool.execute_with_retries(schema)
            print(f"Table {table_name} created successfully!")
        except ydb.GenericError as e:
            if "path exist" in str(e):
                print(f"Table {table_name} already exists, skipping creation.")
            else:
                raise e
    
    async def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None):
        """
        Выполнение произвольного запроса
        """
        self._ensure_connected()
        return await self.pool.execute_with_retries(query, params)
    
    async def clear_all_tables(self):
        """Удаляет все записи во всех таблицах"""
        self._ensure_connected()

        tables = [
            "users",
            "payments",
            "questions",
        ]

        for table in tables:
            try:
                await self.execute_query(f"DELETE FROM `{table}`;")
                print(f"Таблица {table} очищена.")
            except Exception as e:
                print(f"Ошибка при очистке {table}: {e}")


# ------------------------------------------------------------ ПОЛЬЗОВАТЕЛЬ -----------------------------------------------------------


@dataclass
class User:
    telegram_id: int
    full_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    created_at: Optional[int] = None  # Храним как timestamp (секунды с эпохи)
    trial_ends_at: Optional[int] = None  # Храним как timestamp (секунды с эпохи)
    is_paid: bool = False
    night_mode: bool = False


class UserClient(YDBClient):
    def __init__(self, endpoint: str = YDB_ENDPOINT, database: str = YDB_PATH, token: str = YDB_TOKEN):
        super().__init__(endpoint, database, token)
        self.table_name = "users"
        self.table_schema = """
            CREATE TABLE `users` (
                `telegram_id` Uint64 NOT NULL,
                `full_name` Utf8,
                `username` Utf8,
                `language_code` Utf8,
                `created_at` Uint64,
                `trial_ends_at` Uint64,
                `is_paid` Bool,
                `night_mode` Bool,
                PRIMARY KEY (`telegram_id`)
            )
        """
    
    async def create_users_table(self):
        """Создание таблицы users"""
        await self.create_table(self.table_name, self.table_schema)
    
    async def insert_user(self, user: User) -> User:
        """Вставка или обновление пользователя (UPSERT) и возврат объекта User"""

        user_data = await self.get_user_by_id(user.telegram_id)

        if user_data is None:
            from datetime import datetime, timezone, timedelta
            user.created_at = self.datetime_to_timestamp(datetime.now(timezone.utc))
            user.trial_ends_at = self.datetime_to_timestamp(datetime.now(timezone.utc) + timedelta(days=1))

        else:
            user.created_at = user_data.created_at
            user.trial_ends_at = user_data.trial_ends_at

        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DECLARE $full_name AS Utf8?;
            DECLARE $username AS Utf8?;
            DECLARE $language_code AS Utf8?;
            DECLARE $created_at AS Uint64?;
            DECLARE $trial_ends_at AS Uint64?;
            DECLARE $is_paid AS Bool;
            DECLARE $night_mode AS Bool;

            UPSERT INTO users (
                telegram_id, full_name, username, language_code, created_at, trial_ends_at, is_paid, night_mode
            ) VALUES (
                $telegram_id, $full_name, $username, $language_code, $created_at, $trial_ends_at, $is_paid, $night_mode
            );
            """,
            self._to_params(user)
        )
        return await self.get_user_by_id(user.telegram_id)

    async def get_user_by_id(self, telegram_id: int) -> Optional[User]:
        """Получение пользователя по telegram_id"""
        result = await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;

            SELECT telegram_id, full_name, username, language_code, created_at, trial_ends_at, is_paid, night_mode
            FROM users
            WHERE telegram_id = $telegram_id;
            """,
            {"$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64)}
        )

        rows = result[0].rows
        if not rows:
            return None

        return self._row_to_user(rows[0])

    async def update_user(self, user: User) -> User:
        """Обновление данных пользователя по объекту User"""
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DECLARE $full_name AS Utf8?;
            DECLARE $username AS Utf8?;
            DECLARE $language_code AS Utf8?;
            DECLARE $trial_ends_at AS Uint64?;
            DECLARE $is_paid AS Bool;
            DECLARE $night_mode AS Bool;

            UPDATE users SET
                full_name = $full_name,
                username = $username,
                language_code = $language_code,
                trial_ends_at = $trial_ends_at,
                is_paid = $is_paid,
                night_mode = $night_mode
            WHERE telegram_id = $telegram_id;
            """,
            self._to_params(user)
        )
        return await self.get_user_by_id(user.telegram_id)
    
    async def update_user_fields(self, user_id: int, **fields: Any) -> bool:
        """Обновление выбранных полей пользователя по user_id"""
        if not fields:
            return False

        FIELD_TYPES = {
            "full_name":     ydb.OptionalType(ydb.PrimitiveType.Utf8),
            "username":      ydb.OptionalType(ydb.PrimitiveType.Utf8),
            "language_code": ydb.OptionalType(ydb.PrimitiveType.Utf8),
            "is_paid":       ydb.PrimitiveType.Bool,
            "night_mode":    ydb.PrimitiveType.Bool
        }

        # Маппинг типов YDB -> строка для DECLARE
        TYPE_DECLARE = {
            "full_name":     "Utf8?",
            "username":      "Utf8?",
            "language_code": "Utf8?",
            "is_paid":       "Bool",
            "night_mode":    "Bool"
        }

        user_fields = {k: v for k, v in fields.items() if k in FIELD_TYPES}

        if not user_fields:
            return False

        set_clauses = []
        params = {"$telegram_id": (user_id, ydb.PrimitiveType.Uint64)}
        declare_lines = ["DECLARE $telegram_id AS Uint64;"]

        for field, value in user_fields.items():
            param_name = f"${field}"
            param_type = FIELD_TYPES[field]
            declare_type = TYPE_DECLARE[field]

            set_clauses.append(f"{field} = {param_name}")
            params[param_name] = (value, param_type)
            declare_lines.append(f"DECLARE {param_name} AS {declare_type};")

        query = f"""
            {' '.join(declare_lines)}

            UPDATE users
            SET {', '.join(set_clauses)}
            WHERE telegram_id = $telegram_id;
        """

        await self.execute_query(query, params)
        return True

    async def delete_user(self, telegram_id: int) -> None:
        """Удаление пользователя"""
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DELETE FROM users WHERE telegram_id = $telegram_id;
            """,
            {"$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64)}
        )

    def _row_to_user(self, row) -> User:
        return User(
            telegram_id=row["telegram_id"],
            full_name=row.get("full_name"),
            username=row.get("username"),
            language_code=row.get("language_code"),
            created_at=row.get("created_at"),
            trial_ends_at=row.get("trial_ends_at"),
            is_paid=row.get("is_paid"),
            night_mode=row.get("night_mode")
        )

    def _to_params(self, user: User) -> dict:
        return {
            "$telegram_id": (user.telegram_id, ydb.PrimitiveType.Uint64),
            "$full_name": (user.full_name, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$username": (user.username, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$language_code": (user.language_code, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$created_at": (user.created_at, ydb.OptionalType(ydb.PrimitiveType.Uint64)),
            "$trial_ends_at": (user.trial_ends_at, ydb.OptionalType(ydb.PrimitiveType.Uint64)),
            "$is_paid": (user.is_paid, ydb.PrimitiveType.Bool),
            "$night_mode": (user.night_mode, ydb.PrimitiveType.Bool)
        }
    
    @staticmethod
    def timestamp_to_datetime(timestamp: int):
        from datetime import datetime, timezone
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
    
    @staticmethod
    def datetime_to_timestamp(dt: datetime) -> int:
        return int(dt.timestamp())


# ------------------------------------------------------------ ПЛАТЕЖИ -----------------------------------------------------------


class PaymentType(str, Enum):
    PAY = "pay"
    BOOK = "book"
    THEME = "theme"
    DONATE = "donate"


@dataclass
class Payment:
    telegram_id: int
    amount: int
    type: PaymentType
    id: Optional[int] = None
    product_id: Optional[int] = None
    created_at: Optional[int] = None  # Храним как timestamp (секунды с эпохи)


class PaymentClient(YDBClient):
    def __init__(self, endpoint: str = YDB_ENDPOINT, database: str = YDB_PATH, token: str = YDB_TOKEN):
        super().__init__(endpoint, database, token)
        self.table_name = "payments"
        self.table_schema = """
            CREATE TABLE `payments` (
                `id` Uint64 NOT NULL,
                `telegram_id` Uint64 NOT NULL,
                `product_id` Uint64?,
                `amount` Uint32 NOT NULL,
                `type` Utf8 NOT NULL,
                `created_at` Uint64 NOT NULL,
                PRIMARY KEY (`id`)
            )
        """
    
    async def create_payments_table(self):
        """
        Создание таблицы payments
        """
        await self.create_table(self.table_name, self.table_schema)
    
    async def insert_payment(self, payment: Payment) -> Payment:
        """
        Вставка нового платежа с автогенерацией ID
        """
        # Генерируем ID как timestamp в микросекундах для уникальности
        if payment.id is None:
            payment.id = int(datetime.now(timezone.utc).timestamp() * 1000000)
        
        if payment.created_at is None:
            payment.created_at = int(datetime.now(timezone.utc).timestamp())
        
        await self.execute_query(
            """
            DECLARE $id AS Uint64;
            DECLARE $telegram_id AS Uint64;
            DECLARE $product_id AS Uint64?;
            DECLARE $amount AS Uint32;
            DECLARE $type AS Utf8;
            DECLARE $created_at AS Uint64;

            INSERT INTO payments (id, telegram_id, product_id, amount, type, created_at)
            VALUES ($id, $telegram_id, $product_id, $amount, $type, $created_at);
            """,
            self._to_params(payment)
        )
        return payment

    async def delete_payment(self, payment_id: int) -> None:
        """
        Удаление платежа по ID
        """
        await self.execute_query(
            """
            DECLARE $id AS Uint64;
            DELETE FROM payments WHERE id = $id;
            """,
            {"$id": (payment_id, ydb.PrimitiveType.Uint64)}
        )

    # --- helpers ---
    def _row_to_payment(self, row) -> Payment:
        return Payment(
            id=row["id"],
            telegram_id=row["telegram_id"],
            product_id=row.get("product_id"),
            amount=row["amount"],
            type=row["type"],
            created_at=row["created_at"],
        )
    
    @staticmethod
    def timestamp_to_datetime(timestamp: int) -> datetime:
        """Конвертация timestamp в datetime объект"""
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
    
    @staticmethod
    def datetime_to_timestamp(dt: datetime) -> int:
        """Конвертация datetime в timestamp"""
        return int(dt.timestamp())

    def _to_params(self, payment: Payment) -> dict:
        return {
            "$id": (payment.id, ydb.PrimitiveType.Uint64),
            "$telegram_id": (payment.telegram_id, ydb.PrimitiveType.Uint64),  
            "$product_id": (payment.product_id, ydb.OptionalType(ydb.PrimitiveType.Uint64)),  
            "$amount": (payment.amount, ydb.PrimitiveType.Uint32),
            "$type": (payment.type, ydb.PrimitiveType.Utf8),
            "$created_at": (payment.created_at, ydb.PrimitiveType.Uint64),
        }


# ------------------------------------------------------------------ ВОПРОСЫ --------------------------------------------------

class QuestionsTables(str, Enum):
    RU = "questions_ru"
    KZ = "questions_kz"


@dataclass
class Question:
    id: int
    question: str
    options: List[str]
    correct_option_id: int
    explanation: Optional[str] = None
    image: Optional[str] = None
    image_dark: Optional[str] = None


class QuestionClient(YDBClient):
    def __init__(self, table_name: QuestionsTables, endpoint: str = YDB_ENDPOINT, database: str = YDB_PATH, token: str = YDB_TOKEN):
        super().__init__(endpoint, database, token)
        self.table_name = table_name.value
        self.table_schema = f"""
            CREATE TABLE `{self.table_name}` (
                `id` Uint32 NOT NULL,
                `question` Utf8 NOT NULL,
                `options` Json NOT NULL,
                `correct_option_id` Uint32 NOT NULL,
                `explanation` Utf8,
                `image` Utf8,
                `image_dark` Utf8,
                PRIMARY KEY (`id`)
            )
        """
    
    async def create_questions_table(self):
        """Создание таблицы questions"""
        await self.create_table(self.table_name, self.table_schema)
        return self.table_name
    
    async def insert_question(self, questions: Question):
        """Вставка или обновление вопроса (UPSERT) и возврат объекта Questions"""

        await self.execute_query(
            f"""
            DECLARE $id AS Uint32;
            DECLARE $question AS Utf8;
            DECLARE $options AS Json;
            DECLARE $correct_option_id AS Uint32;
            DECLARE $explanation AS Utf8?;
            DECLARE $image AS Utf8?;
            DECLARE $image_dark AS Utf8?;

            UPSERT INTO `{self.table_name}` (
                id, question, options, correct_option_id, explanation, image, image_dark
            ) VALUES (
                $id, $question, $options, $correct_option_id, $explanation, $image, $image_dark
            );
            """,
            self._to_params(questions)
        )

    async def get_question_by_id(self, id: int) -> Optional[Question]:
        """Получение вопроса по id"""
        result = await self.execute_query(
            f"""
            DECLARE $id AS Uint32;

            SELECT id, question, options, correct_option_id, explanation, image, image_dark
            FROM `{self.table_name}`
            WHERE id = $id;
            """,
            {"$id": (id, ydb.PrimitiveType.Uint32)}
        )

        rows = result[0].rows
        if not rows:
            return None

        return self._row_to_question(rows[0])

    async def update_question(self, questions: Question) -> Question:
        """Обновление данных вопроса по объекту Question"""
        await self.execute_query(
            f"""
            DECLARE $id AS Uint32;
            DECLARE $question AS Utf8;
            DECLARE $options AS Json;
            DECLARE $correct_option_id AS Uint32;
            DECLARE $explanation AS Utf8?;
            DECLARE $image AS Utf8?;
            DECLARE $image_dark AS Utf8?;

            UPDATE `{self.table_name}` SET
                question = $question,
                options = $options,
                correct_option_id = $correct_option_id,
                explanation = $explanation,
                image = $image,
                image_dark = $image_dark
            WHERE id = $id;
            """,
            self._to_params(questions)
        )
        return await self.get_question_by_id(questions.id)
    
    async def update_question_fields(self, question_id: int, **fields: Any) -> bool:
        if not fields:
            return False

        allowed_fields = ['question', 'options', 'correct_option_id', 'explanation', 'image', 'image_dark']
        question_fields = {k: v for k, v in fields.items() if k in allowed_fields}

        if not question_fields:
            return False

        FIELD_TYPES = {
            "question":          ydb.PrimitiveType.Utf8,
            "options":           ydb.PrimitiveType.Json,
            "correct_option_id": ydb.PrimitiveType.Uint32,
            "explanation":       ydb.OptionalType(ydb.PrimitiveType.Utf8),
            "image":             ydb.OptionalType(ydb.PrimitiveType.Utf8),
            "image_dark":        ydb.OptionalType(ydb.PrimitiveType.Utf8)
        }

        TYPE_DECLARE = {
            "question":          "Utf8",
            "options":           "Json",
            "correct_option_id": "Uint32",
            "explanation":       "Utf8?",
            "image":             "Utf8?",
            "image_dark":        "Utf8?"
        }

        set_clauses = []
        params = {"$id": (question_id, ydb.PrimitiveType.Uint32)}
        declare_lines = ["DECLARE $id AS Uint32;"]

        for field, value in question_fields.items():
            param_name = f"${field}"
            set_clauses.append(f"{field} = {param_name}")
            params[param_name] = (value, FIELD_TYPES[field])
            declare_lines.append(f"DECLARE {param_name} AS {TYPE_DECLARE[field]};")

        query = f"""
            {' '.join(declare_lines)}

            UPDATE `{self.table_name}`
            SET {', '.join(set_clauses)}
            WHERE id = $id;
        """

        await self.execute_query(query, params)
        return True

    async def delete_question(self, id: int) -> None:
        """Удаление вопроса"""
        await self.execute_query(
            f"""
            DECLARE $id AS Uint32;
            DELETE FROM `{self.table_name}` WHERE id = $id;
            """,
            {"$id": (id, ydb.PrimitiveType.Uint32)}
        )
    
    async def get_questions_count(self) -> int:
        result = await self.execute_query(
            f"""
            SELECT COUNT(*) AS count
            FROM `{self.table_name}`;
            """
        )
        return result[0].rows[0]["count"]

    def _row_to_question(self, row) -> Question:
        options = row.get("options")
        if isinstance(options, str):
            options = json.loads(options)
            
        return Question(
            id=row["id"],
            question=row.get("question"),
            options=options,
            correct_option_id=row.get("correct_option_id"),
            explanation=row.get("explanation"),
            image=row.get("image"),
            image_dark=row.get("image_dark")
        )

    def _to_params(self, questions: Question) -> dict:
        return {
            "$id": (questions.id, ydb.PrimitiveType.Uint32),
            "$question": (questions.question, ydb.PrimitiveType.Utf8),
            "$options": (json.dumps(questions.options, ensure_ascii=False), ydb.PrimitiveType.Json),
            "$correct_option_id": (questions.correct_option_id, ydb.PrimitiveType.Uint32),
            "$explanation": (questions.explanation, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$image": (questions.image, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$image_dark": (questions.image_dark, ydb.OptionalType(ydb.PrimitiveType.Utf8))
        }


# --------------------------------------------------------- СОЗДАНИЕ ТАБЛИЦ -------------------------------------------------------


async def create_tables_on_ydb():
    # Создание всех таблиц в базе
    # async with UserClient() as client:
    #     await client.create_users_table()
    #     print("Table 'USERS' created successfully!")

    async with PaymentClient() as client:
        await client.create_payments_table()
        print("Table 'PAYMENTS' created successfully!")

    # async with QuestionClient(QuestionsTables.RU) as client:
    #     table_name = await client.create_questions_table()
    #     print(f"Table '{table_name}' created successfully!")


# --------------------------------------------------------- ДОБАВЛЕНИЕ СТОЛБЦОВ В ТАБЛИЦУ -------------------------------------------------------

async def migrate():
    async with QuestionClient(QuestionsTables.RU) as client:
        await client.execute_query(
            "ALTER TABLE `questions_ru` ADD COLUMN `image_dark` Utf8;"
        )
        print("Миграция выполнена")


# --------------------------------------------------------- ЗАПУСК -------------------------------------------------------


if __name__ == "__main__":
    asyncio.run(create_tables_on_ydb())
