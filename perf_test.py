import time
import cProfile
import pstats
import io
from memory_profiler import memory_usage

try:
    import gemini_client
    import utils
    from modes import tom_mode
except ImportError as e:
    print(f"⚠️ Помилка імпорту модулів: {e}")


def test_api_call():
    """Емуляція запиту до API для тесту пам'яті та часу."""
    prompt = "Розкажи короткий жарт."
    try:
        gemini_client.ask_gemini(prompt)
    except Exception as e:
        pass


def test_cpu_load():
    """Навантаження CPU логікою парсингу."""
    for _ in range(1000):
        tom_mode._parse_number_from_query("Встанови гучність на 55 відсотків")
        utils.change_volume(10)


if __name__ == "__main__":

    print("PERFORMANCE TEST")
    print("=======================================================")

    print("\n[TEST 1] Gemini API Latency & Memory")
    try:
        mem_usage = memory_usage(test_api_call)
        avg_mem = sum(mem_usage) / len(mem_usage) if mem_usage else 0
        peak_mem = max(mem_usage) if mem_usage else 0

        latencies = []
        for i in range(3):
            start = time.time()
            test_api_call()
            dur = time.time() - start
            latencies.append(dur)
            print(f"   Run {i + 1}: {dur:.4f} sec")

        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        print(
            f"📊 API Stats: Avg Latency: {avg_latency:.4f}s | Peak Memory: {peak_mem:.2f} MiB")

    except Exception as e:
        print(f"❌ Помилка у тесті 1: {e}")

    print("\nCPU Profiling: Command Parsing")

    pr = cProfile.Profile()
    pr.enable()

    test_cpu_load()

    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(10)
    print(s.getvalue())

    print("\nModule Import Time (Cold Start Simulation)")

    try:
        start_import = time.time()
        #import pycaw
#        import screen_brightness_control

        end_import = time.time()
        print(
            f"⏱️ Import Time (External Libs Check): {end_import - start_import:.4f} sec")
    except Exception as e:
        print(f"⚠️ Помилка імпорту: {e}")

    print("\n✅ Тестування завершено.")
