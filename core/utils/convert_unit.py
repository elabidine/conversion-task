# ------- core/utils/convert_currency.py
 
from decimal import ROUND_HALF_UP, Decimal
from gettext import gettext as _

from django.forms import ValidationError
from product.enums import SystemUnit

# Not yet implemented
    
def convert_unit(price: Decimal, from_unit, to_unit=None) -> Decimal:
    """
    Convert a price from one unit to another.
    
    Args:
        price: The price to convert.
        from_unit: The source unit (can be a system or custom unit).
        to_unit: The target unit (can be a system or custom unit).

    Returns:
        The converted price.

    Raises:
        ValidationError: If either unit is invalid or conversion is not possible.
    """
    # Return the original price if units are the same or target unit is not provided
    if from_unit == to_unit or not to_unit:
        return price

    if isinstance(from_unit, SystemUnit) and isinstance(to_unit, SystemUnit):
        # Check if both units are of the same dimension
        if from_unit.dimension != to_unit.dimension:
            raise ValidationError(_(f"Cannot convert between units of different dimensions: {from_unit} and {to_unit}."))
        
        # Convert price to target unit
        converted_price = (Decimal(price) * Decimal(to_unit.units_to_base)) / Decimal(from_unit.units_to_base)
        return Decimal(converted_price.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP))


    # Handle custom units (we assume conversion is not possible)
    raise ValidationError(_(f"Cannot convert between custom units or between system and custom units: {from_unit} and {to_unit}."))
