from tts import speak
from speech import take_command
from gemini_client import ask_gemini


def run_jerry_mode():
    speak("Режим Джері активовано. Слухаю ваше запитання.")

    while True:
        query = take_command(timeout=10, phrase_time_limit=15)
        if query == "none":
            continue

        if any(x in query for x in ["назад", "головне меню", "вихід", "том"]):
            speak("Повертаюся до головного меню.")
            break

        answer = ask_gemini(query)


        speak(answer[:400])