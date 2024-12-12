# from account.enums import MemberRole
# from account.models.account import Account, Member
from core.enums.currency import Currency
from core.enums.general import Focus, Visibility
from core.enums.status import Status
from core.models.flexup_enum_field import FlexUpEnumField
from core.models.flexup_model import FlexUpModel, get_current_member
from decimal import Decimal as Dec, ROUND_HALF_UP
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.utils import convert_price
from product.enums import ProductStatuses, SystemUnit, ProductVisibilities
from typing import Optional
#from polymorphic.models import PolymorphicManager


class AbstractProduct(FlexUpModel):
    """Abstract base class for product-related models.

    This mixin class provides common fields and methods used by both Product and
    OrderItem models. It handles pricing, tax calculations, and unit measurements.

    Attributes:
        name (str): The name of the product.
        currency (Currency): The currency used for pricing.
        price_excluding_tax (Decimal): Base price without tax.
        tax_rate (Decimal): Tax percentage rate (0-100).
        description (str, optional): Detailed product description.
        system_unit (SystemUnit, optional): Standard system unit of measurement.
        custom_unit (str, optional): Custom unit of measurement if standard doesn't apply.
        price_including_tax (Decimal): Calculated price including tax.
        tax_price (Decimal): Calculated tax amount.
        unit (str): Current unit of measurement (system or custom).
        currency_with_unit (str): Formatted string of currency symbol with unit.

    Raises:
        ValidationError: If both system_unit and custom_unit are provided,
                        if no member is provided, or if member lacks required permissions.
    """

    class Meta:
        abstract = True

# Required input fields
    name: str = models.CharField(max_length=255, verbose_name=_("Product name"))

# Optional fields
    currency: Currency = FlexUpEnumField(flexup_enum=Currency, verbose_name=_("Currency"), choices=Currency.choices, null=True, blank=True)
    price_excluding_tax: Dec = models.DecimalField(max_digits=15, decimal_places=4, verbose_name=_("Price excluding tax"), null=True, blank=True)
    tax_rate: Dec = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Tax rate"), null=True, blank=True)
    description: str = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    system_unit: SystemUnit = FlexUpEnumField(flexup_enum=SystemUnit, verbose_name=_("System unit"), choices=SystemUnit.choices, null=True, blank=True)
    custom_unit: str = models.CharField(max_length=255, verbose_name=_("Custom unit"), null=True, blank=True)

# Properties
    @property
    def price_including_tax(self) -> Dec:
        """ Calculate the price including tax. """
        if self.tax_rate is not None and self.price_excluding_tax:
            price = self.price_excluding_tax * (1 + self.tax_rate / 100)
            return price.quantize(Dec('0.01'), rounding=ROUND_HALF_UP)
        return self.price_excluding_tax

    @property
    def tax_price(self) -> Dec:
        """ Calculate the tax amount."""
        if self.tax_rate is not None and self.price_excluding_tax:
            tax = self.price_excluding_tax * (self.tax_rate / 100)
            return tax.quantize(Dec('0.01'), rounding=ROUND_HALF_UP)
        return Dec('0.00')

    @property
    def unit(self) -> str:
        """ Get the unit of measurement. """
        if self.system_unit:
            return self.system_unit.symbol
        elif self.custom_unit:
            return self.custom_unit
        return ''  # in some cases, no unit is required (for example for funding) then don't display any unit

    @property
    def currency_with_unit(self) -> str:
        """ Get the currency symbol with the unit of measurement. """
        if self.unit:
            return f"{self.currency.symbol}/{self.unit}"
        return f"{self.currency.symbol}"

    @property
    def price_info(self) -> str:
        info = ''
        if self.price_excluding_tax:
            # Format prices with up to 2 decimals, removing trailing zeros
            price_excluding_tax = f"{self.price_excluding_tax:,.2f}".rstrip('0').rstrip('.').replace(',', ' ')
            info += f"{price_excluding_tax} {self.currency_with_unit}"
            if self.tax_rate:
                tax_rate = f"{self.tax_rate:.2f}".rstrip('0').rstrip('.')
                price_including_tax = f"{self.price_including_tax:,.2f}".rstrip('0').rstrip('.').replace(',', ' ')
                info += f" + {tax_rate}% tax = {price_including_tax} {self.currency_with_unit}"
            # else:
            #     info += " excl. tax"
        return info

