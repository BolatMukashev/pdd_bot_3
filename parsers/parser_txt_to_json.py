from pathlib import Path
import json
from itertools import islice
from parser_get_tg_photo_id import get_photo_id


def parse_question(file_path: Path):
    with file_path.open("r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    questions = []
    errors_count: int = 0
    i = 0
    n = len(lines)

    while i < n:
        # картинка
        image = lines[i]
        dir = Path(r"C:\Users\Astana\Desktop\MyPrograms\pdd_bot_3\data\pictures")
        image_path = dir / image
        print(image_path)
        file_id = get_photo_id(image_path)
        i += 1

        if i >= n:
            break
        
        # вопрос
        question = lines[i]
        i += 1

        # ответы
        answers = []
        correct_index = None

        while i < n:
            line = lines[i]

            if line.startswith("#") and line[1:].isdigit():
                correct_index = int(line[1:]) - 1
                i += 1
                break

            if line.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                break

            answers.append(line.strip().rstrip("."))
            i += 1

        # комментарий
        comment = None
        if i < n:
            line = lines[i]
            if not line.startswith("#") and not line.lower().endswith(
                (".jpg", ".jpeg", ".png", ".webp")
            ):
                comment = line
                i += 1

        # ── Validation ──────────────────────────────────────────────
        if len(question) > 300:
            print(
                f"'question' превышение 300 символов ({len(question)}) "
                f"in file: {file_path.name}"
            )
            errors_count += 1

        if not (2 <= len(answers) <= 10):
            print(
                f"'options' количество {len(answers)} (должно быть 2–10) "
                f"in file: {file_path.name}"
            )
            errors_count += 1

        for idx, option in enumerate(answers, start=1):
            if len(option) > 100:
                print(
                    f"option #{idx} превышает 100 символов ({len(option)}) "
                    f"in file: {file_path.name}"
                )
                errors_count += 1

        if comment is not None and len(comment) > 200:
            print(
                f"'explanation' превышает 200 символов ({len(comment)}) "
                f"in file: {file_path.name}"
            )
            errors_count += 1

        # ────────────────────────────────────────────────────────────

        questions.append({
            "id": int(file_path.name.split('_utf8.txt')[0]),
            "image": file_id,
            "question": question,
            "options": answers,
            "correct_option_id": correct_index,
            "explanation": comment
        })

    return questions, errors_count


def parse_txt_files(directory: str, start: int, end: int):
    directory = Path(directory)

    all_questions = []
    errors_count = 0

    for file_path in islice(directory.rglob("*.txt"), start, end + 1):
        parsed, errors = parse_question(file_path)
        all_questions.extend(parsed)
        errors_count += errors

    return all_questions, errors_count


if __name__ == "__main__":
    input_dir = r"C:\Users\Astana\Desktop\MyPrograms\pdd_bot_3\data\questions"
    output_file = "parsers/questions.json"

    result, errors_count = parse_txt_files(input_dir, 1, 1019)

    # Читаем существующие данные, если файл есть
    existing = []
    if Path(output_file).exists():
        with open(output_file, "r", encoding="utf-8") as f:
            existing = json.load(f)

    # Объединяем, избегая дублей по id
    existing_ids = {q["id"] for q in existing}
    new_questions = [q for q in result if q["id"] not in existing_ids]
    combined = existing + new_questions

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)

    print(f"Число ошибок: {errors_count}")
    print(f"Новых вопросов добавлено: {len(new_questions)}")
    print(f"Всего вопросов в файле: {len(combined)}")
    