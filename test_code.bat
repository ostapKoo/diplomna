@echo off
echo === Запуск Flake8 (Стиль коду) ===
flake8 .
echo === Запуск Mypy (Статична типізація) ===
mypy main.py utils.py telegram_bot.py --ignore-missing-imports
echo === Перевірка завершена ===
pause
