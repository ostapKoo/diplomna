import utils
from tts import speak
from speech import take_command
import re


def run_tom_mode():
    """
    Активує головний цикл голосового помічника у режимі "Том" (Системний адміністратор).

    Безперервно очікує на голосові команди від користувача. Якщо розпізнано команду
    виходу ("назад", "головне меню" тощо), цикл переривається і керування
    повертається до головного меню програми.
    Інші команди передаються у функцію execute_tom_command для виконання.
    """
    speak("Режим Тома активовано. Чекаю на ваші команди.")
    while True:
        command = take_command(timeout=5, phrase_time_limit=5)
        if command == "none":
            continue

        if any(word in command for word in ["вийди", "назад", "головне меню", "зупинись", "вийти"]):
            speak("Виходжу з режиму керування ПК.")
            break
        execute_tom_command(command)


def _parse_number_from_query(query):
    """
    Вилучає число з тексту команди (від 0 до 100).
    Збережено для проходження Unit-тестів!
    """
    words = query.split()
    for word in words:
        if word.isdigit():
            num = int(word)
            if 0 <= num <= 100:
                return num
    return None


def execute_tom_command(command):
    """
    Головна функція обробки голосових команд для Тома.
    Приймає розпізнаний текст (command) і викликає відповідну функцію з utils.
    """
    command = command.lower()

    if "грати" in command or "запусти гру" in command or "запустити гру" in command:
        games = utils.get_games_list()
        found_game = False

        for game_key in games:

            clean_game_name = game_key.replace("🎮 ", "").lower()
            if clean_game_name in command:
                utils.launch_game(game_key)
                found_game = True
                break

        if not found_game:
            speak("Яку саме гру запустити? Я не знайшов її у вашому списку.")
        return  # Завершуємо перевірки

    elif "повідомлення на екран" in command or "напиши на екрані" in command:
        if "повідомлення на екран" in command:
            text = command.split("повідомлення на екран", 1)[1].strip()
        else:
            text = command.split("напиши на екрані", 1)[1].strip()

        if text:
            utils.show_message_on_screen(text.capitalize())
        else:
            speak("Що саме мені написати на екрані?")
        return

    elif "нагадай через" in command or "нагадування через" in command:
        match = re.search(r'через\s+(\d+)\s+хвилин\w*\s+(.*)', command)

        if match:
            minutes = int(match.group(1))
            text = match.group(2).strip()

            if text:
                utils.set_reminder(minutes, text.capitalize())
            else:
                speak("Про що саме вам нагадати?")
        else:
            speak("Скажіть команду у форматі: нагадай через 5 хвилин і ваш текст.")
        return

    if "скріншот" in command:
        utils.take_screenshot("voice_screenshot.png")

    elif "статус" in command or "навантаження" in command:
        stats = utils.get_system_stats()
        speak(stats)

    elif "пауз" in command or "продовж" in command or "плей" in command:
        utils.media_play_pause()
        speak("Керую медіа.")

    elif "наступн" in command:
        utils.media_next()
        speak("Наступний трек.")

    elif "попередн" in command:
        utils.media_prev()
        speak("Попередній трек.")

    elif "заблокуй" in command or "блок" in command:
        utils.lock_pc()

    elif "перезавантаж" in command:
        utils.restart_pc()

    elif "вимкни комп" in command or "вимкнути комп" in command:
        utils.shutdown_pc()

    elif "скасуй" in command or "відміни" in command:
        utils.cancel_shutdown()

    elif "диспетчер" in command:
        utils.open_task_manager()

    elif "провідник" in command or "папк" in command:
        utils.open_explorer()

    elif "гучніст" in command or "гучність" in command:
        num = _parse_number_from_query(command)
        if num is not None:
            utils.set_master_volume(num)
        elif "збільш" in command:
            utils.change_volume(10)
        elif "зменш" in command:
            utils.change_volume(-10)
        else:
            speak("Скажіть рівень гучності від 0 до 100.")

    elif "звук" in command and ("вимкн" in command or "увімкн" in command):
        utils.toggle_mute()

    elif "яскравіст" in command or "яскравість" in command:
        num = _parse_number_from_query(command)
        if num is not None:
            utils.set_brightness(num)
        elif "збільш" in command:
            utils.change_brightness(10)
        elif "зменш" in command:
            utils.change_brightness(-10)
        else:
            speak("Скажіть рівень яскравості від 0 до 100.")

    elif "браузер" in command or "інтернет" in command:
        utils.open_browser()

    elif "блокнот" in command:
        utils.open_notepad()

    elif "калькулятор" in command:
        utils.open_calculator()

    elif "час" in command or "година" in command:
        utils.tell_time()

    elif "дат" in command or "сьогодні" in command:
        utils.tell_date()

    else:
        speak("Команда не розпізнана. Спробуйте сказати інакше.")
