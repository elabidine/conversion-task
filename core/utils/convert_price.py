from decimal import ROUND_HALF_UP, Decimal

from django.forms import ValidationError

from core.utils import convert_currency, convert_unit
from product.enums import SystemUnit


def convert_price(price: Decimal, from_currency, to_currency=None, from_unit=None, to_unit=None) -> Decimal:
    """ - Convert a price from one currency and unit to another.
    
    - Args:
        price: The price to convert.
        from_currency: The source currency (can be an instance of Currency).
        to_currency: The target currency (can be an instance of Currency, optional).
        from_unit: The source unit (can be a SystemUnit or custom unit, optional).
        to_unit: The target unit (can be a SystemUnit or custom unit, optional).

    - Returns:
        The converted price, accounting for both currency and unit.

    """
    
    # Convert currency if source and target currencies are different
    price_in_target_currency = convert_currency(price, from_currency, to_currency)

    # Convert units if source and target units are different
    price_in_target_unit = convert_unit(price_in_target_currency, from_unit, to_unit)

    return price_in_target_unit    

def convert_unit(price: Decimal, from_unit, to_unit=None) -> Decimal:
    """ - Convert a price from one unit to another.
    
    - Args:
        price: The price to convert.
        from_unit: The source unit (can be a system or custom unit).
        to_unit: The target unit (can be a system or custom unit).

    - Returns:
        The converted price.

    - Raises:
        ValidationError: If either unit is invalid or conversion is not possible.
    """
    # Return the original price if units are the same or target unit is not provided
    if from_unit == to_unit or not to_unit:
        return price

    # Handle system units
    if isinstance(from_unit, SystemUnit) and isinstance(to_unit, SystemUnit):
        # Check if both units are of the same dimension
        if from_unit.dimension != to_unit.dimension:
            raise ValidationError(f"Cannot convert between units of different dimensions: {from_unit} and {to_unit}.")
        
        # Convert price to target unit
        converted_price = (price * Decimal(to_unit.units_to_base)) / Decimal(from_unit.units_to_base)
        return converted_price.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)


    # Handle custom units (we assume conversion is not possible)
    raise ValidationError(f"Cannot convert between custom units or between system and custom units: {from_unit} and {to_unit}.")