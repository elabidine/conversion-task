# Price conversion - Django app

> Note to the candidate: this is a template for the README file. Please review and update it as needed once you have completed the test.

This repo contains some code extract from the FlexUp project as a starting point.

It is a simple Django app that allows to convert prices from one currency to another.

## Install

- Windows
```
rye sync
.venv/Scripts/activate
```

Mac
```
rye sync
chmod +x .venv/bin/activate
source .venv/bin/activate
```

## Run app

- `python manage.py runserver` to launch the app from within the virtual environment
- `rye run python manage.py runserver` to launch the app using the rye environment

## Run tests

- `python manage.py test` : run all tests
- `python manage.py test user` : run all tests in user app
- `python manage.py test product` : run all tests in product app
- `python manage.py test product.tests.product` : run all tests in the product file


### Debug prints:
- Change `DEBUG_PRINTS` value in the `.env` to enable/disable debug prints for the _print_object utility function:
  - '0' never,
  - '1' always,
  - 'test' or only when running tests
- To override the `.env` value, you can pass the `DEBUG_PRINTS` value as an environment variable when running tests:
  - `DEBUG_PRINTS=0 python manage.py test` : in the command line
  - `os.environ["DEBUG_PRINTS"] = "0"` : in the test file


## Reset migrations & database

- `python manage.py makemigrations` : Recreate / update migrations 
- `python manage.py migrate` : Apply migration
- `python manage.py shell` : Open python shell


