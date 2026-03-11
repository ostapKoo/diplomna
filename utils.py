import os
import time
#from pathlib import Path
#import math
import ctypes
#import urllib.parse
import threading


from tts import speak
#from speech import take_command


volume_control = None
PYCAW_LOADED = False
SBC_LOADED = False
PYAUTOGUI_LOADED = False
PSUTIL_LOADED = False


try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_control = cast(interface, POINTER(IAudioEndpointVolume))
    print("✅ Модуль 'pycaw' завантажено.")
    PYCAW_LOADED = True
except Exception as e:
    print(f"❌ Помилка 'pycaw': {e}")
    PYCAW_LOADED = False


try:
    import screen_brightness_control as sbc

    print("✅ Модуль 'screen_brightness_control' завантажено.")
    SBC_LOADED = True
except Exception as e:
    print(f"❌ Помилка 'sbc': {e}")
    SBC_LOADED = False

try:
    import pyautogui

    print("✅ Модуль 'pyautogui' завантажено.")
    PYAUTOGUI_LOADED = True
except Exception as e:
    print(f"❌ Помилка 'pyautogui': {e}")
    PYAUTOGUI_LOADED = False

try:
    import psutil

    print("✅ Модуль 'psutil' завантажено.")
    PSUTIL_LOADED = True
except Exception as e:
    print(f"❌ Помилка 'psutil': {e}")
    PSUTIL_LOADED = False


def tell_time():
    now = time.strftime("%H годин %M хвилин")
    speak(f"Зараз {now}")


def tell_date():
    now = time.strftime("%d %B %Y року")
    speak(f"Сьогодні {now}")


def open_browser(url=""):
    if url:
        speak(f"Відкриваю {url.split('.')[0]}.")
        os.system(f"start chrome {url}")
    else:
        speak("Відкриваю браузер.")
        os.system("start chrome")


def open_calculator():
    speak("Запускаю калькулятор.")
    os.system("calc")


def open_notepad():
    speak("Відкриваю блокнот.")
    os.system("notepad")


def open_explorer():
    speak("Відкриваю провідник.")
    os.system("explorer")


def open_task_manager():
    speak("Відкриваю диспетчер завдань.")
    os.system("taskmgr")


def lock_pc():
    speak("Блокую комп'ютер.")
    os.system("rundll32.exe user32.dll,LockWorkStation")


def shutdown_pc():
    speak("Вимикаю комп’ютер через хвилину.")
    os.system("shutdown /s /t 60")


def restart_pc():
    speak("Перезавантажую комп'ютер через хвилину.")
    os.system("shutdown /r /t 60")


def cancel_shutdown():
    speak("Вимкнення скасовано.")
    os.system("shutdown /a")


def open_google(): open_browser("google.com")


def open_youtube(): open_browser("youtube.com")


def open_wikipedia(): open_browser("uk.wikipedia.org")


def get_system_stats():
    if not PSUTIL_LOADED:
        return "❌ Модуль psutil не завантажено."
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('C:').percent
    speak("Перевіряю стан системи.")
    return f"💻 Навантаження процесора: {cpu}%\n🧠 Використання ОЗП: {ram}%\n💾 Зайнято на диску C: {disk}%"


def take_screenshot(filename="screenshot.png"):
    if not PYAUTOGUI_LOADED:
        speak("Модуль для скріншотів недоступний.")
        return None
    pyautogui.screenshot(filename)
    speak("Скріншот зроблено.")
    return filename


def media_play_pause():
    if PYAUTOGUI_LOADED:
        pyautogui.press('playpause')


def media_next():
    if PYAUTOGUI_LOADED:
        pyautogui.press('nexttrack')


def media_prev():
    if PYAUTOGUI_LOADED:
        pyautogui.press('prevtrack')


def set_master_volume(level_percent: int):
    if PYCAW_LOADED and volume_control:
        if 0 <= level_percent <= 100:
            scalar_level = level_percent / 100.0
            volume_control.SetMasterVolumeLevelScalar(scalar_level, None)
            speak(f"Гучність встановлено на {level_percent} відсотків.")
    else:
        speak("Точне встановлення гучності недоступне. Використовуйте кнопки '+10%' або '-10%'.")


def change_volume(step_percent: int):
    if PYCAW_LOADED and volume_control:
        current_scalar = volume_control.GetMasterVolumeLevelScalar()
        current_percent = round(current_scalar * 100)
        new_percent = max(0, min(100, current_percent + step_percent))
        set_master_volume(new_percent)
    elif PYAUTOGUI_LOADED:
        presses = abs(step_percent) // 2
        if step_percent > 0:
            pyautogui.press('volumeup', presses=presses)
            speak("Гучність збільшено.")
        else:
            pyautogui.press('volumedown', presses=presses)
            speak("Гучність зменшено.")
    else:
        speak("Керування гучністю недоступне.")


