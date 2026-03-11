import customtkinter as ctk
import threading
import sys
import os
import queue
import time
from tkinter import messagebox


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


assistant_loaded = False
bot_loaded = False

try:
    from main import main_assistant

    assistant_loaded = True
except ImportError:
    print("❌ Попередження: main.py не знайдено.")

try:
    import telegram_bot

    bot_loaded = True
except ImportError:
    print("❌ Попередження: telegram_bot.py не знайдено.")


class ModernAssistantGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Голосовий Асистент: Том і Джері")
        self.geometry("850x600")
        self.minsize(700, 500)

        self.is_bot_running = False

        self.log_queue = queue.Queue()
        self.check_log_queue()
        sys.stdout = self.RedirectText(self.log_queue)
        sys.stderr = self.RedirectText(self.log_queue)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.setup_main_panel()

    def setup_sidebar(self):
        """Бічна панель (Sidebar) з кнопками керування"""
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Tom & Jerry\nDashboard",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 30))


        self.start_voice_btn = ctk.CTkButton(
        self.sidebar_frame,
            text="🎤 Старт Голосу",
            command=self.start_voice_assistant,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.start_voice_btn.grid(row=1, column=0, padx=20, pady=10)


        self.tg_switch_var = ctk.StringVar(value="off")
        self.tg_switch = ctk.CTkSwitch(
            self.sidebar_frame,
            text="Telegram Бот",
            command=self.toggle_telegram_bot,
            variable=self.tg_switch_var,
            onvalue="on",
            offvalue="off",
            font=ctk.CTkFont(size=14),
            progress_color="#3498db"
        )
        self.tg_switch.grid(row=2, column=0, padx=20, pady=(20, 10))

        if not bot_loaded:
            self.tg_switch.configure(state="disabled", text="ТГ Бот недоступний")


        self.settings_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="⚙️ Налаштування API",
            command=self.open_settings,
            fg_color="#f39c12",  # Помаранчевий
            hover_color="#e67e22"
        )
        self.settings_btn.grid(row=3, column=0, padx=20, pady=30)


        self.exit_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="🛑 Вийти з програми",
            command=self.stop_program,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        self.exit_btn.grid(row=7, column=0, padx=20, pady=20)

    def setup_main_panel(self):
        """Основна зона з логами та статусом"""
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.log_frame.grid_columnconfigure(0, weight=1)
        self.log_frame.grid_rowconfigure(1, weight=1)

        self.log_label = ctk.CTkLabel(
            self.log_frame,
            text="📋 Журнал Активності",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.log_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.log_area = ctk.CTkTextbox(
            self.log_frame,
            font=("Consolas", 13),
            corner_radius=10,
            text_color="#e0e0e0"
        )
        self.log_area.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.log_area.configure(state="disabled")

        self.status_var = ctk.StringVar(value="Готовий до запуску...")
        self.status_label = ctk.CTkLabel(
            self,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color="#95a5a6"
        )
        self.status_label.grid(row=1, column=1, padx=20, pady=(0, 10), sticky="w")


    def open_settings(self):
        """Відкриває вікно для введення API ключів"""
        settings_win = ctk.CTkToplevel(self)
        settings_win.title("Налаштування API")
        settings_win.geometry("450x350")
        settings_win.attributes("-topmost", True)
        settings_win.resizable(False, False)

        ctk.CTkLabel(settings_win, text="🔧 Налаштування Токенів", font=ctk.CTkFont(size=18, weight="bold")).pack(
            pady=15)


        ctk.CTkLabel(settings_win, text="Telegram Bot Token:").pack(anchor="w", padx=30)
        tg_entry = ctk.CTkEntry(settings_win, width=390, show="*", placeholder_text="Вставте токен від BotFather...")
        tg_entry.pack(pady=(0, 15), padx=30)


        ctk.CTkLabel(settings_win, text="Gemini API Key:").pack(anchor="w", padx=30)
        gemini_entry = ctk.CTkEntry(settings_win, width=390, show="*",
                                    placeholder_text="Вставте ключ від Google AI Studio...")
        gemini_entry.pack(pady=(0, 20), padx=30)

        def save_keys():
            tg_token = tg_entry.get().strip()
            gemini_key = gemini_entry.get().strip()


            env_vars = {}
            if os.path.exists(".env"):
                with open(".env", "r", encoding="utf-8") as file:
                    for line in file:
                        if "=" in line:
                            k, v = line.strip().split("=", 1)
                            env_vars[k] = v


            if tg_token: env_vars["TELEGRAM_BOT_TOKEN"] = tg_token
            if gemini_key: env_vars["GEMINI_API_KEY"] = gemini_key


            try:
                with open(".env", "w", encoding="utf-8") as file:
                    for k, v in env_vars.items():
                        file.write(f"{k}={v}\n")

                messagebox.showinfo(
                    "Успіх",
                    "✅ Ключі успішно збережено у файл .env!\n\n⚠️ БУДЬ ЛАСКА, перезапустіть програму, щоб нові ключі почали працювати."
                )
                settings_win.destroy()
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося зберегти файл: {e}")


        ctk.CTkButton(
            settings_win,
            text="💾 Зберегти ключі",
            command=save_keys,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(pady=10)

        ctk.CTkLabel(settings_win, text="*Ключі приховані для вашої безпеки", text_color="gray",
                     font=("Arial", 10)).pack()


    def start_voice_assistant(self):
        if not assistant_loaded:
            messagebox.showerror("Помилка!", "Файл main.py не знайдено!")
            return

        self.start_voice_btn.configure(state="disabled", text="Голос активний")
        self.status_var.set("Асистент запускається...")

        self.voice_thread = threading.Thread(target=main_assistant, daemon=True)
        self.voice_thread.start()

    def toggle_telegram_bot(self):
        state = self.tg_switch_var.get()

        if state == "on" and not self.is_bot_running:
            self.is_bot_running = True
            self.status_var.set("Запуск Telegram-бота...")
            self.tg_thread = threading.Thread(target=self.run_telegram_bot, daemon=True)
            self.tg_thread.start()

        elif state == "off" and self.is_bot_running:
            self.is_bot_running = False
            self.status_var.set("Зупинка Telegram-бота...")
            threading.Thread(target=self.stop_telegram_bot, daemon=True).start()

    def run_telegram_bot(self):
        try:
            print("⏳ Підключення до Telegram...")
            telegram_bot.bot.remove_webhook()
            print("🚀 Telegram бот успішно запущено!")
            telegram_bot.bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"❌ Помилка ТГ бота: {e}")
            self.is_bot_running = False
            self.after(0, self.tg_switch.deselect)

    def stop_telegram_bot(self):
        print("🛑 Зупинка Telegram-бота...")
        telegram_bot.bot.stop_polling()
        print("✅ Telegram-бот вимкнено.")

    def stop_program(self):
        print("--- Завершення роботи... ---")
        if self.is_bot_running and bot_loaded:
            telegram_bot.bot.stop_polling()
        self.destroy()
        sys.exit()


    def check_log_queue(self):
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.add_log_message(message)
        except queue.Empty:
            pass
        self.after(100, self.check_log_queue)

    def add_log_message(self, message):
        self.log_area.configure(state="normal")
        timestamp = time.strftime("[%H:%M:%S] ")
        self.log_area.insert("end", f"{timestamp}{message}\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

        if "🎤" in message:
            self.status_var.set("Говоріть зараз...")
        elif "🧠" in message:
            self.status_var.set("Розпізнавання...")
        elif "🔊" in message:
            self.status_var.set("Асистент говорить...")
        elif "🚀 Telegram" in message:
            self.status_var.set("Телеграм-бот онлайн")
        elif "✅ Telegram-бот вимкнено" in message:
            self.status_var.set("Телеграм-бот вимкнено")

    class RedirectText:
        def __init__(self, queue):
            self.queue = queue

        def write(self, text):
            if text.strip(): self.queue.put(text)

        def flush(self):
            pass


if __name__ == "__main__":
    app = ModernAssistantGUI()
    app.protocol("WM_DELETE_WINDOW", app.stop_program)
    app.mainloop()