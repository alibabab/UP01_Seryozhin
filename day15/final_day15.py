import os
import logging
from dotenv import load_dotenv
from gigachat import GigaChat
from pydantic import BaseModel, Field
for var in ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy", "SOCKS_PROXY", "socks_proxy"]:
    os.environ[var] = ""
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)
class AnalysisResult(BaseModel):
    topic: str = Field(description="Тема сообщения")
    category: str = Field(description="Категория: запрос ответ претензия благодарность напоминание")
    difficulty: str = Field(description="Сложность составления: низкая средняя высокая")
    summary: str = Field(description="Краткое содержание")
logging.info("Старт программы")
load_dotenv()
key = os.getenv("GIGACHAT_CREDENTIALS")
scope = os.getenv("GIGACHAT_SCOPE")
print("=== Анализатор деловой переписки ===")
text = input("Введите текст или описание ситуации: ").strip()
if text == "":
    print("Сообщение не должно быть пустым")
    logging.warning("Получен пустой ввод")
else:
    logging.info("Промпт сформирован")
    try:
        logging.info("Запрос отправлен")
        with GigaChat(
            credentials=key,
            scope=scope,
            model="GigaChat-2",
            ca_bundle_file="certs/russian_trusted_root_ca_pem.crt",
            timeout=60,
        ) as client:
            completion, parsed = client.chat_parse(
                "Проанализируй ситуацию деловой переписки и заполни поля. Текст: " + text,
                response_format=AnalysisResult,
                strict=True,
            )
            print()
            print("Тема:", parsed.topic)
            print("Категория:", parsed.category)
            print("Сложность:", parsed.difficulty)
            print("Кратко:", parsed.summary)
            logging.info("Ответ успешно получен")

            with open("result.txt", "w", encoding="utf-8") as f:
                f.write("Тема: " + parsed.topic + "\n")
                f.write("Категория: " + parsed.category + "\n")
                f.write("Сложность: " + parsed.difficulty + "\n")
                f.write("Кратко: " + parsed.summary + "\n")
            print()
            print("Результат сохранён в result.txt")
    except Exception as error:
        print("Не удалось выполнить запрос. Проверьте ключ и подключение.")
        logging.error("Ошибка: %s", error)