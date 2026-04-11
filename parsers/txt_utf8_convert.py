from pathlib import Path

def convert_folder(folder_path: str):
    folder = Path(folder_path)

    for file_path in folder.rglob("*.txt"):
        try:
            raw = file_path.read_bytes()
            text = raw.decode("cp1251", errors="ignore")

            new_file = file_path.with_name(file_path.stem + "_utf8.txt")
            new_file.write_text(text, encoding="utf-8")

            file_path.unlink()

            print(f"OK: {file_path.name} -> {new_file.name}")

        except Exception as e:
            print(f"ERROR: {file_path} -> {e}")


if __name__ == "__main__":
    convert_folder(r"C:\Users\Astana\Desktop\Client\Болат\Программа пдд 1.10 (2)\Программа пдд 1.10\questions")