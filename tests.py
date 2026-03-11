import unittest
from unittest.mock import patch, MagicMock
from modes.tom_mode import _parse_number_from_query
import utils
import gemini_client


class TestTomJerryLogic(unittest.TestCase):

    def test_parse_number_valid(self):
        """Перевірка вилучення числа з коректної фрази."""

        self.assertEqual(_parse_number_from_query("гучність 50"), 50)
        self.assertEqual(_parse_number_from_query("яскравість 100"), 100)
        self.assertEqual(_parse_number_from_query("0 відсотків"), 0)

    def test_parse_number_invalid(self):
        """Перевірка ігнорування некоректних чисел."""

        self.assertIsNone(_parse_number_from_query("гучність 101"))
        self.assertIsNone(_parse_number_from_query("гучність багато"))
        self.assertIsNone(_parse_number_from_query("текст без чисел"))


    @patch('utils.volume_control')
    @patch('utils.PYCAW_LOADED', True)
    def test_change_volume_clamping_max(self, mock_volume):
        """Перевірка, що гучність не перевищує 100%."""


        mock_volume.GetMasterVolumeLevelScalar.return_value = 0.95


        utils.change_volume(10)


        mock_volume.SetMasterVolumeLevelScalar.assert_called_with(1.0, None)

    @patch('utils.volume_control')
    @patch('utils.PYCAW_LOADED', True)
    def test_change_volume_clamping_min(self, mock_volume):
        """Перевірка, що гучність не падає нижче 0%."""


        mock_volume.GetMasterVolumeLevelScalar.return_value = 0.05


        utils.change_volume(-10)


        mock_volume.SetMasterVolumeLevelScalar.assert_called_with(0.0, None)


    @patch('gemini_client.model')
    def test_ask_gemini_success(self, mock_model):
        """Перевірка успішного запиту до AI."""
        mock_chat = MagicMock()
        mock_chat.send_message.return_value.text = "Привіт, я Джері."
        mock_model.start_chat.return_value = mock_chat

        response = gemini_client.ask_gemini("Привіт")
        self.assertEqual(response, "Привіт, я Джері.")

    @patch('gemini_client.model')
    def test_ask_gemini_error(self, mock_model):
        """Перевірка обробки виключення (API Error)."""
        mock_model.start_chat.side_effect = Exception("API Error 500")
        response = gemini_client.ask_gemini("Привіт")
        self.assertIn("❌", response)


if __name__ == '__main__':
    unittest.main()