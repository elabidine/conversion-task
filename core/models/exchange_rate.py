

#from account.models.account import Account, Member
from core.enums.currency import Currency
from core.enums.general import Focus, Visibility
from core.enums.status import Status
from core.models.flexup_enum_field import FlexUpEnumField
from core.models.flexup_model import FlexUpModel, get_current_member
from decimal import Decimal as Dec, ROUND_HALF_UP
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from product.enums import ProductStatuses, SystemUnit, ProductVisibilities
from typing import Optional
from dataclasses import fields


class ExchangeRate(models.Model):
    currency: Currency = FlexUpEnumField(flexup_enum=Currency, verbose_name=_("Currency"), choices=Currency.choices)
    rate: Dec = models.DecimalField(verbose_name=_("Rate"), max_digits=15, decimal_places=6)
    datetime = models.DateTimeField(verbose_name=_("Date"), auto_now_add=True)
    
  
  