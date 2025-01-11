import unittest
from unittest.mock import patch, MagicMock
import main

class TestCurrencyFetcher(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_currencies_invalid_code(self, mock_get):
        # Мокаем ответ от API
        mock_response = MagicMock()
        mock_response.content = """
        <ValCurs Date="01.01.2025" name="Foreign Currency Market">
            <Valute ID="R01035">
                <NumCode>840</NumCode>
                <CharCode>USD</CharCode>
                <Nominal>1</Nominal>
                <Name>Доллар США</Name>
                <Value>75,1234</Value>
            </Valute>
        </ValCurs>
        """

        mock_get.return_value = mock_response

        fetcher = main.CurrencyFetcher(cooldown=1)
        result = fetcher.fetch_currencies(['R9999'])  # Некорректный ID

        # Проверка, что результат для некорректного кода валюты - None
        expected_result = [{'R9999': None}]
        self.assertEqual(result, expected_result)

    def test_get_currency_info(self):
        fetcher = main.CurrencyFetcher(cooldown=1)
        fetcher._currencies = {
            'USD': ('Доллар США', ('75', '1234')),
            'EUR': ('Евро', ('85', '5678'))
        }

        result = fetcher.get_currency_info('USD')
        expected_result = ('Доллар США', ('75', '1234'))
        self.assertEqual(result, expected_result)

        result_invalid = fetcher.get_currency_info('GBP')
        self.assertIsNone(result_invalid)

    def test_get_currency_info_invalid(self):
        fetcher = main.CurrencyFetcher(cooldown=1)
        result = fetcher.get_currency_info('GBP')
        self.assertIsNone(result)

    def test_visualize_currencies(self):
        # Тестируем визуализацию
        fetcher = main.CurrencyFetcher(cooldown=1)
        fetcher._currencies = {
            'USD': ('Доллар США', ('75', '1234')),
            'EUR': ('Евро', ('85', '5678'))
        }

        # Мокаем plt.savefig, чтобы избежать реального сохранения файла
        with patch('matplotlib.pyplot.savefig') as mock_savefig:
            fetcher.visualize_currencies()
            mock_savefig.assert_called_once_with('currencies.jpg')  # Проверка на один вызов

            # Можно также проверить, что данные визуализируются корректно
            args, kwargs = mock_savefig.call_args
            self.assertTrue(args[0].endswith('.jpg'))  # Проверка правильности имени файла

if __name__ == '__main__':
    unittest.main()
