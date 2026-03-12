from gtts import gTTS
from pydub import AudioSegment
import simpleaudio as sa
import io
from functools import lru_cache
from logger_config import logger

@lru_cache(maxsize=20)
def _generate_wav_bytes(text: str, lang: str = 'uk') -> bytes:
    """
    Генерує WAV аудіо в пам'яті та повертає байти.
    Кешується для максимальної швидкодії.
    """
    logger.debug(f"Мережевий запит gTTS для: '{text}' (Не з кешу)")

    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang=lang)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    wav_io = io.BytesIO()
    audio_segment = AudioSegment.from_file(mp3_fp, format="mp3")
    audio_segment.export(wav_io, format="wav")

    wav_bytes = wav_io.getvalue()

    mp3_fp.close()
    wav_io.close()

    return wav_bytes


def speak(text: str):
    """
   Озвучує переданий текст українською мовою за допомогою gTTS.
   Зберігає згенероване аудіо у тимчасовий файл, конвертує його

   у формат WAV за допомогою pydub та відтворює через simpleaudio.
   Args:

       text (str): Текст, який необхідно озвучити.
   Raises:
       Exception: Якщо виникає помилка при генерації або відтворенні аудіо,
                  помилка виводиться у консоль.
   """
    logger.info(f"Озвучення: {text}", extra={'context': 'TTS'})
    try:
        wav_bytes = _generate_wav_bytes(text)

        wave_obj = sa.WaveObject.from_wave_file(io.BytesIO(wav_bytes))
        play_obj = wave_obj.play()
        play_obj.wait_done()

    except Exception as e:
        logger.error(f"Помилка озвучення (gTTS): {e}", exc_info=True)