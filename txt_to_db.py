from pathlib import Path
from itertools import islice
import json
from get_photo_id import get_photo_id
from  time import sleep
from ydb_functions import add_new_question, Question, QuestionsTables
import asyncio


def parse_questions(file_path: Path):
    with file_path.open("r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    questions = []
    i = 0
    n = len(lines)

    while i < n:
        image = lines[i]
        dir = Path(r"C:\Users\Astana\Desktop\MyPrograms\pdd_bot_3\data\pictures")
        image_path = dir / image
        print(image_path)
        file_id = get_photo_id(image_path)
        i += 1

        if i >= n:
            break

        question = lines[i]
        i += 1

        answers = []
        correct_index = None

        while i < n:
            line = lines[i]

            if line.startswith("#") and line[1:].isdigit():
                correct_index = int(line[1:]) - 1
                i += 1
                break

            # если вдруг новый файл/вопрос начинается с картинки
            if line.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                break

            clean_line = line.rstrip()

            if clean_line.endswith("."):
                clean_line = clean_line[:-1].rstrip()

            answers.append(clean_line)
            i += 1

        # optional comment
        comment = None
        if i < n:
            line = lines[i]
            if not line.startswith("#") and not line.lower().endswith(
                (".jpg", ".jpeg", ".png", ".webp")
            ):
                comment = line
                i += 1

        questions.append({
            "image": file_id,
            "question": question,
            "options": answers,
            "correct_option_ids": correct_index,
            "explanation": comment
        })

        new_question = Question(id=int(file_path.name.split('_utf8.txt')[0]),
                                question=question,
                                options=answers,
                                correct_option_id=correct_index,
                                image=file_id,
                                explanation=comment
                                )
        asyncio.run(add_new_question(new_question))

        sleep(1)

    return questions


def parse_directory(directory: str, start: int, end: int):
    directory = Path(directory)

    all_questions = []

    for file_path in islice(directory.rglob("*.txt"), start, end + 1):
        parsed = parse_questions(file_path)
        all_questions.extend(parsed)

    return all_questions


if __name__ == "__main__":
    input_dir = r"C:\Users\Astana\Desktop\MyPrograms\pdd_bot_3\data\questions"  # папка с txt файлами
    output_file = "questions.json"

    result = parse_directory(input_dir, 1, 50)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Parsed: {len(result)} questions")