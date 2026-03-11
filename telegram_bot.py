import os
import telebot
from telebot import types
from dotenv import load_dotenv


import utils
import gemini_client
import tts


original_speak = tts.speak
tom_voice_enabled = True


def conditional_speak(text):
    global tom_voice_enabled
    if tom_voice_enabled:
        original_speak(text)


tts.speak = conditional_speak
utils.speak = conditional_speak

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    print("❌ Помилка: Не знайдено TELEGRAM_BOT_TOKEN у файлі .env")
    exit()

bot = telebot.TeleBot(TOKEN)
user_states = {}


def main_menu_kb():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🐱 Режим Том (ПК)", "🐭 Режим Джері (ШІ)")
    return markup


def tom_menu_kb(voice_enabled):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    # Ряд 1: Медіа
    markup.add("⏮ Попер.", "⏯ Play/Pause", "⏭ Наст.")
    # Ряд 2: Звук
    markup.add("🔉 Гучність -10%", "🔇 Звук (Увімк/Вимк)", "🔊 Гучність +10%")
    # Ряд 3: Яскравість (ПОВЕРНУЛИ!)
    markup.add("🌑 Яскравість -10%", "🔅 Яскравість +10%")
    # Ряд 4: Інтерактив
    markup.add("💬 Повідомлення на ПК",
               "🎮 Запустити гру", "⏰ Нагадування на ПК")
    # Ряд 5: Додатки
    markup.add("📝 Записати нотатку", "🌐 Браузер", "📂 Провідник")
    # Ряд 6: Статус
    markup.add("📸 Зробити скріншот", "📊 Статус ПК", "💻 Диспетчер процесів")
    # Ряд 7: Живлення
    markup.add("🔒 Заблокувати", "🛑 Вимкнути ПК", "❌ Скасувати вимкн.")

    if voice_enabled:
        markup.add("🔇 Вимкнути озвучку дій ПК")
    else:
        markup.add("🔊 Увімкнути озвучку дій ПК")

    markup.add("🔙 Головне меню")
    return markup


def cancel_action_kb():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🚫 Скасувати дію")
    return markup


def games_kb():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    games = utils.get_games_list()
    for game in games:
        markup.add(game)
    markup.add("🚫 Скасувати дію")
    return markup


def jerry_settings_kb():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📱 Відповідати в Телеграм", "💻 Озвучити на ПК")
    markup.add("🔙 Головне меню")
    return markup


def jerry_active_kb():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔙 Головне меню")
    return markup


# ==========================================
# базові команди
# ==========================================

@bot.message_handler(commands=['start'])
def start_message(message):
    user_states[message.chat.id] = {'mode': 'menu'}
    bot.send_message(
        message.chat.id, "Привіт! Оберіть режим роботи:", reply_markup=main_menu_kb())


@bot.message_handler(func=lambda m: m.text in ["🔙 Головне меню"])
def exit_modes(message):
    user_states[message.chat.id] = {'mode': 'menu'}
    bot.send_message(message.chat.id, "Головне меню:",
                     reply_markup=main_menu_kb())


@bot.message_handler(func=lambda message: message.text == "🐱 Режим Том (ПК)")
def tom_mode(message):
    global tom_voice_enabled
    user_states[message.chat.id] = {'mode': 'tom'}
    bot.send_message(message.chat.id, "🐱 Режим керування ПК активний:",
                     reply_markup=tom_menu_kb(tom_voice_enabled))


@bot.message_handler(func=lambda message: message.text == "🐭 Режим Джері (ШІ)")
def jerry_mode(message):
    user_states[message.chat.id] = {'mode': 'jerry_setup'}
    bot.send_message(message.chat.id, "🐭 Джері готовий. Де виводити відповідь?",
                     reply_markup=jerry_settings_kb())


@bot.message_handler(func=lambda m: m.text in ["📱 Відповідати в Телеграм", "💻 Озвучити на ПК"])
def set_jerry_output(message):
    output_type = "tg" if "Телеграм" in message.text else "pc"
    user_states[message.chat.id] = {
        'mode': 'jerry_chat', 'output': output_type}
    bot.send_message(message.chat.id, "Готово! Чекаю на ваше запитання.",
                     reply_markup=jerry_active_kb())


