from decimal import ROUND_HALF_UP, Decimal
from core.utils import convert_price, convert_unit
from product.enums import SystemUnit
from core.enums.currency import Currency
from django.test import TestCase

from utils.print_object import _print_object

        
    # to be completed by the candidate

class TestConvertPrice(TestCase):
    def test_convert_currency_and_unit(self):
        _print_object(print_function_name=True)
        result = convert_price(Decimal("100"), from_currency=Currency.EUR, to_currency=Currency.USD, from_unit=SystemUnit.KG, to_unit=SystemUnit.GRAM)
        self.assertEqual(result, Decimal("105590.00"))

    def test_convert_currency_only(self):
        _print_object(print_function_name=True)
        result = convert_price(price=Decimal("100"), from_currency=Currency.EUR, to_currency=Currency.USD, from_unit=SystemUnit.KG)
        self.assertEqual(result,Decimal("105.59")) 
        
        

    def test_convert_unit_only(self):
        _print_object(print_function_name=True)
        result = convert_price(Decimal("100"), from_currency=Currency.EUR, to_currency=Currency.EUR, from_unit=SystemUnit.KG, to_unit=SystemUnit.GRAM)
        self.assertEqual(result, Decimal("100000"))  

    # def test_invalid_currency(self):
    #     with self.assertRaises(ValueError):
    #         convert_price(Decimal("100"), from_currency=Currency.EUR, to_currency="INVALID", from_unit=SystemUnit.KG, to_unit=SystemUnit.GRAM)

    def test_invalid_unit(self):
        _print_object(print_function_name=True)
        with self.assertRaises(ValueError):
            convert_price(Decimal("100"), from_currency=Currency.EUR, to_currency=Currency.USD, from_unit=SystemUnit.KG, to_unit="invalid_unit")
            
    def test_convert_unit(self):
        _print_object(print_function_name=True)
        result = convert_unit(Decimal("40"), from_unit=SystemUnit.GRAM, to_unit=SystemUnit.KG)
        self.assertEqual(result,Decimal("0.04"))