def toggle_mute():
    if PYCAW_LOADED and volume_control:
        is_muted = volume_control.GetMute()
        volume_control.SetMute(not is_muted, None)
        speak("Звук увімкнено." if is_muted else "Звук вимкнено.")
    elif PYAUTOGUI_LOADED:
        pyautogui.press('volumemute')
        speak("Звук перемикнуто.")


def set_brightness(level_percent: int):
    if not SBC_LOADED:
        return
    if 0 <= level_percent <= 100:
        try:
            sbc.set_brightness(level_percent)
            speak(f"Яскравість {level_percent} відсотків.")
        except:
            pass


def change_brightness(step_percent: int):
    if not SBC_LOADED:
        return
    try:
        current = int(sbc.get_brightness(display=0)[0])
        new_percent = max(0, min(100, current + step_percent))
        set_brightness(new_percent)
    except:
        pass


GAMES = {
    "🎮 CS:GO 2": r"steam://rungameid/730",
    "🎮 GTA V ": r"steam://rungameid/271590",
    "🎮 R.E.P.O": r"steam://rungameid/3241660",
    "🎮 Відкрити Steam": r"C:\Program Files (x86)\Steam\steam.exe"
}


def get_games_list():
    return list(GAMES.keys())


def launch_game(game_name):
    """Запускає гру зі словника"""
    path = GAMES.get(game_name)
    if path:
        speak(f"Запускаю {game_name.replace('🎮 ', '')}")
        try:
            os.startfile(path)
            return True
        except Exception as e:
            print(f"Помилка запуску: {e}")
            return False
    return False


def _show_popup(text):
    ctypes.windll.user32.MessageBoxW(
        0, text, "Повідомлення з Телеграм 💬", 0x40000 | 0x40)


def show_message_on_screen(text):
    speak("Вам нове повідомлення на екрані.")
    threading.Thread(target=_show_popup, args=(text,), daemon=True).start()


def _reminder_popup(text):
    ctypes.windll.user32.MessageBoxW(0, text, "⏰ Нагадування!", 0x40000 | 0x30)


def set_reminder(minutes, text):
    """Встановлює таймер у фоні"""

    def reminder_task():
        speak(f"Увага! Спрацювало нагадування: {text}")
        _reminder_popup(text)

    threading.Timer(minutes * 60.0, reminder_task).start()
    speak(f"Таймер на {minutes} хвилин встановлено.")


def _flash_and_speak(text):
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    root.configure(bg='red')

    def toggle_color(count):
        if count > 0:
            current_bg = root.cget("bg")
            next_bg = "yellow" if current_bg == "red" else "red"
            root.configure(bg=next_bg)
            root.after(300, toggle_color, count - 1)
        else:
            root.destroy()
            speak(f"Увага! Нагадування: {text}")

    toggle_color(12)
    root.mainloop()


def set_reminder(minutes, text):
    """Встановлює таймер у фоні"""

    def reminder_task():
        _flash_and_speak(text)

    threading.Timer(minutes * 60.0, reminder_task).start()
    speak(f"Таймер на {minutes} хвилин встановлено.")


def write_note(text):
    """Зберігає текст у файл notes.txt із вказанням часу"""
    try:
        with open("notes.txt", "a", encoding="utf-8") as file:
            timestamp = time.strftime("%d.%m.%Y %H:%M")
            file.write(f"[{timestamp}] {text}\n")
        speak("Нотатку успішно збережено.")
    except Exception as e:
        print(f"Помилка збереження нотатки: {e}")
        speak("Не вдалося зберегти нотатку.")


def get_top_processes():
    """Повертає топ-15 процесів, що споживають найбільше пам'яті"""
    if not PSUTIL_LOADED:
        return "❌ Модуль psutil не завантажено."

    processes = []
    for proc in psutil.process_iter(['name', 'memory_percent']):
        try:
            if proc.info['name']:
                processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    processes = sorted(
        processes, key=lambda p: p['memory_percent'] if p['memory_percent'] else 0, reverse=True)

    text = "💻 Топ-15 процесів (ОЗП):\n\n"
    seen_names = set()
    count = 0
    for p in processes:
        name = p['name']
        if name not in seen_names:
            mem = round(p['memory_percent'], 1) if p['memory_percent'] else 0
            text += f"▪️ `{name}` — {mem}%\n"
            seen_names.add(name)
            count += 1
        if count >= 15:
            break

    return text


def kill_process(process_name):
    """Зупиняє процес за його назвою (наприклад: chrome.exe)"""
    if not PSUTIL_LOADED:
        return False
    try:
        process_name = process_name.strip().lower()
        if not process_name.endswith('.exe'):
            process_name += '.exe'

        killed = False
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() == process_name:
                    proc.kill()
                    killed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        if killed:
            speak(
                f"Процес {process_name.replace('.exe', '')} успішно завершено.")
            return True
        else:
            speak(f"Не знайшов процес {process_name}.")
            return False
    except Exception as e:
        print(f"Помилка закриття процесу: {e}")
        return False
