from decimal import Decimal as Dec
from django.forms import ValidationError
from django.test import TestCase
from core.enums.currency import Currency
from core.utils import convert_price, convert_unit
from core.utils.convert_currency import convert_currency, get_exchange_rate
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
            Currency.USD: Dec("0.95"),
            Currency.EUR: Dec("1"),
        }

    def test_01_raise_error_for_missing_from_currency(self):
        #Raise an exception if the source currency is not provided
        _print_object(print_function_name=True)
        
        with self.assertRaises(ValidationError) as cm:
            convert_currency(self.price, from_currency=None, to_currency=Currency.EUR)
            
        _print_object({"input": {"price": self.price, "from_currency": None, "to_currency": Currency.EUR}, "output": str(cm.exception)})

    def test_02_conversion_with_missing_target_currency(self):
        #Return the input price if the target currency is not provided
        _print_object(print_function_name=True)
        
        result = convert_currency(self.price,from_currency=Currency.USD)
        _print_object({"input": {"price": self.price, "from_currency": Currency.USD}, "output": result})
        self.assertEqual(result, self.price)
        
    def test_03_conversion_with_same_currency(self):
        #Return the input price i the source and target currency are the same
        _print_object(print_function_name=True)
        
        result = convert_currency(self.price, **self.same_currency)
        _print_object({"input": {"price": self.price, "same_currency": self.same_currency}, "output": result})
        self.assertEqual(result, self.price)

    def test_04_exchange_rate_of_eur(self):
        #if the currency is EUR, the rate is 1
        _print_object(print_function_name=True)
        
        result = get_exchange_rate(Currency.EUR)
        _print_object({"input": {"currency": Currency.EUR}, "output": result})
        self.assertEqual(result, Dec("1"))
        
    def test_05_raise_error_for_invalid_currency(self):
        #Raise an error if the currency is not valid
        _print_object(print_function_name=True)
        
        with self.assertRaises(ValidationError) as cm:
            convert_currency(self.price, **self.invalid_currency)
        _print_object({"input": {"price": self.price, "invalid_currency": self.invalid_currency}, "output": str(cm.exception)})

    @patch("core.utils.convert_currency.get_exchange_rate")
    def test_06_convert_currency_correctly(self, mock_get_rate):
        # This test uses mocking because exchange rates fluctuate over time. 
        # Without mocking, comparing the result with a fixed value would cause the test to fail.
        _print_object(print_function_name=True)
        
        mock_get_rate.side_effect = lambda currency: self.mock_exchange_rates[currency]
        result = convert_currency(self.price, **self.valid_currencies)
        expected_price = Dec('105.2632')
        
        _print_object({"input": {"price": self.price, "valid_currencies": self.valid_currencies}, "output": result})
        self.assertEqual(result, expected_price.quantize(Dec("0.0001")))

    @patch("core.utils.convert_currency.fetch_specific_rate_from_api")
    def test_07_fetch_rate_when_missing_in_database(self, fetch_rate_function):
        # Fetch the rate from the API when it's not in the database or the datetime is more then 24Hours
        # The mock function should return the rate from the API.
        _print_object(print_function_name=True)
        
        fetch_rate_function.return_value = Dec("1.25")
        result = convert_currency(self.price, from_currency=Currency.USD, to_currency=Currency.EUR)
        
        _print_object({"input": {"price": self.price, "from_currency": Currency.USD, "to_currency": Currency.EUR}, "output": result})
        self.assertEqual(result, Dec("80.00"))

    def test_08_conversion_of_identical_units(self):
        #Return the input_price if the target and the source are the same
        _print_object(print_function_name=True)
        from_unit = to_unit = SystemUnit.KG
        result = convert_unit(self.price, from_unit, to_unit)
        _print_object({"input": {"price": self.price, "from_unit": from_unit, "to_unit": to_unit}, "output": result})
        self.assertEqual(result, self.price)
        
    def test_09_conversion_without_target_unit(self):
        #Return the input_price if the target unit is not provided
        _print_object(print_function_name=True)
        
        from_unit = to_unit = SystemUnit.KG
        result = convert_unit(self.price, from_unit, to_unit)
        
        _print_object({"input": {"price": self.price, "from_unit": from_unit, "to_unit": None}, "output": result})
        self.assertEqual(result, self.price)

    def test_10_conversion_between_same_dimension_units(self):
        #Conversion price between same dimension units
        _print_object(print_function_name=True)
        
        from_unit = SystemUnit.KG
        to_unit = SystemUnit.GRAM
        result = convert_unit(self.price, from_unit, to_unit)
        expected = self.price * Dec(to_unit.units_to_base) / Dec(from_unit.units_to_base)
        
        _print_object({"input": {"price": self.price, "from_unit": from_unit, "to_unit": to_unit}, "output": result})
        self.assertEqual(result, expected.quantize(Dec("0.0001")))

    def test_11_conversion_with_invalid_unit(self):
        #Raise an error if either unit is not a valid system unit
        _print_object(print_function_name=True)
        
        from_unit = SystemUnit.KG
        with self.assertRaises(ValidationError) as cm:
            convert_unit(self.price, from_unit, "invalid")
            
        _print_object({"input": {"price": self.price, "from_unit": "Couple", "to_unit": "Plate"}, "output": str(cm.exception)})
        
    def test_12_conversion_between_different_dimensions(self):
        #Raise an error if the dimensions of the units are different
        _print_object(print_function_name=True)
        from_unit = SystemUnit.KG
        to_unit = SystemUnit.LIT
        with self.assertRaises(ValidationError) as cm:
            convert_unit(self.price, from_unit, to_unit)
            
        _print_object({"input": {"price": self.price, "from_unit": from_unit, "to_unit": to_unit}, "output": str(cm.exception)})
        

    @patch('core.utils.convert_price.convert_currency')  
    @patch('core.utils.convert_price.convert_unit')    
    def test_13_convert_price_currency_and_unit(self, mock_convert_unit, mock_convert_currency):
        
        #Test the convert_price function to ensure it correctly handles both
        #currency and unit conversions by mocking external dependencies.
        
        _print_object(print_function_name=True)
        mock_convert_currency.return_value = Dec('105.00')  
        mock_convert_unit.return_value = Dec('0.105') 
        
        result = convert_price(self.price, self.valid_currencies["from_currency"], self.valid_currencies["to_currency"], SystemUnit.KG, SystemUnit.GRAM)
        _print_object({"input": {"price": self.price, "from_unit": SystemUnit.KG, "to_unit":  SystemUnit.GRAM,"from_currency":self.valid_currencies["from_currency"],"to_currency":self.valid_currencies["to_currency"]}, "output": Dec("0.105")})
        self.assertEqual(result, Dec('0.105'))
        


