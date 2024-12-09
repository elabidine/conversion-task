""" 
python manage.py test core.tests.complex_status_enum
"""
import os
from django.test import TestCase
from core.enums.status import Status
from core.models.flexup_enum import FlexUpEnum
from utils.print_object import _print_object

from django.test import SimpleTestCase

os.environ["DEBUG_PRINTS"] = "0"

class ComplexStatusEnum(FlexUpEnum):
    """ The list of all available dummy statuses, building on the Status enum """
    priority: int
    group: str
    
    # name            =  value,                    priority,      group
    NEW               =  Status.NEW.value,         1,            "not started"
    DRAFT             =  Status.DRAFT.value,       None,         "not started"
    PENDING           =  Status.PENDING.value,     None,         "not started"
    REJECTED          =  Status.REJECTED.value,    None,         "not started"
    RETRACTED         =  Status.RETRACTED.value,   None,         "not started"
    SIGNED            =  Status.SIGNED.value,      9,            "in progress"
    CONFIRMED         =  Status.CONFIRMED.value,   7,            "in progress"

    # # Declare default values for the inherited properties
    # _init_ = 'value priority group'

    
    # def __init__(self, value, priority, group):
    #     # Access the corresponding Status member using the value
    #     status_member = Status(value)
    #     # Copy attributes from the Status member
    #     self.label = status_member.label
    #     self.symbol = status_member.symbol
    #     self.color = status_member.color
    #     self.description = status_member.description
    #     # Set additional attributes
    #     self.priority = priority
    #     self.group = group
        
    # @property
    # def __str__(self):
    #     return f"{self.name} - {self.priority}"

    @property
    def weight(self) -> int:
        """Calculate weight based on priority"""
        if self.priority is None:
            return None
        return self.priority ** 2
    
    @property
    def label(self):
        # return the label of the corresponding Status member
        return Status(self.value).label
    
    @property
    def symbol(self):
        # return the label of the corresponding Status member
        return Status(self.value).symbol

CSE = ComplexStatusEnum    
DummyStatusShortList = CSE.allowed_choices(CSE.NEW, CSE.DRAFT)

class DummyStatusTestCase(SimpleTestCase):
    def test_dummy_status_inherits_status_properties(self):
        
        _print_object(CSE.NEW, "label", "symbol", "priority", "group", "weight")
        _print_object(CSE.NEW.value)
        _print_object(CSE.choices)
        _print_object(CSE.is_valid("NW"))
        _print_object(CSE.is_valid(CSE.NEW))
        _print_object(DummyStatusShortList)
        _print_object(CSE.filter_choices("priority"))
        _print_object(CSE.find_by_property("priority", 9))
        _print_object(CSE.get_by_value("SI"))
        
        
        # Test that DummyStatus.NEW correctly references Status.NEW properties
        self.assertEqual(CSE.NEW.label, Status.NEW.label)
        self.assertEqual(CSE.NEW.symbol, Status.NEW.symbol)
        self.assertEqual(len(CSE.choices), 7)
        self.assertEqual(CSE.choices, [('NW', 'New'), ('DR', 'Draft'), ('PE', 'Pending'), ('RJ', 'Rejected'), ('RT', 'Retracted'), ('SI', 'Signed'), ('CF', 'Confirmed')])
        self.assertEqual(CSE.choices[0], ('NW', 'New'))
        self.assertEqual(CSE.is_valid("NW"), True)
        self.assertEqual(CSE.is_valid(CSE.NEW), True)
        self.assertEqual(DummyStatusShortList, [('NW', 'New'),  ('DR', 'Draft')])
        self.assertEqual(CSE.filter_choices("priority"), [('NW', 'New'), ('SI', 'Signed'), ('CF', 'Confirmed')])
        self.assertEqual(CSE.find_by_property("priority", 9), [('SI', 'Signed')])
        self.assertEqual(CSE.get_by_value("SI"), CSE.SIGNED)
        
        

    def test_basic_properties(self):
        """Test basic properties inherited from Status"""
        self.assertEqual(CSE.NEW.label, "New")
        self.assertEqual(CSE.NEW.symbol, "🆕")
        self.assertEqual(CSE.DRAFT.label, "Draft")
        self.assertEqual(CSE.DRAFT.symbol, "📄")

    def test_custom_properties(self):
        """Test DummyStatus specific properties"""
        self.assertEqual(CSE.NEW.priority, 1)
        self.assertEqual(CSE.NEW.group, "not started")
        self.assertEqual(CSE.DRAFT.priority, None)
        self.assertEqual(CSE.DRAFT.group, "not started")
        self.assertEqual(CSE.SIGNED.priority, 9)
        self.assertEqual(CSE.SIGNED.group, "in progress")

    def test_weight_computation(self):
        """Test weight property computation"""
        self.assertEqual(CSE.NEW.weight, 1)      # 1^2
        self.assertEqual(CSE.DRAFT.weight, None)   # 5^2
        self.assertEqual(CSE.SIGNED.weight, 81)  # 9^2

    def test_choices(self):
        """Test choices property structure"""
        self.assertEqual(len(CSE.choices), 7)
        self.assertEqual(CSE.choices[0], ('NW', 'New'))
        self.assertEqual(CSE.choices[1], ('DR', 'Draft'))
        self.assertEqual(CSE.choices[5], ('SI', 'Signed'))

    def test_validation(self):
        """Test validation methods"""
        self.assertTrue(CSE.is_valid("NW"))
        self.assertTrue(CSE.is_valid(CSE.NEW))
        self.assertTrue(CSE.is_valid("DR"))
        self.assertFalse(CSE.is_valid("XX"))
        self.assertFalse(CSE.is_valid("INVALID"))

    def test_status_integration(self):
        """Test integration with Status enum"""
        self.assertEqual(CSE.NEW.value, Status.NEW.value)
        self.assertEqual(CSE.DRAFT.value, Status.DRAFT.value)
        self.assertEqual(CSE.SIGNED.value, Status.SIGNED.value)
        self.assertEqual(CSE.NEW.label, Status.NEW.label)
        self.assertEqual(CSE.DRAFT.symbol, Status.DRAFT.symbol)
