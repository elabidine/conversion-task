# Django Price Converter - Practical Test - Instructions for the candidate

_Fabrizio Nastri, Dec 2024_

### Description

This repo provides the scaffolding for a simple app designed to test:

- your knowledge of:
  - Django,
  - APIs,
- your ability to read and understand:
  - existing code developed by someone else
  - the specifications of a given ticket / task
- your ability to:
  - fulfill the ticket requirements / specifications
  - write clean and maintainable code
  - to follow the coding style and guidelines of the existing codebase
  - to write and pass tests
  - to handle / debug legacy code

This test does not require you to build any front end / pages, only the backend logic and the tests.

### Installation

> Note: this repo contains some code extract from the FlexUp project as a starting point. 
> Some apps have not been copied (accounts, contracts, orders, etc.). 
> Some references to these apps and models have been commented out in the code.
> You will need to finish cleaning up the code and remove / comment out some references to these other apps & models in your code before you can run it.

- `rye sync` : to create a virtual environment in the root folder and install the dependencies 
- to activate the virtual environment using a build in script
  - `.venv\Scripts\activate` : for Windows
  - `source .venv/bin/activate` : for Mac / Linux
- `python manage.py makemigrations` : to create the migrations
- `python manage.py migrate` : to apply the migrations
- `python manage.py runserver` : to run the server

### Usage

> There are no views or templates in this app. The homepage is just there to show that the app is running.

- Open browser on http://localhost:8000/ to see the homepage


### App specifications / coding exercise

- The main models / enums in this app are:
  - `Product` model: which inherits from the `AbstractProduct` and contains the product details
  - `ExchangeRate` model (see core.models): which contains the currency conversion rates
  - `SystemUnit` a `FlexUpEnum`: which contains the system units and their conversion rates
  - `Currency` a `FlexUpEnum`: which contains the currency codes, names and symbols
  - `FlexUpEnum` is a custom enum that can store some extra properties
- `Product`:  in this exercise, we will only be interested in the following `Product` fields:
  - `price_excluding_tax` : a decimal field (15 digits, 4 decimals)
  - `currency` : a `FlexUpEnum`, containing the currency code, name and symbol
  - `system_unit` : a `FlexUpEnum`, containing the unit code, name, dimension and conversion_to_base 
  - `custom_unit` : a string
- `ExchangeRate`: contains the following fields:
  - `currency` : a `FlexUpEnum`
  - `rate` : a decimal field (15 digits, 6 decimals)
  - `datetime` : a datetime field
- Currency conversion
  - To populate the `ExchangeRate` model, you will need to fetch the conversion rates from an external API
  - You only fetch and store the conversion rates when needed, to limit the number of API calls
  - The base currency is the Euro (EUR), which has a conversion rate of 1
  - All the other currency rates are stored as a conversion rate to the Euro (eg: 1 USD = 0.85 EUR, 1 JPY = 0.007874 EUR)
- System units have the following properties:
    - `value` : a 3-character string, stored in the database
    - `dimension`: a `FlexUpEnum`, containing the dimension of the unit
    - `conversion_to_base`: a float, containing the conversion rate to the base unit (eg: 1 MG = 0.000001 KG)


### Features:

- You need to create and test 3 functions:
  - `convert_currency`
    - This function should take a price, a source currency, and a target currency, and return the price converted to the target currency.
    - Return the input price if:
      - the source and target currency are the same
      - the target currency is not provided (we assume its the same as the source currency)
    - For the source and for target currency, the rate should be as follows:
      - if the currency is EUR, the rate is 1
      - else, the conversion rate should first be searched in the database:
        - if the rate is not found for that currency:
          - the rate should be fetched from an external API and stored in the database with the date and time
        - if the rate is found:
          - if the datetime is less that 24 hours old, the rate should be used
          - else, a new rate should be fetched from the external API and stored in the database with the date and time
    - Raise an exception if:
      - either the source currency is not provided
      - if either currency is not a valid currency
      - the fetching of the rate from the external API fails
  
  - `convert_unit`
    - This function should take an price, a source unit, and a target unit, and return the price converted to the target unit.
    - The source unit and the target unit can be both be either:
      - a system unit, or
      - a custom unit
    - Return the input price if:
      - the source and target unit are the same
      - the target unit is not provided (we assume its the same as the source unit)
    - If the target unit is different from the source unit:
      - The price should be converted using the conversion rate of the units from the `SystemUnit` enum.
      - Raise an exception if:
        - either unit is not a valid system unit
        - both are system units but have a different dimensions

  - `convert_price`
    - This function should take a price, a source currency, a target currency, a source unit, and a target unit, and return the price converted to the target currency and unit.
    - It should use the `convert_currency` and `convert_unit` functions to do the conversion

- In addition, you should add a `convert_price` method to the `Product` model that simplifies the conversion:
  - it takes the target currency and unit as parameters
  - it returns a new product, with all the fields copied from the original product, except:
    - the price is converted to the target currency and unit
    - the currency and unit are set to the target currency and unit
    - it is stored in the database with a new id

### Tests

- You need to write tests for the 3 functions and 1 method above
- Each test should test the function with different scenarios, including all the edge cases
- Use the `_print_object` utility function in your tests to print
  - the name of each test
  - the input parameters
  - the output
