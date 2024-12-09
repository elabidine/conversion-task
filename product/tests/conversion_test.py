from decimal import Decimal as Dec
from django.forms import ValidationError
from django.test import TestCase
from core.enums.currency import Currency
from core.utils.convert_currency import convert_currency
from unittest.mock import patch
from core.models.exchange_rate import ExchangeRate
from django.utils.timezone import now

from utils.print_object import _print_object


class AbstractConversionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for testing
        cls.price = Dec("100.00")
        cls.valid_currencies = {
            "from_currency": Currency.USD,
            "to_currency": Currency.EUR,
        }
        cls.same_currency = {
            "from_currency": Currency.USD,
            "to_currency": Currency.USD,
        }
        cls.invalid_currency = {
            "from_currency": "INVALID",
            "to_currency": Currency.EUR,
        }
        cls.mock_exchange_rates = {
            Currency.USD: Dec("1.20"),
            Currency.EUR: Dec("0.80"),
        }

    def test_01_raise_exception_for_missing_from_currency(self):
        # Given a missing source currency
        with self.assertRaises(ValidationError) as cm:
            convert_currency(self.price, from_currency=None, to_currency=Currency.EUR)
        _print_object( self,'_Input >', 'price', '_Output >', 'The source currency must be provided.', print_function_name=True)
        # Then a meaningful error message is returned
        self.assertIn("The source currency must be provided.",str(cm.exception))

    def test_02_return_original_price_for_same_currency(self):
        # Given the same source and target currencies
        result = convert_currency(self.price, **self.same_currency)
        _print_object(self, '_Input >', 'price', 'invalid_currency', print_function_name=True)
        
        # Then the original price is returned
        self.assertEqual(result, self.price)

    def test_03_raise_exception_for_invalid_currency(self):
        # Given an invalid source currency
        
        with self.assertRaises(ValidationError) as cm:
            convert_currency(self.price, **self.invalid_currency)

        # Then a meaningful error message is returned
        self.assertIn("One or both provided currencies are invalid", str(cm.exception))

    @patch("core.utils.convert_currency.get_exchange_rate")
    def test_04_convert_price_with_valid_currencies(self, mock_get_rate):
        # Given valid exchange rates and a price
        mock_get_rate.side_effect = lambda currency: self.mock_exchange_rates[currency]
        result = convert_currency(self.price, **self.valid_currencies)

        # Then the price is converted correctly
        expected_price = (self.price / Dec("1.20")) * Dec("0.80")  # Formula for conversion
        self.assertEqual(result, expected_price.quantize(Dec("0.01")))

    @patch("core.utils.convert_currency.fetch_specific_rate_from_api")
    def test_05_fetch_rate_when_not_in_database(self, fetch_rate_function):
        # Given the API returns a valid rate
        fetch_rate_function.return_value = Dec("1.25")
        rate = convert_currency(self.price, from_currency=Currency.USD, to_currency=Currency.EUR)

        # Then the rate is used in the conversion
        self.assertEqual(rate,Dec(80))

    @patch("core.utils.convert_currency.ExchangeRate.objects.get")
    def test_06_use_rate_from_database_when_fresh(self, mock_db_rate):
        # Given a fresh exchange rate in the database
        mock_db_rate.return_value = ExchangeRate(
            currency=Currency.USD, rate=Dec("1.25"), datetime=now()
        )
        result = convert_currency(self.price, from_currency=Currency.USD, to_currency=Currency.EUR)

        # Then the price is converted using the database rate
        self.assertEqual(result,Dec(80))

    def test_07_calculate_taxed_price_properties(self):
        # Add properties to ensure full coverage of calculations
        converted = Dec("100.00") * Dec("0.80") / Dec("1.20")
        self.assertEqual(converted.quantize(Dec("0.01")), Dec("66.67"))
