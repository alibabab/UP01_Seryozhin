from pathlib import Path
import csv
def split_with_overlap(text, chunk_size, overlap, minimum_length=30):
    if chunk_size <= 0:
        raise ValueError("chunk_size должен быть больше 0")
    if overlap < 0:
        raise ValueError("overlap не может быть отрицательным")
    if overlap >= chunk_size:
        raise ValueError("overlap должен быть меньше chunk_size")
    chunks = []
    step = chunk_size - overlap
    for start in range(0, len(text), step):
        chunk = text[start:start + chunk_size].strip()
        if len(chunk) >= minimum_length:
            chunks.append(chunk)
    return chunks
source_dir = Path("normalized")
chunks_dir = Path("chunks")
chunks_dir.mkdir(exist_ok=True)
files = list(source_dir.glob("*.txt"))
if not files:
    source_dir = Path(".")
    files = [f for f in source_dir.glob("*.txt") if f.name != "final_day18.py"]
all_chunks = []
chunk_size = 200
overla = 40
for file_path in files:
    text = file_path.read_text(encoding="utf-8")
    chunks = split_with_overlap(text, chunk_size, overlap)
    for chunk_id, chunk in enumerate(chunks):
        data = {
            "source": file_path.name,
            "chunk_id": chunk_id,
            "text": chunk,
            "length": len(chunk),
        }
        all_chunks.append(data)
        source_stem = file_path.stem
        filename = f"{source_stem}_chunk_{chunk_id}.txt"
        (chunks_dir / filename).write_text(chunk, encoding="utf-8")
with open("chunks_summary.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["source", "chunk_id", "length"])
    for chunk in all_chunks:
        writer.writerow([chunk["source"], chunk["chunk_id"], chunk["length"]])
print("Документов:", len(files))
print("Всего чанков:", len(all_chunks))
if all_chunks:
    total = sum(c["length"] for c in all_chunks)
    print("Средняя длина:", round(total / len(all_chunks), 1))