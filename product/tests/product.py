# from account.enums import MemberRole, Visibility
# from account.models import Member
#from account.models.individual import Individual
# from account.models.legal_entity import LegalEntity
from core.enums.country import Country
from core.enums.currency import Currency
from core.enums.general import Focus, Visibility
from core.enums.status import Status
from core.models.flexup_model import get_current_member, override_current_member
from decimal import Decimal as Dec
from django.db import Error
from django.test import TestCase
from product.enums import SystemUnit
from product.models import Product

from django.db import transaction
from django.core.exceptions import ValidationError

from utils.print_object import _print_object


class AbstractProductTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        # Given some product details
        cls.all_details = {                    # common all details provided
            "name": "Potatoes",
            "price_excluding_tax": Dec('100.00'),
            "tax_rate": Dec('20.00'),
            "description": "Fresh potatoes!",
            "currency": Currency.DZD,
            "system_unit": SystemUnit.KG,
            "status": Status.ACTIVE,
            "focus": Focus.STARRED,
            "visibility": Visibility.PUBLIC,
        }
        cls.minimum_details = {                    # only required details provided
            "name" : "Computer",
            "price_excluding_tax": Dec('1000.00'),
            "currency": Currency.USD  
        }
        cls.custom_unit_details = {                 # custom unit provided
            "name": "Cake",
            "price_excluding_tax": Dec('5.00'),
            "tax_rate": Dec('10.00'),
            "custom_unit": "portion",
            "currency": Currency.USD
        }
       

    def test_01_create_product_with_all_details(self):
        # Given an editor member of the account, and a full set of product details (see setUpTestData)
        # When the editor creates a product
        #with override_current_member(self.supplier_member):
            potatoes = Product.objects.create(**self.all_details)

            # Then the product is created with the details provided
            self.assertEqual(potatoes.name, "Potatoes")
            self.assertEqual(potatoes.price_excluding_tax, Dec('100.00'))
            self.assertEqual(potatoes.tax_rate, Dec('20.00'))
            self.assertEqual(potatoes.description, "Fresh potatoes!")
            self.assertEqual(potatoes.currency, Currency.JPY)
            self.assertEqual(potatoes.system_unit, SystemUnit.KG)
            self.assertEqual(potatoes.status, Status.ACTIVE)
            #self.assertEqual(potatoes.visibility, Visibility.PUBLIC)
            self.assertEqual(potatoes.focus, Focus.STARRED)
            #self.assertEqual(potatoes.created_by_member, self.supplier_member)

            # # And the default values are assigned correctly
            self.assertEqual(potatoes.custom_unit, None)
            #self.assertEqual(potatoes.account, self.supplier_member.account)
            #self.assertEqual(potatoes.updated_by_member, self.supplier_member)
            #self.assertTrue(potatoes.global_id.startswith("PR-"))

            # And the properties are calculated correctly
            self.assertEqual(potatoes.price_including_tax, Dec('120.00'))
            self.assertEqual(potatoes.tax_price, Dec('20.00'))
            self.assertEqual(potatoes.unit, 'kg')
            self.assertEqual(potatoes.currency_with_unit, '¥/kg')
            self.assertEqual(str(potatoes), 'Potatoes, 100 ¥/kg + 20% tax = 120 ¥/kg 🌍🟢')

    def test_02_create_product_with_only_minimum_details(self):
        # Given an editor member of the account, and some product details with only minimum required fields (see setUpTestData)
        # When the editor creates a product

        computer = Product.objects.create(**self.minimum_details)


        # Then the product is created with the provided details
        self.assertEqual(computer.name, "Computer")
        self.assertEqual(computer.price_excluding_tax, Dec('1000.00'))

        # And the default values are set correctly
        self.assertEqual(computer.currency, Currency.USD)
        self.assertEqual(computer.system_unit, None)
        self.assertEqual(computer.status, Status.DRAFT)
        #self.assertEqual(computer.visibility, Visibility.PRIVATE)
        self.assertEqual(computer.focus, Focus.NORMAL)

        # And the properties are calculated correctly
        self.assertEqual(computer.currency_with_unit, '$')
        self.assertEqual(str(computer), 'Computer, 1 000 $ 🔒📄')


        # When the price information is removed
        computer.price_excluding_tax = None
        #computer.save(member=self.supplier_member)

        # Then the price information does not appear in the string representation
        self.assertEqual(str(computer), 'Computer 🔒📄')

    def test_04_create_product_with_custom_unit(self):
        # Given an editor member of the account, and some product details with a custom unit (see setUpTestData)
        # When the editor creates a product
        cake = Product.objects.create(**self.custom_unit_details)

        # Then the product is created with the given details
        self.assertEqual(cake.name, "Cake")
        self.assertEqual(cake.price_excluding_tax, Dec('5.00'))
        self.assertEqual(cake.tax_rate, Dec('10.00'))
        self.assertEqual(cake.custom_unit, "portion")

        # And the default values are set correctly
        #self.assertEqual(cake.currency, self.supplier_member.account.currency)
        self.assertEqual(cake.system_unit, None)

        # And the properties are calculated correctly
        self.assertEqual(cake.currency_with_unit, '$/portion')
        self.assertEqual(str(cake), 'Cake, 5 $/portion + 10% tax = 5.5 $/portion 🔒📄')

    def test_04_create_product_with_both_units(self):
        # Given an editor member of the account, and some product details with both units (see setUpTestData)
        # When the editor tries to create a product
        with self.assertRaises(ValidationError):
            Product.objects.create(name="Test Product", system_unit=SystemUnit.LIT, custom_unit="Custom Unit")
