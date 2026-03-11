from gtts import gTTS
from pydub import AudioSegment
import simpleaudio as sa
import io


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

    mp3_fp = io.BytesIO()
    wav_io = io.BytesIO()

    try:
        print(f"🔊 Асистент: {text}")
        tts = gTTS(text=text, lang='uk')

        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        audio_segment = AudioSegment.from_file(mp3_fp, format="mp3")

        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)

        wave_obj = sa.WaveObject.from_wave_file(wav_io)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    except Exception as e:
        print(f"❌ Помилка озвучення (gTTS): {e}")
    finally:
        mp3_fp.close()
        wav_io.close()
