import json
import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ydb_functions import add_new_question, Question, QuestionsTables


def load_questions(file_path: str, table: QuestionsTables) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        new_question = Question(
            id=item["id"],
            image=item.get("image"),
            question=item["question"],
            options=item["options"],
            correct_option_id=item["correct_option_id"],
            explanation=item.get("explanation"),
        )
        asyncio.run(add_new_question(new_question, table))


# использование
if __name__ == "__main__":
    load_questions("parsers/questions.json", QuestionsTables.RU)

