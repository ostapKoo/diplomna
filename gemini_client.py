import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

model = None

if not API_KEY:
    print("❌ Помилка: GEMINI_API_KEY не знайдено. Створіть .env файл.")
else:
    try:
        genai.configure(api_key=API_KEY)
        MODEL_NAME = "gemini-2.5-flash"

        model = genai.GenerativeModel(
            MODEL_NAME,
            system_instruction="Відповідай українською мовою, коротко і по суті."
        )
        print(f"✅ Gemini ініціалізовано ({MODEL_NAME})")
    except Exception as e:
        print(f"❌ Помилка підключення до Gemini: {e}")


def ask_gemini(prompt: str) -> str:
    if not model:
        return "Gemini недоступний. Перевірте API ключ в .env файлі."

    print(f"🧠 Запит до Джері: {prompt}")
    try:
        chat = model.start_chat(history=[])
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Помилка Gemini: {e}")
        return "❌ Виникла помилка під час відповіді."
