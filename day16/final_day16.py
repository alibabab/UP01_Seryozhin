from pathlib import Path
def clean_text(text):
    lines = text.splitlines()
    clean_lines = []
    for line in lines:
        line = line.strip()
        if line != "":
            clean_lines.append(line)
    return "\n".join(clean_lines)
corpus_dir = Path(".")
cleaned_dir = Path("cleaned")
cleaned_dir.mkdir(exist_ok=True)
files = list(corpus_dir.glob("*.txt"))
documents = []
for file_path in files:
    if file_path.name.startswith("final_") or file_path.name.startswith("prepare_") or file_path.name.startswith("report"):
        continue
    text = file_path.read_text(encoding="utf-8")
    text = clean_text(text)
    if text == "":
        print("Пропущен пустой файл:", file_path.name)
        continue
    documents.append({
        "source": file_path.name,
        "text": text
    })
    output_path = cleaned_dir / file_path.name
    output_path.write_text(text, encoding="utf-8")
print("Документов:", len(documents))
total_chars = 0
longest_name = ""
longest_len = 0
shortest_name = ""
shortest_len = 10**9
for document in documents:
    chars = len(document["text"])
    total_chars = total_chars + chars
    print(document["source"], chars)
    if chars < 50:
        print("Предупреждение короткий документ", document["source"])
    if chars > longest_len:
        longest_len = chars
        longest_name = document["source"]
    if chars < shortest_len:
        shortest_len = chars
        shortest_name = document["source"]
print("Всего символов:", total_chars)
print("Самый длинный:", longest_name, longest_len)
print("Самый короткий:", shortest_name, shortest_len)
if len(documents) > 0:
    avg = total_chars / len(documents)
    print("Средняя длина:", round(avg, 1))