#
    ## Fab→JB: 2024-11-05 This test does not work.
    ## @skip("This test does not work.")
    #def test_05_create_product_without_member(self):
    #    # Given some product details (see setUpTestData)
    #    # When a product is created without a mprice_excluding_taxember
    #    # Then a validation error is raised
    #    with self.assertRaises(ValueError):
    #        Product.objects.create(name="Test Product", currency=Currency.EUR)

    def test_07_recovering_a_public_product_from_database(self):
        # Given a user who has stored a product in the database
        #with override_current_member(self.supplier_member):
            product = Product.objects.create(**self.all_details)
            # print("---- %s" % p.created_by_member)
            # print("---- %s" % p.account)

            # When the user retrieves the product from the database
            #product = Product.objects.get(name="Potatoes")
            # print("---- %s" % product.created_by_member)
            # print("---- %s" % product.account)

            # Then the product is retrieved with the correct details
            self.assertEqual(str(product), 'Potatoes, 100 ¥/kg + 20% tax = 120 ¥/kg 🌍🟢')

        # When a user from another account tries to retrieve the public and available product
       # with override_current_member(self.other_member):
            # print("\nWith other user")
            # print('get_current_member() → ', get_current_member())
            product = Product.objects.get(name="Potatoes")
            # print('product.__dict__ before save → ', product.__dict__)

            # Then the product is retrieved successfully
            self.assertEqual(str(product), 'Potatoes, 100 ¥/kg + 20% tax = 120 ¥/kg 🌍🟢')

        # But if the product visibility is changed **by supplier** to private
        #with override_current_member(self.supplier_member):
            #product.visibility = Visibility.PRIVATE
            # print()
            # print("-- before save --")
            # print('get_current_member() → ', get_current_member())
            # #print('product.__dict__ before save → ', product.__dict__)
            # print(">>>> %s" % product)
            # print(">>>>>> %s" % product.visibility)
            # print(">>>>>> %s" % product.account.__class__)
            # print(">>>>>> %s" % self.supplier_member.account.__class__)
            product.save()
            # print('product.__dict__ after save → ', product.__dict__)

        # The the supplier can still retrieve the product
            #product = Product.objects.get(name="Potatoes")
            #self.assertEqual(str(product), 'Potatoes, 100 ¥/kg + 20% tax = 120 ¥/kg 🔒🟢⭐')

    # Fab→JB: 2024-11-05 This test does not work.
    # @skip("This test does not work.")
    def test_08_updating_product(self):
        # Given a user who has stored a product in the database
        #with override_current_member(self.supplier_member):
            Product.objects.create(**self.all_details)

            # When the user updates the product
            product = Product.objects.get(name="Potatoes")
            product.name = "Sweet potatoes"
            product.save()

            # Then the product is updated correctly
            product = Product.objects.get(name="Sweet potatoes")
            self.assertEqual(str(product), 'Sweet potatoes, 100 ¥/kg + 20% tax = 120 ¥/kg 🌍🟢')

