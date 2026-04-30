import json
import asyncio
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ydb_functions import add_new_question, Question, QuestionsTables
from ydb_logic import QuestionClient


async def load_questions_async(file_path: str, table: QuestionsTables) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    BATCH_SIZE = 5
    success, failed = 0, []

    async with QuestionClient(table) as client:
        for batch_start in range(0, len(data), BATCH_SIZE):
            batch = data[batch_start : batch_start + BATCH_SIZE]

            tasks = [
                client.insert_question(Question(
                    id=item["id"],
                    image=item.get("image"),
                    question=item["question"],
                    options=item["options"],
                    correct_option_id=item["correct_option_id"],
                    explanation=item.get("explanation"),
                ))
                for item in batch
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    failed.append((batch[i]["id"], result))
                else:
                    success += 1

            print(f"📦 Загружено {min(batch_start + BATCH_SIZE, len(data))}/{len(data)}")

    print(f"\n✅ Успешно добавлено: {success}/{len(data)}")
    if failed:
        print(f"❌ Ошибки ({len(failed)}):")
        for qid, err in failed:
            print(f"  Вопрос ID {qid}: {err}")


# использование
if __name__ == "__main__":
    asyncio.run(load_questions_async("parsers/questions.json", QuestionsTables.RU))

