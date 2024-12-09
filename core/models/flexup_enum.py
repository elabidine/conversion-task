# -------- core/models/flexup_enum.py
from enum_properties import EnumProperties
from django.utils.translation import gettext_lazy as _

from utils.print_object import _print_object

class ClassPropertyDescriptor:
    """A descriptor that enables defining class properties in the class body.

    This descriptor allows class properties to be defined similarly to instance properties,
    but at the class level rather than instance level.
    """
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, instance, owner):
        return self.fget(owner)


def classproperty(func):
    """Decorator that creates a class-level property.

    Similar to the @property decorator, but works on class methods instead of instance methods.

    Args:
        func: The function to be converted into a class property.

    Returns:
        ClassPropertyDescriptor: A descriptor that handles the class property behavior.
    """
    return ClassPropertyDescriptor(func)


class FlexUpEnum(EnumProperties):
    """Base class for creating enums with additional properties and methods.

    This class extends EnumProperties to provide additional functionality for handling enum values, including validation, filtering, and property-based lookups.

    How to use:
        - you must first declare the property names in the enum class, starting with "label" (do not mention the enum instance name or value)
        - the you declare the enum instances with the values and the properties.

    Example:
        class ExampleEnum(FlexUpEnum):
            label: str
            symbol: str
            level: int

            \# name =  value,  label,    symbol,  level
            ONE =     "O",    "One",    "😅",     1
            TWO =     "T",    "Two",    "⭐",     2
            THREE =   "H",    "Three",  "🍀",     None

    """
    # def __init__(self, *args):
    #     # Extract custom attributes from args and assign them
    #     if len(args) > 1:
    #         self.label = args[1]  # Example to assign label


    @classmethod
    def is_valid(cls, input_value, short_list=None, property_name=None, property_value=None):
        """
        Check if the given input_value is valid for this enum. Optionally filtered by a property (optionally with a value to match) and/or a short_list.

        Args:
            - input_value = The value to check (value or enum instance).
            - short_list = A list of enum values or tuples to filter by.
            - property_name =  The name of the property to filter by.
            - property_value = The value of the property to filter by if none provide, excludes values with None).
            If both property_name and short_list are provided, the value must be in both lists.

        Returns:
            True if the value is valid, False otherwise.
        """
        # Handle None values and attribute errors
        if input_value is None:
            return False

        # Return error if property_value is provided without property_name
        if property_value and not property_name:
            raise ValueError("property_value cannot be provided without property_name")

        # Extract the raw value if input_value is an enum instance
        if isinstance(input_value, cls):
            value = input_value.value
        else:
            value = input_value


        if short_list:
            # Handle both enum instances and (value, label) tuples in short_list
            valid_values_shl = []
            for item in short_list:
                if isinstance(item, cls):
                    valid_values_shl.append(item.value)
                elif isinstance(item, tuple):
                    valid_values_shl.append(item[0])  # Get the value from the tuple

        if property_name:
            if property_value:
                valid_values_prop = [item.value for item in cls if getattr(item, property_name) == property_value]
            else:
                valid_values_prop = [item.value for item in cls if getattr(item, property_name, None) is not None]
        else:
            valid_values = [item.value for item in cls]

        # return true if value is in both lists, if applicable
        if short_list and property_name:
            return value in valid_values_shl and value in valid_values_prop
        elif short_list:
            # print("short_list: ", short_list)
            # print("value: ", value)
            # print("valid_values_shl: ", valid_values_shl)
            return value in valid_values_shl
        elif property_name:
            return value in valid_values_prop
        else:
            return value in valid_values

    # @classmethod
    @classproperty
    def choices(cls):
        return [(item.value, item.label) for item in cls]

    @classmethod
    def allowed_choices(cls, *allowed_values):
        """
        - Return a filtered list of choices (tuples) based on allowed enum values.
        - Args:
            - allowed_values = List of enum instances values to be included in the choices
        - Returns:
            - list of tuples = representing the allowed choices provided
        """
        return [(item.value, item.label) for item in cls if item.name in allowed_values]

    @classmethod
    def filter_choices(cls, property_name):
        """
        - Return a list of choices (tuples) where the given property is not None.
        - Args:
            - property_name: The name of the property to filter by.
        - Returns:
            - list of tuples representing the enums for the allowed choices provided
        """
        return [(item.value, item.label) for item in cls if getattr(item, property_name, None) is not None]

    @classmethod
    def find_by_property(cls, property_name, value):
        """
        Return the list of all enum (tuples) items where the given property has the given value.
        - Args:
            - property_name: The name of the property to filter by.
            - value: The value to filter by.
        - Returns:
            - A list of tuples representing the enums where the property has the given value.
        """
        return [(item.value, item.label) for item in cls if getattr(item, property_name) == value]

    @classmethod
    def get_by_value(cls, value):
        """
        Returns the enum (tuple) item with the given value.
        - Args:
            - value: The value to filter by.
        - Returns:
            - A list of tuples representing the enums with the given value, or None if not found.
        """
        return next((item for item in cls if item.value == value), None)

    def __str__(self):
        return self.value

    def __len__(self):
        return len(self.value)

    # the comparison is based on the order of the items in the list
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            # Get the indices from _member_names_ list
            # print("same class")
            self_idx = self.__class__._member_names_.index(self.name)
            other_idx = self.__class__._member_names_.index(other.name)
            # print(self_idx, ": ", self.name)
            # print(other_idx, ": ", other.name)
            # print(self_idx < other_idx)
            return self_idx < other_idx
        return self.value < other.value
    
    # # use this version if the the comparison is based on name of the items, but this is redundant with the get_first_item utility function
    # def __lt__(self, other):
    #     if self.__class__ is other.__class__:
    #         self_name = self._value2member_map_[self.value].name
    #         other_name = self._value2member_map_[other.value].name
    #         return self_name < other_name
    #     return self.value < other.value
