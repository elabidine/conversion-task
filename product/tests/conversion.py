from decimal import Decimal as Dec
from django.forms import ValidationError
from django.test import TestCase
from core.enums.currency import Currency
from core.utils import convert_price, convert_unit
from core.utils.convert_currency import convert_currency
from unittest.mock import patch

from product.enums import SystemUnit
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
        _print_object(print_function_name=True)
        with self.assertRaises(ValidationError) as cm:
            convert_currency(self.price, from_currency=None, to_currency=Currency.EUR)
        _print_object({"input": {"price": self.price, "from_currency": None, "to_currency": Currency.EUR}, "output": str(cm.exception)})

    def test_02_return_original_when_currencies_are_same(self):
        _print_object(print_function_name=True)
        result = convert_currency(self.price, **self.same_currency)
        _print_object({"input": {"price": self.price, "same_currency": self.same_currency}, "output": result})
        self.assertEqual(result, self.price)

    def test_03_raise_error_for_invalid_currency(self):
        _print_object(print_function_name=True)
        with self.assertRaises(ValidationError) as cm:
            convert_currency(self.price, **self.invalid_currency)
        _print_object({"input": {"price": self.price, "invalid_currency": self.invalid_currency}, "output": str(cm.exception)})

    @patch("core.utils.convert_currency.get_exchange_rate")
    def test_04_convert_currency_correctly(self, mock_get_rate):
        _print_object(print_function_name=True)
        mock_get_rate.side_effect = lambda currency: self.mock_exchange_rates[currency]
        result = convert_currency(self.price, **self.valid_currencies)
        expected_price = (self.price * Dec("0.80")) / Dec("1.20")
        _print_object({"input": {"price": self.price, "valid_currencies": self.valid_currencies}, "output": result})
        self.assertEqual(result, expected_price.quantize(Dec("0.0001")))

    @patch("core.utils.convert_currency.fetch_specific_rate_from_api")
    def test_05_fetch_rate_when_not_in_database(self, fetch_rate_function):
        _print_object(print_function_name=True)
        fetch_rate_function.return_value = Dec("1.25")
        result = convert_currency(self.price, from_currency=Currency.USD, to_currency=Currency.EUR)
        _print_object({"input": {"price": self.price, "from_currency": Currency.USD, "to_currency": Currency.EUR}, "output": result})
        self.assertEqual(result, Dec("80.00"))

    def test_06_identical_units(self):
        _print_object(print_function_name=True)
        from_unit = to_unit = SystemUnit.KG
        result = convert_unit(self.price, from_unit, to_unit)
        _print_object({"input": {"price": self.price, "from_unit": from_unit, "to_unit": to_unit}, "output": result})
        self.assertEqual(result, self.price)

    def test_07_conversion_between_same_dimension_units(self):
        _print_object(print_function_name=True)
        from_unit = SystemUnit.KG
        to_unit = SystemUnit.GRAM
        result = convert_unit(self.price, from_unit, to_unit)
        expected = self.price * Dec(to_unit.units_to_base) / Dec(from_unit.units_to_base)
        _print_object({"input": {"price": self.price, "from_unit": from_unit, "to_unit": to_unit}, "output": result})
        self.assertEqual(result, expected.quantize(Dec("0.0001")))

    def test_08_conversion_between_different_dimensions(self):
        _print_object(print_function_name=True)
        from_unit = SystemUnit.KG
        to_unit = SystemUnit.LIT
        with self.assertRaises(ValidationError) as cm:
            convert_unit(self.price, from_unit, to_unit)
        _print_object({"input": {"price": self.price, "from_unit": from_unit, "to_unit": to_unit}, "output": str(cm.exception)})
        

    @patch('core.utils.convert_price.convert_currency')  
    @patch('core.utils.convert_price.convert_unit')    
    def test_convert_09_price_currency_and_unit(self, mock_convert_unit, mock_convert_currency):
        """
           Test the convert_price function to ensure it correctly handles both
           currency and unit conversions by mocking external dependencies.
        """
        _print_object(print_function_name=True)
        mock_convert_currency.return_value = Dec('100.00')  
        mock_convert_unit.return_value = Dec('110.00') 
        
        result = convert_price(self.price, self.valid_currencies["from_currency"], self.valid_currencies["to_currency"], SystemUnit.KG, SystemUnit.GRAM)
        _print_object({"input": {"price": self.price, "from_unit": SystemUnit.KG, "to_unit":  SystemUnit.GRAM,"from_currency":self.valid_currencies["from_currency"],"to_currency":self.valid_currencies["to_currency"]}, "output": Dec("110")})
        self.assertEqual(result, Dec('110.00'))
        


