import os
from dotenv import load_dotenv
from gigachat import GigaChat
from prompts import SYSTEM_PROMPT
from gigachat.models import ChatCompletionRequest, ChatMessage, ChatModelOptions
for var in ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy", "SOCKS_PROXY", "socks_proxy"]:
    os.environ[var] = ""
load_dotenv()
key = os.getenv("GIGACHAT_CREDENTIALS")
scope = os.getenv("GIGACHAT_SCOPE")
system_msg = ChatMessage(role="system", content=SYSTEM_PROMPT)
messages = [system_msg]
max_pairs = 
print("=== Помощник по деловой переписке ===")
print("Можно писать уточнения к предыдущему ответу")
print("Команды: выход | очистить | история")
print()
with open("chat_history.txt", "a", encoding="utf-8") as f:
    f.write("Новый запуск\n\n")
with GigaChat(
    credentials=key,
    scope=scope,
    model="GigaChat-2",
    ca_bundle_file="certs/russian_trusted_root_ca_pem.crt",
    timeout=60,
) as client:
    while True:
        text = input("Вы: ").strip()
        cmd = text.lower()
        if cmd == "выход":
            print("До свидания")
            break
        if text == "":
            print("Введите текст сообщения")
            continue
        if cmd == "очистить":
            messages = [system_msg]
            print("История текущего диалога очищена")
            with open("chat_history.txt", "a", encoding="utf-8") as f:
                f.write("История текущего диалога очищена\n\n")
            continue
        if cmd == "история":
            print("Сообщений в памяти:", len(messages))
            for m in messages:
                print("-", m.role)
            continue
        messages.append(ChatMessage(role="user", content=text))
        request = ChatCompletionRequest(
            model="GigaChat-2",
            messages=messages,
            model_options=ChatModelOptions(
                temperature=0.2,
                max_tokens=400,
            ),
        )
        response = client.chat.create(request)
        answer = response.messages[0].content[0].text
        print()
        print("Помощник:")
        print(answer)
        print()
        messages.append(ChatMessage(role="assistant", content=answer))
        limit = 1 + 2 * max_pairs
        if len(messages) > limit:
            rest = messages[1:]
            rest = rest[-(2 * max_pairs):]
            messages = [system_msg] + rest
        print("Сообщений в памяти:", len(messages))
        with open("chat_history.txt", "a", encoding="utf-8") as f:
            f.write("Пользователь: " + text + "\n")
            f.write("Помощник: " + answer + "\n\n")