import os
from dotenv import load_dotenv
from gigachat import GigaChat
from prompts import SYSTEM_PROMPT
from gigachat.models import ChatCompletionRequest, ChatMessage, ChatModelOptions
load_dotenv()
key = os.getenv("GIGACHAT_CREDENTIALS")
scope = os.getenv("GIGACHAT_SCOPE")
print("=== Помощник по деловой переписке ===")
print()
situaciya = input("Ситуация (запрос, ответ, претензия, благодарность, напоминание): ").strip()
adresat = input("Кому пишем (руководитель, коллега, клиент, партнёр): ").strip()
cel = input("Цель сообщения (что нужно получить или сказать): ").strip()
print()
print("Формат ответа:")
print("1 - краткий")
print("2 - пошаговый")
format_vybor = input("Выберите 1 или 2: ").strip()
if situaciya == "" or adresat == "" or cel == "":
    print("Нужно заполнить ситуацию, адресата и цель. Запрос не отправлен.")
else:
    if format_vybor == "1":
        format_text = "Дай краткий ответ."
    elif format_vybor == "2":
        format_text = "Дай пошаговый ответ: сначала тон, потом письмо, потом пояснение."
    else:
        print("Нужно выбрать 1 или 2. Запрос не отправлен.")
        format_text = None
    if format_text is not None:
        user_prompt = f"""Составь деловое письмо.
Ситуация: {situaciya}
Адресат: {adresat}
Цель: {cel}
{format_text}
"""
        print()
        print("--- Собранный запрос ---")
        print(user_prompt)
        print("------------------------")
        print()
        print("Отправляем запрос...")
        request = ChatCompletionRequest(
            model="GigaChat-2",
            messages=[
                ChatMessage(
                    role="system",
                    content=SYSTEM_PROMPT,
                ),
                ChatMessage(
                    role="user",
                    content=user_prompt,
                ),
            ],
            model_options=ChatModelOptions(
                temperature=0.2,
                max_tokens=400,
            ),
        )
        with GigaChat(
            credentials=key,
            scope=scope,
            model="GigaChat-2",
            ca_bundle_file="certs/russian_trusted_root_ca_pem.crt",
            timeout=60,
        ) as client:
            response = client.chat.create(request)
        answer = response.messages[0].content[0].text
        print()
        print("Ответ:")
        print(answer)
        with open("last_prompt.txt", "w", encoding="utf-8") as f:
            f.write(user_prompt)
        with open("last_answer.txt", "w", encoding="utf-8") as f:
            f.write(answer)
        print()
        print("Промпт и ответ сохранены в last_prompt.txt и last_answer.txt")