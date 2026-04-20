from pathlib import Path
import json


def parse_question(file_path: Path):
    with file_path.open("r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    questions = []
    errors_count: int = 0
    i = 0
    n = len(lines)

    while i < n:
        image = lines[i]
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

            if line.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                break

            answers.append(line)
            i += 1

        comment = None
        if i < n:
            line = lines[i]
            if not line.startswith("#") and not line.lower().endswith(
                (".jpg", ".jpeg", ".png", ".webp")
            ):
                comment = line
                i += 1

        # ── Validation ──────────────────────────────────────────────
        if len(question) > 1300:
            print(
                f"'question' exceeds 1300 chars ({len(question)}) "
                f"in file: {file_path.name}"
            )
            errors_count += 1

        if not (2 <= len(answers) <= 10):
            print(
                f"'options' count is {len(answers)} (must be 2–10) "
                f"in file: {file_path.name}"
            )
            errors_count += 1

        for idx, option in enumerate(answers, start=1):
            if len(option) > 100:
                print(
                    f"option #{idx} exceeds 100 chars ({len(option)}) "
                    f"in file: {file_path.name}"
                )
                errors_count += 1

        if comment is not None and len(comment) > 200:
            print(
                f"'explanation' exceeds 200 chars ({len(comment)}) "
                f"in file: {file_path.name.split('_utf8.txt')[0]}"
            )
            errors_count += 1

        # ────────────────────────────────────────────────────────────

        questions.append({
            "image": image,
            "question": question,
            "options": answers,
            "correct_option_ids": correct_index,
            "explanation": comment
        })

    return questions, errors_count


def parse_directory(directory: str, ):
    directory = Path(directory)

    all_questions = []
    errors_count = 0

    for file_path in directory.rglob("*.txt"):
        parsed, errors = parse_question(file_path)
        all_questions.extend(parsed)
        errors_count += errors

    return all_questions, errors_count


if __name__ == "__main__":
    input_dir = r"C:\Users\Astana\Desktop\MyPrograms\pdd_bot_3\data\questions"
    output_file = "questions.json"

    result, errors_count = parse_directory(input_dir)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Число ошибок: {errors_count}")
    print(f"Спарсено: {len(result)} вопросов")
    