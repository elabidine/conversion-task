from core.enums.domain import Domain
from core.enums.status import Status
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel
from uuid import uuid4
import threading

local = threading.local()


class CurrentMemberMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'member'): # Implementation of current member TBD
            set_current_member(request.member)
        response = self.get_response(request)
        clear_current_member()

        return response


def get_current_member():
    # """ Get the current member """
    # return getattr(local, 'member', None)
    return None


def get_active_user(user=None):
    # """ Get the active user for the current member or the provided user """
    # if user is None:
    #     member = get_current_member()
    #     if not member or not member.user:
    #         raise ValueError(_("A user must be provided"))
    #     user = member.user
    #     if not user.is_active:
    #         raise ValueError(_("The user is not active"))
    # return user
    return None


def get_active_account(account=None):
    # """ Get the active account for the current member or the provided account """
    # if account is None:
    #     member = get_current_member()
    #     if not member:
    #         raise ValueError(_("An account must be provided"))
    #     account = member.account
    #     if not account.status == Status.ACTIVE:
    #         raise ValueError(_("The account must be active"))
    # return account
    return None


def set_current_member(member):
    # local.member = member
    pass


def clear_current_member():
    # if hasattr(local, 'member'):
    #     del local.member
    pass
        


class FlexUpModel(PolymorphicModel):
    class Meta:
        abstract = True

# # Optional input fields
#     created_by_member = models.ForeignKey("account.Member", verbose_name=_("Created by member"), on_delete=models.PROTECT, related_name='created_%(class)s_set', blank=True, null=True)
#     updated_by_member = models.ForeignKey("account.Member", verbose_name=_("Last updated by member"), on_delete=models.PROTECT, related_name='updated_%(class)s_set', blank=True, null=True)

# # Calculated fields
#     created_datetime = models.DateTimeField(verbose_name=_("Created date"), auto_now_add=True)
#     updated_datetime = models.DateTimeField(verbose_name=_("Last updated date"), auto_now=True)
#     reference_id = models.CharField(max_length=8, verbose_name=_("Global ID"), blank=True, null=True) # unique=True, db_index=True

# # Properties
#     @property
#     def global_id(self) -> str:
#         return self.class_id + "-" + self.reference_id
    
#     # static class-level caching of the class_id
#     _class_id = None
    
#     @property
#     def class_id(self) -> str:
#         if self._class_id is None:
#             class_name = self.__class__.__name__
#             class_codes = Domain.find_by_property('class_name', class_name)
#             if class_codes:
#                 class_code = class_codes[0][0]
#             else:
#                 class_code = "XX"
            
#             self._class_id = class_code
        
#         return self._class_id

# # Methods
#     @staticmethod
#     def _generate_unique_reference_id(size=8):
#         return str(uuid4()).upper()[:size]
    
#     def assign_reference_id(self):
#         """ Generate a unique reference ID for the record """
#         if not self.reference_id:
#             reference_id = self._generate_unique_reference_id()
#             while self.__class__.objects.filter(reference_id=reference_id).exists():
#                 reference_id = self._generate_unique_reference_id()
#             self.reference_id = reference_id

#     def assign_values(self):
#         if not self.reference_id:
#             self.assign_reference_id()

#         now = timezone.now()
#         if not self.pk: # Creation
#             if not self.created_by_member:
#                 self.created_by_member = get_current_member()
#                 self.created_datetime = now

#         if not self.updated_by_member:
#             self.updated_by_member = get_current_member()
#             self.updated_datetime = now
    
#     def clean(self):
#         return super().clean()

#     def save(self, *args, **kwargs):
#         self.assign_values()
#         self.full_clean()
        
#         if 'member' in kwargs:
#             kwargs.pop('member')

#         super().save(*args, **kwargs)


# Context manager for CLI & tests
class override_current_member:
    def __init__(self, member):
        self.member = member
        self.previous_member = None

    def __enter__(self):
        self.previous_member = get_current_member()
        set_current_member(self.member)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.previous_member is not None:
            set_current_member(self.previous_member)
        else:
            clear_current_member()
