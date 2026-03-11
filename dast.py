import time
import os
import sys
from zapv2 import ZAPv2

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import gemini_client
except ImportError:
    print("❌ Помилка: Не знайдено файл gemini_client.py")
    sys.exit(1)


def run_dast_scan():
    ZAP_API_KEY = 'luo93kl8skuagq6r1c8q2but4r'
    ZAP_PROXY_HOST = '127.0.0.1'
    ZAP_PROXY_PORT = '8081'

    print(f"⏳ Підключення до OWASP ZAP на порту {ZAP_PROXY_PORT}...")

    zap = ZAPv2(apikey=ZAP_API_KEY, proxies={
        'http': f'http://{ZAP_PROXY_HOST}:{ZAP_PROXY_PORT}',
        'https': f'http://{ZAP_PROXY_HOST}:{ZAP_PROXY_PORT}'
    })

    try:
        version = zap.core.version
        print(f"✅ ZAP знайдено! Версія: {version}")
    except Exception as e:
        print(f"❌ Не вдалося підключитися до ZAP: {e}")
        print("Переконайтеся, що програма OWASP ZAP запущена і порт співпадає.")
        return

    cert_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "zap_cert.pem")

    if not os.path.exists(cert_path):
        print(f"❌ ПОМИЛКА: Не знайдено файл '{cert_path}'")
        print("Експортуйте сертифікат із ZAP (Tools -> Options -> Network -> Server Certificates -> Save)")
        return

    print(f"🔐 Використовуємо сертифікат: {cert_path}")

    print("🔄 Налаштування проксі для перехоплення трафіку...")

    os.environ["HTTP_PROXY"] = f"http://{ZAP_PROXY_HOST}:{ZAP_PROXY_PORT}"
    os.environ["HTTPS_PROXY"] = f"http://{ZAP_PROXY_HOST}:{ZAP_PROXY_PORT}"

    os.environ["REQUESTS_CA_BUNDLE"] = cert_path
    os.environ["CURL_CA_BUNDLE"] = cert_path

    os.environ["GRPC_DEFAULT_SSL_ROOTS_FILE_PATH"] = cert_path

    print("🚀 Генерація трафіку (відправка запитів до Gemini)...")

    test_prompts = [
        "Привіт, це тест безпеки DAST.",
        "Розкажи короткий факт про космос."
    ]

    for prompt in test_prompts:
        print(f"   -> Відправка запиту: '{prompt}'")
        try:
            response = gemini_client.ask_gemini(prompt)
            print("      ✅ Отримано відповідь (200 OK)")
        except Exception as e:
            print(f"      ❌ Помилка виконання: {e}")

        time.sleep(2)

    print("\n📊 Аналіз результатів сканування в ZAP...")

    time.sleep(3)

    alerts = zap.core.alerts()

    if len(alerts) == 0:
        print("✅ ZAP не знайшов явних вразливостей (це добре!).")
        print("Перевірте вкладку 'History' в самому ZAP, щоб побачити перехоплені запити.")
    else:
        print(f"⚠️ Знайдено {len(alerts)} сповіщень (Alerts):\n")
        print(f"{'RISK':<15} | {'NAME'}")
        print("-" * 60)

        for alert in alerts:
            risk = alert.get('risk')
            name = alert.get('name')
            print(f"{risk:<15} | {name}")

    os.environ.pop("HTTP_PROXY", None)
    os.environ.pop("HTTPS_PROXY", None)
    os.environ.pop("REQUESTS_CA_BUNDLE", None)
    os.environ.pop("GRPC_DEFAULT_SSL_ROOTS_FILE_PATH", None)


if __name__ == "__main__":
    run_dast_scan()
