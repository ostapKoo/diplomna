import unittest
from unittest.mock import patch, MagicMock
import sys
import io


import utils
import gemini_client
import tts

class TestIntegrationComponents(unittest.TestCase):
    @patch('tts.speak')
    def test_utils_integrates_with_tts(self, mock_speak):
        """
        Integration Test: Перевірка того, що модуль utils коректно
        передає дані в модуль tts.
        """
        print("\n--- Running Integration Test: Utils -> TTS ---")
        utils.tell_time()

        self.assertTrue(mock_speak.called, "Помилка: utils.tell_time() не викликала tts.speak()")

        args, _ = mock_speak.call_args
        print(f"Utils передав у TTS: '{args[0]}'")
        self.assertIn("Зараз", args[0])


    @patch('gemini_client.model')
    def test_gemini_client_integrates_with_api(self, mock_model):
        """
        Integration Test: Перевірка взаємодії клієнта з бібліотекою Google API
        з використанням Mock-об'єкта.
        """
        print("\n--- Running Integration Test: Gemini Client -> Google API (Mocked) ---")


        mock_chat = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Це тестова відповідь від штучного інтелекту."


        mock_model.start_chat.return_value = mock_chat
        mock_chat.send_message.return_value = mock_response


        user_prompt = "Хто ти?"
        result = gemini_client.ask_gemini(user_prompt)



        self.assertEqual(result, "Це тестова відповідь від штучного інтелекту.")

        mock_chat.send_message.assert_called_once_with(user_prompt)
        print("Gemini Client успішно викликав метод send_message() у бібліотеки Google.")


if __name__ == '__main__':
    unittest.main()