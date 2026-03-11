import speech_recognition as sr
r = sr.Recognizer()
r.energy_threshold = 4000
r.pause_threshold = 0.8
r.dynamic_energy_threshold = True


def take_command(timeout=5, phrase_time_limit=10) -> str:
    """
    Слухає мікрофон та розпізнає мову користувача.

    Використовує Google Speech Recognition для перетворення голосу в текст
    українською мовою (uk-UA). Автоматично фільтрує фоновий шум.

    Args:
        timeout (int, optional): Максимальний час очікування початку фрази в секундах. За замовчуванням 5.
        phrase_time_limit (int, optional): Максимальна тривалість самої фрази в секундах. За замовчуванням 5.

    Returns:
        str: Розпізнаний текст у нижньому регістрі. Повертає "none", якщо голос
             не почуто або не розпізнано.
    """
    try:
        with sr.Microphone() as source:
            print("\n🎤 Говоріть зараз...")

            audio = r.listen(source, timeout=timeout,
                             phrase_time_limit=phrase_time_limit)
            print("🧠 Розпізнавання...")

            query = r.recognize_google(audio, language='uk-UA')
            print(f"👤 Ви сказали: '{query}'")
            return query.lower()

    except sr.WaitTimeoutError:
        print("⌛ Не почуто голосу.")
        return "none"
    except sr.UnknownValueError:
        print("❌ Не вдалося розпізнати голос.")
        return "none"
    except sr.RequestError as e:
        print(f"❌ Проблема з Google Speech Recognition: {e}")
        return "none"
    except Exception as e:
        print(f"❌ Помилка мікрофона: {e}")
        return "none"
