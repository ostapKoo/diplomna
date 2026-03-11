import os
import sys
import subprocess
import json


def run_sast_scan():
    print("\n🔍 Запуск SAST-сканування коду...")

    output_file = "bandit_results.json"
    excludes = "venv,.venv,.git,.idea,__pycache__"

    cmd = [
        sys.executable, "-m", "bandit",
        "-r", ".",
        "-f", "json",
        "-o", output_file,
        "-x", excludes
    ]

    try:
        subprocess.run(cmd, check=False)
        print(f"✅ Сканування завершено. Результати збережено у {output_file}")
    except Exception as e:
        print(f"❌ Помилка запуску: {e}")
        return


    if not os.path.exists(output_file):
        print("⚠️ Файл звіту не створено.")
        return


    try:
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("⚠️ Помилка читання файлу звіту (можливо, він порожній або пошкоджений).")
        return

    results = data.get("results", [])

    print("\n" + "=" * 40)
    print("📊 ЗВІТ SAST (BANDIT)")
    print("=" * 40)

    if not results:
        print("🎉 Чудово! Вразливостей не знайдено.")
    else:
        print(f"⚠️ Знайдено проблем: {len(results)}\n")

        for i, issue in enumerate(results, 1):
            severity = issue['issue_severity']
            msg = issue['issue_text']
            filename = issue['filename']
            line = issue['line_number']
            code = issue['code'].strip()

            sev_icon = "🔴" if severity == 'HIGH' else "🟠" if severity == 'MEDIUM' else "🔵"

            print(f"{i}. {sev_icon} [{severity}] {msg}")
            print(f"   Файл: {filename}:{line}")
            print(f"   Код:  {code}")
            print("-" * 40)

    print("\nℹ️  Пояснення:")
    print("   🔴 HIGH: Критична проблема, потребує негайного виправлення.")
    print("   🟠 MEDIUM: Потенційна проблема.")
    print("   🔵 LOW: Незначне зауваження.")


if __name__ == "__main__":
    run_sast_scan()