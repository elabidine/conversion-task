#  --------- core/models/flexup_enum_field.py
from typing import Any
from django.db import models
from django.forms import ValidationError


class FlexUpEnumField(models.CharField):
    description = "A FlexUpEnum field"

    def __init__(self, flexup_enum, *args, **kwargs):
        self.flexup_enum = flexup_enum
        max_length = max(len(str(item.value)) for item in flexup_enum)
        if 'max_length' in kwargs:
            kwargs.pop('max_length', None)

        super().__init__(*args, max_length=max_length, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['flexup_enum'] = self.flexup_enum

        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        if value is not None:
            for choice in self.flexup_enum:
                if choice.value == value:
                    return choice

        return None


#     def to_python(self, value): # Origina version
#         if not isinstance(value, str) and value in self.flexup_enum:
#             return value
#
#         for choice in self.flexup_enum:
#             if choice.value == value:
#                 return choice
#
#         return None

    def to_python(self, value):
        if isinstance(value, self.flexup_enum):
            return value
        if value is None:
            return None
        enum_value = self.flexup_enum.get_by_value(value)
        if enum_value is not None:
            return enum_value
        raise ValidationError(f"Invalid value '{value}' for field {self.name}. Must be one of {[item.value for item in self.flexup_enum]}")


    def get_prep_value(self, value):
        if value is None:
            return None
        # If it's already an enum instance
        if isinstance(value, self.flexup_enum):
            return value.value

        # If it's a string, try to find matching enum
        enum_value = self.flexup_enum.get_by_value(value)
        if enum_value is not None:
            return enum_value.value

        raise ValueError(f"Invalid value '{value}' for field {self.name}. Must be one of {[item.value for item in self.flexup_enum]}")

        # return str(value)