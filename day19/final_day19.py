from pathlib import Path
import json
chunks = [
    {"source": "zapros.txt", "chunk_id": 0, "text": "Запрос пишут когда нужно получить сведения. В начале указывают обращение."},
    {"source": "zapros.txt", "chunk_id": 1, "text": "Дальше ясно пишут что именно нужно. В конце просят ответить в удобный срок."},
    {"source": "otvet.txt", "chunk_id": 0, "text": "Ответ должен быть по делу. Сначала ссылаются на полученный запрос."},
    {"source": "otvet.txt", "chunk_id": 1, "text": "Потом дают нужную информацию. Лучше коротко и понятно."},
    {"source": "pretenziya.txt", "chunk_id": 0, "text": "Претензию пишут когда есть проблема. Описывают факт без грубых слов."},
    {"source": "pretenziya.txt", "chunk_id": 1, "text": "Указывают что ожидают в ответ. Тон вежливый но твёрдый."},
    {"source": "blagodarnost.txt", "chunk_id": 0, "text": "Благодарность нужна чтобы отметить помощь. Пишут коротко и искренне."},
    {"source": "napominanie.txt", "chunk_id": 0, "text": "Напоминание пишут если срок подходит. Мягко напоминают о договорённости."},
    {"source": "napominanie.txt", "chunk_id": 1, "text": "Указывают дату или срок. Просят подтвердить выполнение."},
    {"source": "struktura_pisma.txt", "chunk_id": 0, "text": "Структура письма: обращение основная часть завершение и подпись."},
    {"source": "struktura_pisma.txt", "chunk_id": 1, "text": "В обращении используют имя или должность. В основной части пишут суть."},
]
USE_MODEL = False
try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    USE_MODEL = True
    print("Модель загружена")
except Exception as e:
    print("Модель недоступна, использую простой поиск по словам")
    print("Причина:", type(e).__name__)
def simple_score(query, text):
    q = set(query.lower().split())
    t = set(text.lower().split())
    if not q:
        return 0.0
    return len(q & t) / len(q)
def find_best(query):
    if USE_MODEL:
        texts = [c["text"] for c in chunks]
        chunk_embeddings = model.encode(texts)
        query_embedding = model.encode(query)
        scores = model.similarity(query_embedding, chunk_embeddings)[0].tolist()
    else:
        scores = [simple_score(query, c["text"]) for c in chunks]

    results = []
    for i in range(len(chunks)):
        results.append({"index": i, "score": scores[i]})
    results = sorted(results, key=lambda item: item["score"], reverse=True)

    best = results[0]
    best_chunk = chunks[best["index"]]
    return best_chunk, best["score"], results[:3]
print("Чанков:", len(chunks))
print()
test_questions = [
    "Как написать запрос информации",
    "Как оформить претензию",
    "Что писать в напоминании о сроке",
]
for query in test_questions:
    print("Вопрос:", query)
    best_chunk, best_score, top3 = find_best(query)
    print("Источник:", best_chunk["source"])
    print("Чанк:", best_chunk["chunk_id"])
    print("Текст:", best_chunk["text"])
    print("Сходство:", round(float(best_score), 4))
    print("Top-3:")
    for r in top3:
        c = chunks[r["index"]]
        print(" ", round(float(r["score"]), 4), c["source"], c["text"][:50])
    print("---")
print()
query = input("Ваш вопрос (или Enter чтобы пропустить): ").strip()
if query:
    best_chunk, best_score, top3 = find_best(query)
    if best_score < 0.1 and not USE_MODEL:
        print("Подходящий фрагмент не найден")
    else:
        print("Источник:", best_chunk["source"])
        print("Чанк:", best_chunk["chunk_id"])
        print("Текст:", best_chunk["text"])
        print("Сходство:", round(float(best_score), 4))
out = []
for c in chunks:
    item = {"source": c["source"], "chunk_id": c["chunk_id"], "text": c["text"]}
    out.append(item)
with open("chunks_meta.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print()
print("Метаданные сохранены в chunks_meta.json")