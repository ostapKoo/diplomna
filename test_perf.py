import time
from tts import speak

print("=== ТЕСТУВАННЯ ПРОДУКТИВНОСТІ TTS ===")


start_time = time.time()
speak("Асистент Том і Джері активовано.")
first_run_time = time.time() - start_time
print(f"⏱️ Перший запуск (Без кешу): {first_run_time:.4f} секунд")


start_time = time.time()
speak("Асистент Том і Джері активовано.")
second_run_time = time.time() - start_time
print(f"⏱️ Другий запуск (З кешу): {second_run_time:.4f} секунд")


if second_run_time > 0:
    improvement = (first_run_time / second_run_time) * 100
    print(f"🚀 Швидкодія покращилась у {improvement:.0f} разів!")