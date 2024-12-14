from decimal import ROUND_HALF_UP, Decimal

from django.forms import ValidationError

from core.utils import convert_currency, convert_unit
from product.enums import SystemUnit
from core.enums.currency import Currency


def convert_price(price: Decimal, from_currency:Currency, to_currency:Currency=None, from_unit:SystemUnit=None, to_unit:SystemUnit=None) -> Decimal:
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

