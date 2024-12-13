# ------- core/utils/convert_currency.py
import requests
from decimal import Decimal
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.enums.currency import Currency
from datetime import timedelta
from core.models.exchange_rate import ExchangeRate
from decimal import Decimal , ROUND_HALF_UP

from utils.print_object import _print_object

        
# Not yet implemented
def convert_currency(price:Decimal, from_currency: Currency, to_currency: Currency = None,date=None) -> Decimal:
    
    """ - Convert a price (price or amount) from one currency to another. 
    - Args:
        - price: The price to convert.
        - from_currency: The currency to convert from.
        - to_currency: The currency to convert to.
        - date: The date to use for the conversion rate. If None, the current date is used.
    - Returns:
        - The converted price if both currencies are different
        - The original price if either currency is None, or if they are the same.
    - Raises:
        - ValidationError: If the source currency is not provided.
        - ValidationError: If either provided currency is invalid.
    """
    if not from_currency:
        raise ValidationError(_('The source currency must be provided.'))
    
    if not to_currency or from_currency == to_currency:
        return price
    
    if not isinstance(from_currency, Currency) or not isinstance(to_currency, Currency):
        raise ValidationError(_('One or both provided currencies are invalid.'))
    
    else:
            # Get exchange rates for the source and target currencies
            from_rate = get_exchange_rate(from_currency)
            to_rate = get_exchange_rate(to_currency)    
            # Convert the value

            converted_value = Decimal((price / from_rate) * to_rate).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
            
            return converted_value

def get_exchange_rate(currency: Currency) -> Decimal:
    
    """ - Retrieve the exchange rate for a given currency. Fetch from the API if not in the database
    or if the stored rate is outdated.

    - Args:
        currency (Currency): The currency for which the rate is required.

    - Returns:
        Decimal: The exchange rate.

    """
    if currency.value == "EUR":
        return Decimal(1)  # EUR is the base currency

    # Try to find the rate in the database
    try:
        rate_data = ExchangeRate.objects.get(currency=currency)
        if rate_data.datetime > timezone.now() - timedelta(hours=24):
            # Rate is fresh, return it
            return rate_data.rate
    except ExchangeRate.DoesNotExist:
        pass  

    # Fetch the rate from the external API
    rate = fetch_specific_rate_from_api(currency)

    # Store the rate in the database
    ExchangeRate.objects.update_or_create(
        currency=currency,
        defaults={
        'rate': Decimal(rate),
        'datetime':timezone.now  # These are the fields to update or create
    }
    )
    return Decimal(rate).quantize(Decimal('0.000001'),rounding=ROUND_HALF_UP)

def fetch_specific_rate_from_api(currency: Currency) -> Decimal:
    """ - Fetch the exchange rate for a specific currency from an external API.
              Use two api calls to fetch the rate and minmize request    

    - Args:
        currency (str): The currency for which the rate is required.

    - Returns:
        Decimal: The exchange rate.

    - Raises:
        RuntimeError: If the API request fails or the currency is invalid.
    """
    API_URL_ALPHA = "https://www.alphavantage.co/query" 
    BASE_CURRENCY = "EUR"
    API_KEY_ALPHA = "0O8QML1RVJW8JVXV"
    FUNCTION="CURRENCY_EXCHANGE_RATE"

    try:
        response = requests.get(API_URL_ALPHA, params={"function":FUNCTION,"apikey": API_KEY_ALPHA,"from_currency": currency.value, "to_currency": BASE_CURRENCY})
        response.raise_for_status()  # Raise an error for HTTP errors
        
        data = response.json()
        
        rate = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
        
        return Decimal(rate).quantize(Decimal('0.000001'),rounding=ROUND_HALF_UP)
    
    except (requests.RequestException, KeyError) as e:
        _print_object(f"Failed to fetch rate for {currency}: {e} with ALPHA API")
 
    API_URL_TWELVE = f"https://api.twelvedata.com/exchange_rate"
    API_KEY_TWELVE="b2246d7458cd463b819b23449c357377"
    
    try:
        response = requests.get(API_URL_TWELVE, params={"apikey":API_KEY_TWELVE,"symbol":f"{currency.value}/{BASE_CURRENCY}"})
        
        response.raise_for_status()  # Raise an error for HTTP errors
        data = response.json()
        
        if "rate" in data:
            return Decimal(data["rate"]).quantize(Decimal('0.000001'),rounding=ROUND_HALF_UP)
        
    except (requests.RequestException, KeyError) as e:
            raise RuntimeError(f"Failed to fetch rate for {currency}: {e} with TWELVE API")