# Assign values, clean & save
    def clean(self):
        """ Validate the product data. """
        super().clean()
        # force conversion of tax and price_excluding_tax to Decimal and then round to 2 decimals
        if self.tax_rate is not None:
            self.tax_rate = Dec(self.tax_rate).quantize(Dec('0.01'), rounding=ROUND_HALF_UP)
        if self.price_excluding_tax is not None:
            self.price_excluding_tax = Dec(self.price_excluding_tax).quantize(Dec('0.0001'), rounding=ROUND_HALF_UP)
        if self.system_unit and self.custom_unit:
            raise ValidationError(_('You cannot provide both a system unit and a custom unit'))
        # tax rate must be between 0 and 200
        if self.tax_rate is not None and (self.tax_rate < 0 or self.tax_rate > 200):
            raise ValidationError(_('Invalid tax rate'))


# class VisibleProductManager(PolymorphicManager):
#     def get_queryset(self):
#         current_member = get_current_member()
#         all = super().get_queryset()

#         if current_member:
#             # My account's products
#             my_products = all.filter(account=current_member.account)
            
#             # Other account's public & active products
#             public_active_products = all\
#                 .filter(status=Status.ACTIVE, visibility=Visibility.PUBLIC)\
#                 .exclude(account=current_member.account)

#             return my_products | public_active_products
#         else:
#             # If no current member, return all public and active products
#             return all.filter(status=Status.ACTIVE, visibility=Visibility.PUBLIC)


class Product(AbstractProduct):
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

# Required input fields
    # account = models.ForeignKey(Account, verbose_name=_("Account"), on_delete=models.PROTECT, related_name='products', editable=False, null=True, blank=True)

# Optional fields
    status = FlexUpEnumField(flexup_enum=Status, verbose_name=_("Status"), choices=ProductStatuses, default=Status.DRAFT)
    visibility = FlexUpEnumField(flexup_enum=Visibility, verbose_name=_("Visibility"), choices=ProductVisibilities, default=Visibility.PRIVATE)
    focus = FlexUpEnumField(flexup_enum=Focus, verbose_name=_("Focus"), choices=Focus.choices, default=Focus.NORMAL)

    # visible = VisibleProductManager()

# Methods
    def duplicate(self):
        new_product = self
        new_product.name = f"{self.name} (copy)"
        new_product.status = Status.PENDING
        new_product.save()
        return new_product

    def __str__(self):
        # current_member = get_current_member()
        # if current_member and current_member.account != self.account and self.visibility == Visibility.PRIVATE:
        #         return _('Private product')
        
        label = f"{self.name}"
        
        if self.price_info:
            if label:
                label += ", "
            label += self.price_info
        label += f" {self.visibility.symbol}{self.status.symbol}"
        
        # if current_member and current_member.account == self.account:
        #     label += f"{self.focus.symbol}"
        
        return label

    def assign_values(self):
        # current_member = get_current_member()

        # if current_member and not self.account:
        #     self.account = current_member.account
        
        if not self.currency and self.account:
            self.currency = self.account.currency
        
        if self.price_excluding_tax:
            self.price_excluding_tax = round(self.price_excluding_tax, 4)
        
        if self.tax_rate:
            self.tax_rate = round(self.tax_rate, 2)
        
        super().assign_values()
        
        
    def convert_price(self, to_currency:Currency, to_unit:SystemUnit):
        """ - Convert the product's price to a different currency and unit.
        
        - Args:
            to_currency (Currency): The target currency for conversion.
            to_unit (SystemUnit): The target unit for conversion.

        - Returns:
            Product: A new product instance with the converted price, unit, and currency.
        
        -Raises:
            ValidationError: If the Price excluding Tax is not existing or 
        """
        if not self.price_excluding_tax:
            raise ValidationError(_("Price excluding tax must be set to convert the price."))

        # Convert the price using a helper function

        new_price = convert_price(
            self.price_excluding_tax,
            from_currency=self.currency,
            to_currency=to_currency,
            from_unit=self.system_unit or self.custom_unit,
            to_unit=to_unit,
        )
        print("Price", new_price)
        # Create a new Product instance with the converted values
        new_product = Product.objects.create(
            name=self.name,
            currency=to_currency,
            price_excluding_tax=new_price,
            tax_rate=self.tax_rate,
            description=self.description,
            system_unit=to_unit if isinstance(to_unit, SystemUnit) else None,
            custom_unit=None if isinstance(to_unit, SystemUnit) else to_unit,
            status=self.status,
            visibility=self.visibility,
            focus=self.focus,
        )
        return new_product

    def clean(self):
        # current_member = get_current_member()
        
        # if not current_member:
        #     raise ValueError(_("No current member. Cannot create a product without a current member"))

        if not Status.is_valid(self.status, ProductStatuses):
            raise ValidationError(_('Invalid product status'))
        
        # if current_member and current_member.role not in [MemberRole.ADMIN, MemberRole.EDITOR]:
        #     raise PermissionError(_("You don't have the required permissions to create or update a product"))

        # if current_member and self.account and current_member.account != self.account:
        #     raise PermissionError(_("You can't create or update a product from another account"))
        
        super().clean()