# removed for the assignment

    def test_10_prices_with_many_decimals(self):

         # Given a member editor of an active account
         #with override_current_member(self.supplier_member):
             # When the user creates a product with a price & tax rate that has many decimals
             product = Product.objects.create(name="Test Product", price_excluding_tax=Dec('100.1234'), tax_rate=Dec('20.12'),currency = Currency.USD)
             # Then the product price & tax rate is stored and displayed with 2 decimals
             self.assertEqual(product.price_excluding_tax, Dec('100.12'))
             self.assertEqual(product.tax_rate, Dec('20.12'))
             self.assertEqual(product.price_including_tax, Dec('120.26'))
             self.assertEqual(str(product), 'Test Product, 100.12 $ + 20.12% tax = 120.26 $ 🔒📄')
             # When the price & tax rate that has less than 2 decimals, the decimals are padded
             product.price_excluding_tax = Dec('105.74')
             product.tax_rate = Dec('15.00')
             product.save()
             # Then the product price & tax rate is displayed with with up to 2 decimals, or less if trailing zeros
             self.assertEqual(product.price_including_tax, Dec('121.60'))
             self.assertEqual(str(product), 'Test Product, 105.74 $ + 15% tax = 121.6 $ 🔒📄')

    # # def test_11_viewer_member_cannot_create_or_update_product(self):
    #     _print_object(print_function_name=True)        
    #     Given viewer member of a active supplier account
    #     viewer = Member.objects.create(account=self.supplier_account, user=self.other_user, role=MemberRole.VIEWER)
    #     _print_object(viewer, "account", "user", "status")
        
    #     with override_current_member(viewer):
    #         When the viewer tries to create a product
    #         Then a validation error is raised
    #         with self.assertRaises(PermissionError):
    #             Product.objects.create(name="Test Product", price_excluding_tax=100.00)

    #     Given a product created by an editor member
    #     with override_current_member(self.supplier_member):
    #         product = Product.objects.create(name="Test Product", price_excluding_tax=100.00)

    #     with override_current_member(viewer):
    #         When the viewer tries to update the product
    #         Then a validation error is raised
    #         with self.assertRaises(PermissionError):
    #             product.name = "Updated Product"
    #             product.save()

    def test_12_product_with_invalid_values(self):
        # Given an editor member of the account
        #with override_current_member(self.supplier_member):
            # When the user tries to create a product with an invalid tax rate, he gets an error
            with self.assertRaises(ValidationError):
                   Product.objects.create(name="Test Product", price_excluding_tax=100.00, tax_rate=-20.00)

            # When the user tries to create a product with an invalid currency, he gets an error
            with self.assertRaises(ValidationError):
                with transaction.atomic():
                   Product.objects.create(name="Test Product", price_excluding_tax=100.00, currency="invalid")

            # When the user tries to create a product with an invalid system unit, he gets an error
            with self.assertRaises(ValidationError):
                with transaction.atomic():
                    Product.objects.create(name="Test Product", price_excluding_tax=100.00, system_unit="invalid")

            # When the user tries to create a product with an invalid status, he gets an error
            with self.assertRaises(ValidationError):
                with transaction.atomic():
                    Product.objects.create(name="Test Product", price_excluding_tax=100.00, status="invalid")

            # When the user tries to create a product with an invalid focus, he gets an error
            with self.assertRaises(ValidationError):
                with transaction.atomic():
                    Product.objects.create(name="Test Product", price_excluding_tax=100.00, focus="invalid")

            # When the user tries to create a product with an invalid visibility, he gets an error
            with self.assertRaises(ValidationError):
                with transaction.atomic():
                    Product.objects.create(name="Test Product", price_excluding_tax=100.00, visibility="invalid")
                    
    def test_13_convert_to_different_currency_and_unit(self):
        
        _print_object(print_function_name=True)
        
        potatoes = Product.objects.create(**self.all_details)
        converted_product = potatoes.convert_price(to_currency=Currency.USD, to_unit=SystemUnit.GRAM)
        self.assertEqual(converted_product.currency, Currency.USD)
        self.assertEqual(converted_product.system_unit, SystemUnit.GRAM)
        
        _print_object({"input": {**self.all_details}, "output":{converted_product.system_unit,converted_product.currency,converted_product.name,converted_product.price_excluding_tax}})

