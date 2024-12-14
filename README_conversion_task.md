
# Project Documentation

## Bug Fixes

### **Fix BUG: LIT/MIL Conversion**  
- Fixed an issue where the conversion factor between liters (L) and milliliters (ML) was incorrectly set to `1`.  
- Updated the conversion factor to the correct value of `0.001`.  

## Functions Overview

### `get_exchange_rate` - core/utils/convert_currency
This function checks if the exchange rate for a currency exists in the database and if it is more than 24 hours old. If the rate is outdated or doesn't exist, the function calls `fetch_api_currency` to get the exchange rate for the currency. If the currency exists in the database, it is updated; if not, it is created.

### `fetch_specific_rate_from_api` - core/utils/convert_currency
This function converts each currency to the Euro (EUR) using two third-party APIs (ALPHA and TWELVE). If the first API fails, the second API is used. If both fail to provide a rate, an error is raised.

### `convert_currency` - core/utils/convert_currency
This function retrieves the exchange rates for both the source and target currencies using `get_exchange_rate`. It then performs the conversion by multiplying the source value by the source currency rate and dividing it by the target currency rate.

**Updated:** The `datetime` parameter in this function is now specified as `timezone/datetime`, which matches the field type.

### `convert_unit` - core/utils/convert_unit
This function converts a price from one unit to another.

### `convert_price` - core/utils/convert_price
This function converts a price from one currency and unit to another, using the `convert_unit` and `convert_currency` functions.

### `convert_price` Method - product/models
This method converts a product's price to a different currency and unit.

## Testing

### Product Tests
The tests include debugging and adjustments based on the previous versions. The old tests that existed in this file were debugged and adjusted to work with the latest implementation. Additionally, I have added new tests specifically for the `convert_price` method of the `Product` model, which I have implemented.

To run the tests (you will see only the new tests for the `convert_price` method, including the input and expected output.):
```bash
python manage.py test product.tests.product
```

### Conversion Tests
These tests are related to the `convert_price`, `convert_unit`, and `convert_currency` functions. They validate the full conversion process across different currencies and units.

To run the tests:
```bash
python manage.py test product.tests.conversion
```

### Future Considerations for Fetching Rates with a Specific Date

In the future, if we need to fetch exchange rates for a specific date (other than the current date), the system can be adapted to support this functionality. The current approach compares the stored rate’s datetime with the present moment to determine if it needs updating. If fetching rates for specific historical dates becomes a requirement, we can modify the logic to handle this feature, allowing us to retrieve rates as they were on any given day.