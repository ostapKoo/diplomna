from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def before_all(context):
    # 1. Мокаємо гучність (Volume Control)
    # Використовуємо create=True, щоб створити атрибут, якщо його немає
    context.volume_patcher = patch('utils.volume_control', create=True)
    context.mock_volume = context.volume_patcher.start()

    # Налаштовуємо поведінку
    context.mock_volume.GetMasterVolumeLevelScalar.return_value = 0.5

    # 2. Мокаємо TTS (щоб не говорив голосом)
    context.tts_patcher = patch('tts.speak', create=True)
    context.mock_speak = context.tts_patcher.start()

    # 3. Підміняємо прапорець завантаження
    import utils
    utils.PYCAW_LOADED = True


def after_all(context):
    # Безпечне завершення патчів
    if hasattr(context, 'volume_patcher'):
        context.volume_patcher.stop()
    if hasattr(context, 'tts_patcher'):
        context.tts_patcher.stop()