# ==========================================
# том
# ==========================================

@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get('mode') == 'tom')
def handle_tom_commands(message):
    global tom_voice_enabled
    state = user_states[message.chat.id]
    text = message.text

    try:
        # --- 1. ПЕРЕВІРКА ПІДРЕЖИМІВ (Діалоги) ---
        if text == "🚫 Скасувати дію":
            state['sub_mode'] = None
            bot.reply_to(message, "Дію скасовано.",
                         reply_markup=tom_menu_kb(tom_voice_enabled))
            return

        if state.get('sub_mode') == 'waiting_for_message':
            utils.show_message_on_screen(text)
            state['sub_mode'] = None
            bot.reply_to(message, "✅ Повідомлення відправлено на екран ПК!",
                         reply_markup=tom_menu_kb(tom_voice_enabled))
            return

        if state.get('sub_mode') == 'waiting_for_game':
            if text in utils.get_games_list():
                utils.launch_game(text)
                state['sub_mode'] = None
                bot.reply_to(message, f"✅ Запускаю {text} на ПК!", reply_markup=tom_menu_kb(
                    tom_voice_enabled))
            else:
                bot.reply_to(
                    message, "Будь ласка, оберіть гру з кнопок нижче.")
            return

        if state.get('sub_mode') == 'waiting_for_reminder_time':
            if text.isdigit():
                state['reminder_time'] = int(text)
                state['sub_mode'] = 'waiting_for_reminder_text'
                bot.reply_to(
                    message, "Відмінно. Тепер напишіть **ТЕКСТ** нагадування:", parse_mode="Markdown")
            else:
                bot.reply_to(
                    message, "❌ Помилка: Введіть тільки число (кількість хвилин).")
            return

        if state.get('sub_mode') == 'waiting_for_reminder_text':
            minutes = state.get('reminder_time', 1)
            utils.set_reminder(minutes, text)
            state['sub_mode'] = None
            bot.reply_to(message, f"✅ Нагадування успішно встановлено!\n⏳ Спрацює через {minutes} хв.",
                         reply_markup=tom_menu_kb(tom_voice_enabled))
            return
        if state.get('sub_mode') == 'waiting_for_note':
            utils.write_note(text)
            state['sub_mode'] = None
            bot.reply_to(message, "✅ Нотатку успішно збережено у файл notes.txt!",
                         reply_markup=tom_menu_kb(tom_voice_enabled))
            return

        # Кнопки меню
        if text == "💬 Повідомлення на ПК":
            state['sub_mode'] = 'waiting_for_message'
            bot.reply_to(message, "Напишіть текст, який ви хочете вивести на екран:",
                         reply_markup=cancel_action_kb())
            return

        elif text == "🎮 Запустити гру":
            state['sub_mode'] = 'waiting_for_game'
            bot.reply_to(message, "Оберіть гру зі списку:",
                         reply_markup=games_kb())
            return

        elif text == "⏰ Нагадування на ПК":
            state['sub_mode'] = 'waiting_for_reminder_time'
            bot.reply_to(message, "Через скільки хвилин нагадати?\n*(Напишіть просто число, наприклад: 5)*",
                         parse_mode="Markdown", reply_markup=cancel_action_kb())
            return

        #  команди
        if text == "🔇 Вимкнути озвучку дій ПК":
            tom_voice_enabled = False
            bot.reply_to(message, "✅ Озвучку ВИМКНЕНО.",
                         reply_markup=tom_menu_kb(tom_voice_enabled))
        elif text == "🔊 Увімкнути озвучку дій ПК":
            tom_voice_enabled = True
            bot.reply_to(message, "✅ Озвучку УВІМКНЕНО.",
                         reply_markup=tom_menu_kb(tom_voice_enabled))
        elif text == "🔅 Яскравість +10%":
            utils.change_brightness(10)
        elif text == "🌑 Яскравість -10%":
            utils.change_brightness(-10)
        elif text == "🔊 Гучність +10%":
            utils.change_volume(10)
        elif text == "🔉 Гучність -10%":
            utils.change_volume(-10)
        elif text == "🔇 Звук (Увімк/Вимк)":
            utils.toggle_mute()
        elif text == "⏯ Play/Pause":
            utils.media_play_pause()
        elif text == "⏭ Наст.":
            utils.media_next()
        elif text == "⏮ Попер.":
            utils.media_prev()
        elif text == "🌐 Браузер":
            utils.open_browser()
        elif text == "📝 Записати нотатку":
            state['sub_mode'] = 'waiting_for_note'
            bot.reply_to(message, "Напишіть текст, який потрібно зберегти у нотатки:",
                         reply_markup=cancel_action_kb())
            return
        elif text == "📂 Провідник":
            utils.open_explorer()
        elif text == "📊 Статус ПК":
            bot.reply_to(message, utils.get_system_stats())
        elif text == "📸 Зробити скріншот":
            file_path = utils.take_screenshot("temp_screen.png")
            if file_path and os.path.exists(file_path):
                with open(file_path, 'rb') as photo:
                    bot.send_photo(message.chat.id, photo,
                                   caption="📸 Ваш екран")
                os.remove(file_path)
        elif text == "🔒 Заблокувати":
            utils.lock_pc()
        elif text == "🛑 Вимкнути ПК":
            utils.shutdown_pc()
        elif text == "❌ Скасувати вимкн.":
            utils.cancel_shutdown()
        else:
            bot.reply_to(message, "Скористайтеся кнопками меню.")
            if state.get('sub_mode') == 'waiting_for_process_kill':
                if utils.kill_process(text):
                    bot.reply_to(message, f"✅ Процес `{text}` успішно завершено!", parse_mode="Markdown",
                                 reply_markup=tom_menu_kb(tom_voice_enabled))
                else:
                    bot.reply_to(message, f"❌ Процес `{text}` не знайдено, або відмовлено в доступі.",
                                 parse_mode="Markdown", reply_markup=tom_menu_kb(tom_voice_enabled))
                state['sub_mode'] = None
                return

            elif text == "💻 Диспетчер процесів":
                state['sub_mode'] = 'waiting_for_process_kill'
                process_list = utils.get_top_processes()
                bot.reply_to(
                    message,
                    f"{process_list}\n\n⚠️ **Напишіть точну назву програми** зі списку вище (наприклад, `chrome.exe` або `discord.exe`), щоб примусово її закрити:",
                    parse_mode="Markdown",
                    reply_markup=cancel_action_kb()
                )
                return

    except Exception as e:
        state['sub_mode'] = None
        bot.reply_to(
            message, f"❌ Помилка: {e}", reply_markup=tom_menu_kb(tom_voice_enabled))


# ==========================================
# джері
# ==========================================

@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get('mode') == 'jerry_chat')
def handle_jerry_chat(message):
    bot.send_chat_action(message.chat.id, 'typing')
    response_text = gemini_client.ask_gemini(message.text)
    output_type = user_states[message.chat.id].get('output', 'tg')

    if output_type == 'tg':
        bot.send_message(message.chat.id, response_text,
                         reply_markup=jerry_active_kb())
    else:
        bot.send_message(
            message.chat.id, "🔊 Озвучую відповідь на ПК...", reply_markup=jerry_active_kb())
        original_speak(response_text)


@bot.message_handler(func=lambda message: True)
def catch_all(message):
    user_states[message.chat.id] = {'mode': 'menu'}
    bot.send_message(
        message.chat.id,
        "🔄 Бот був перезавантажений або команда не розпізнана.\nБудь ласка, оберіть режим:",
        reply_markup=main_menu_kb()
    )


if __name__ == "__main__":
    print("⏳ Підключення до Telegram...")
    try:
        bot.remove_webhook()
        print("🚀 Telegram бот успішно запущено! Натисніть Ctrl+C для зупинки.")
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"❌ КРИТИЧНА ПОМИЛКА: {e}")
