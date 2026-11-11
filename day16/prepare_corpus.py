from pathlib import Path
def clean_text(text):
    lines = text.splitlines()
    clean_lines = []
    for line in lines:
        line = line.strip()
        if line != "":
            clean_lines.append(line)
    return "\n".join(clean_lines)
corpus_dir = Path("corpus")
if not corpus_dir.exists():
    corpus_dir = Path(".")
cleaned_dir = Path("cleaned")
cleaned_dir.mkdir(exist_ok=True)
files = list(corpus_dir.glob("*.txt"))
print("Найдено файлов:", len(files))
documents = []
for file_path in files:
    if file_path.name.startswith("final_") or file_path.name.startswith("prepare_"):
        continue
    text = file_path.read_text(encoding="utf-8")
    text = clean_text(text)
    if text == "":
        print("Пропущен пустой файл:", file_path.name)
        continue
    if len(text) < 50:
        print("Предупреждение короткий документ:", file_path.name)
    documents.append({
        "source": file_path.name,
        "text": text
    })
    output_path = cleaned_dir / file_path.name
    output_path.write_text(text, encoding="utf-8")
print()
print("Документов после очистки:", len(documents))
total = 0
for document in documents:
    n = len(document["text"])
    total = total + n
    print(document["source"], "-", n, "символов")
print("Всего символов:", total)