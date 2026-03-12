from tts import speak
from speech import take_command
from modes.tom_mode import run_tom_mode
from modes.jerry_mode import run_jerry_mode
from logger_config import logger


def main_assistant():
    logger.info("Голосовий цикл асистента запущено", extra={'context': 'VoiceLoop'})
    speak("Асистент Том і Джері активовано. Скажіть 'Том' або 'Джері'.")

    while True:
        query = take_command(timeout=5, phrase_time_limit=5)
        if query == "none":
            continue

        if any(x in query for x in ["том", "тома", "тон", "дом", "там", "дім", "томас"]):
            logger.info("Активовано режим: Том", extra={'context': 'ModeSwitch'})
            run_tom_mode()
            speak("Виберіть режим: Том або Джері.")

        elif any(x in query for x in ["джері", "джорі", "жері", "джеррі"]):
            logger.info("Активовано режим: Джері", extra={'context': 'ModeSwitch'})
            run_jerry_mode()
            speak("Виберіть режим: Том або Джері.")

        elif any(x in query for x in ["вихід", "зупинити", "стоп", "до побачення"]):
            logger.info("Користувач ініціював вихід з програми", extra={'context': 'AppShutdown'})
            speak("До побачення! Асистент завершує роботу.")
            break


if __name__ == "__main__":
    logger.info("Програму Tom and Jerry успішно запущено", extra={'context': 'AppStartup'})
    try:
        main_assistant()
    except KeyboardInterrupt:
        logger.info("Програму примусово зупинено (Ctrl+C)", extra={'context': 'AppShutdown'})
    except Exception as e:
        logger.critical(f"Критичний збій у головному циклі: {e}", exc_info=True, extra={'context': 'AppCrash'})