from django.test import TestCase
from contract.enums.contract import ContractStatus
from core.enums.status import Status
from core.models.flexup_enum import FlexUpEnum
from utils.print_object import _print_object


class MockEnum(FlexUpEnum):
    label: str
    symbol: str
    level: int

    # name =  value,  label,    symbol,   level
    ONE =     "O",    "One",    "😅",    1
    TWO =     "T",    "Two",    "⭐",    2
    THREE =   "H",    "Three",  "🍀",    None

MK = MockEnum

ShortList1 = MockEnum.allowed_choices(MK.ONE, MK.TWO)
ShortList2 = MockEnum.filter_choices("level")
ShortList3 = MockEnum.allowed_choices(MK.ONE, MK.THREE)


class TestFlexUpEnum(TestCase):
    """Test suite for FlexUpEnum functionality."""

    @classmethod
    def setUpTestData(cls):
        """Set up data for all test methods."""

        # Create tuples once for all tests
        cls.tuple_one = (MK.ONE.value, MK.ONE.label)
        cls.tuple_two = (MK.TWO.value, MK.TWO.label)
        cls.tuple_three = (MK.THREE.value, MK.THREE.label)

    def test_enum_instantiation(self):
        """Test basic enum instantiation and properties."""
        self.assertEqual(MK.ONE.value, 'O')
        self.assertEqual(MK.ONE.label, 'One')
        self.assertEqual(MK.ONE.symbol, '😅')
        self.assertEqual(MK.ONE.level, 1)

    def test_choices(self):
        """Test the choices class property."""
        expected_choices = [
            self.tuple_one,
            self.tuple_two,
            self.tuple_three
        ]
        self.assertEqual(MK.choices, expected_choices)

    def test_allowed_choices(self):
        """Test the allowed_choices method."""
        expected_choices = [self.tuple_one, self.tuple_two]
        self.assertEqual(
            MK.allowed_choices(MK.ONE, MK.TWO),
            expected_choices
        )

    def test_filter_choices(self):
        """Test filtering choices by property."""
        expected_choices = [self.tuple_one, self.tuple_two]
        self.assertEqual(MK.filter_choices("level"), expected_choices)

    def test_find_by_property(self):
        """Test finding choices by property value."""
        expected_choices = [self.tuple_two]
        self.assertEqual(
            MK.find_by_property("symbol", "⭐"),
            expected_choices
        )

    def test_str_representation(self):
        """Test string representation."""
        self.assertEqual(str(MK.ONE), "O")
        self.assertEqual(str(MK.TWO), "T")
        self.assertEqual(str(MK.THREE), "H")

    def test_is_valid_method(self):
        """Test the is_valid_value method."""
        # Test with raw values
        self.assertTrue(MK.is_valid('O'))
        self.assertTrue(MK.is_valid('T'))
        self.assertTrue(MK.is_valid('H'))
        self.assertFalse(MK.is_valid('X'))
        self.assertFalse(MK.is_valid('🍀'))

        # Test with enum instances
        self.assertTrue(MK.is_valid(MK.ONE))
        self.assertTrue(MK.is_valid(MK.TWO))
        self.assertTrue(MK.is_valid(MK.THREE))

        # Test None values
        self.assertFalse(MK.is_valid(None))
        foo = None
        self.assertFalse(MK.is_valid(foo))

        # Test with raw values and with property filtering
        self.assertTrue(MK.is_valid('O', property_name='level'))
        self.assertTrue(MK.is_valid('T', property_name='level'))
        self.assertFalse(MK.is_valid('H', property_name='level'))

        # Test with raw values and with property filtering - using positional arguments
        self.assertTrue(MK.is_valid('O', None, 'level'))
        self.assertTrue(MK.is_valid('T', None, 'level'))
        self.assertFalse(MK.is_valid('H', None, 'level'))

        # Test with raw valueswith property filtering and value
        self.assertTrue(MK.is_valid('T', None,'symbol', '⭐'))
        self.assertFalse(MK.is_valid('O', None, 'symbol', '⭐'))
        self.assertTrue(MK.is_valid('H', None,'symbol', '🍀'))

        # Tests with instances and property filtering
        self.assertTrue(MK.is_valid(MK.ONE, None,'level'))
        self.assertTrue(MK.is_valid(MK.TWO, None,'level', 2))
        self.assertFalse(MK.is_valid(MK.THREE, None,'level'))
        self.assertFalse(MK.is_valid(MK.TWO, None,'level', 3))

        # Test with values & instances and shortlist
        self.assertTrue(MK.is_valid('O', ShortList1))
        self.assertTrue(MK.is_valid(MK.ONE, ShortList1))
        self.assertTrue(MK.is_valid('O', ShortList2))
        self.assertTrue(MK.is_valid(MK.ONE, ShortList2))
        self.assertFalse(MK.is_valid('H', ShortList2))

        # Test with values & instances and shortlist and property together
        self.assertTrue(MK.is_valid('O', ShortList1, 'level', 1 ))
        self.assertTrue(MK.is_valid(MK.ONE, ShortList1, 'level', 1))
        self.assertFalse(MK.is_valid('O', ShortList1, 'level', 2))
        self.assertFalse(MK.is_valid('H', ShortList1, 'label', 'Three'))
        self.assertTrue(MK.is_valid('O', ShortList1, 'level'))
        self.assertFalse(MK.is_valid('H', ShortList3, 'level'))
        self.assertTrue(MK.is_valid('H', ShortList3, 'label'))

    def test_is_valid_satus(self):
        contract_status = Status.NEW
        _print_object(contract_status)
        _print_object(ContractStatus.choices)
        self.assertEqual(Status.is_valid(contract_status), True)
        self.assertEqual(Status.is_valid(contract_status, ContractStatus.choices), True)
        
        
""" 
python manage.py test core.tests.flexup_enum.TestFlexUpEnum.test_is_valid_satus
"""
