import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from gigachat import GigaChat
from prompts import SYSTEM_PROMPT
from gigachat.models import ChatCompletionRequest, ChatMessage, ChatModelOptions
for var in ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy", "SOCKS_PROXY", "socks_proxy"]:
    os.environ[var] = ""
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)
load_dotenv()
key = os.getenv("GIGACHAT_CREDENTIALS")
scope = os.getenv("GIGACHAT_SCOPE")
if not key:
    print("Нет ключа. Создайте файл .env с GIGACHAT_CREDENTIALS")
    raise SystemExit(1)
_msg = ChatMessage(role="system", content=SYSTEM_PROMPT)
messages = [system_msg]
max_pairs = 3
corpus_dir = Path("corpus")
corpus_texts = []
if corpus_dir.exists():
    for p in corpus_dir.glob("*.txt"):
        t = p.read_text(encoding="utf-8").strip()
        if t:
            corpus_texts.append(p.name + ":\n" + t)
print("=== ИИ-агент: Деловая переписка ===")
print("Пишите запрос или уточнение к предыдущему ответу")
print("Команды: выход | очистить | история | справка")
print()
logging.info("Агент запущен")
with open("chat_history.txt", "a", encoding="utf-8") as f:
    f.write("Новый запуск\n\n")
cert = "certs/russian_trusted_root_ca_pem.crt"
client_kwargs = dict(
    credentials=key,
    scope=scope,
    model="GigaChat-2",
    timeout=60,
)
if Path(cert).exists():
    client_kwargs["ca_bundle_file"] = cert
with GigaChat(**client_kwargs) as client:
    while True:
        text = input("Вы: ").strip()
        cmd = text.lower()

        if cmd == "выход":
            print("До свидания")
            logging.info("Выход")
            break

        if text == "":
            print("Введите текст запроса")
            logging.warning("Пустой ввод")
            continue

        if cmd == "очистить":
            messages = [system_msg]
            print("История очищена")
            logging.info("История очищена")
            with open("chat_history.txt", "a", encoding="utf-8") as f:
                f.write("История текущего диалога очищена\n\n")
            continue

        if cmd == "история":
            print("Сообщений:", len(messages))
            for m in messages:
                print("-", m.role)
            continue

        if cmd == "справка":
            print("Примеры: составь письмо руководителю о сдаче отчёта")
            print("Команды: выход очистить история справка")
            continue
        user_content = text
        if corpus_texts and len(messages) <= 2:
            user_content = text + "\n\nСправка из базы:\n" + "\n\n".join(corpus_texts[:3])

        messages.append(ChatMessage(role="user", content=user_content))
        try:
            logging.info("Запрос отправлен")
            request = ChatCompletionRequest(
                model="GigaChat-2",
                messages=messages,
                model_options=ChatModelOptions(temperature=0.2, max_tokens=500),
            )
            response = client.chat.create(request)
            answer = response.messages[0].content[0].text
            print()
            print("Агент:")
            print(answer)
            print()
            logging.info("Ответ получен")
            messages.append(ChatMessage(role="assistant", content=answer))
            limit = 1 + 2 * max_pairs
            if len(messages) > limit:
                messages = [system_msg] + messages[1:][-(2 * max_pairs):]
            with open("chat_history.txt", "a", encoding="utf-8") as f:
                f.write("Пользователь: " + text + "\n")
                f.write("Агент: " + answer + "\n\n")
        except Exception as error:
            print("Не удалось получить ответ. Проверьте ключ и интернет.")
            logging.error("Ошибка API: %s", error)
            if messages and messages[-1].role == "user":
                messages.pop()