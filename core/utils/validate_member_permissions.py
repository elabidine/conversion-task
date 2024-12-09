        
from core.enums.domain import Domain
from core.models.flexup_model import get_current_member
from django.utils.translation import gettext_lazy as _

from utils.print_object import _print_object


def validate_member_permissions(obj):
        """
        Checks if the current member has the right to save (create or update) this object.
        - Args: obj: The object to be saved
        - Returns: None
        - Raises: PermissionError if the current member does not have the right to save the object.
        - Rules:
            - If the get_current_member returns None, we assume it's a system action, so we allow it (Note: This could be dangerous)
            - If the object has the "account" attribute, the current member must be the owner of the account.
            - If the object has the "client" and "supplier" attributes, the current member must be one of them.
            - The member rights must be in the list of rights for this class of object (based on the domain).
            - If any test fails, a PermissionError is raised.
        """
        current_member = get_current_member()
        
        # Allow system actions if no current member is found
        if not current_member: # We assume it's a system action
            return
        
        # Validate account ownership for objects with an "account" attribute
        if hasattr(obj, "account"):
            if current_member.account != obj.account:
                raise PermissionError(_("You can't create or update a record for another account"))
        
        # Check that the member is active
        if current_member.status != "ACTIVE":
            raise PermissionError(f"Member is currently {current_member.status.label}. Only active member can create or update records.")
        
    
        # Validate party involvement for objects with "client" and "supplier" attributes
        elif hasattr(obj, "client") and hasattr(obj, "supplier"):
            if current_member.account not in [obj.client, obj.supplier]:
                raise ValueError("The current account is not a party to the transaction")
        
        # Validate party involvement for objects with "client" and "supplier" attributes
        elif hasattr(obj, "payee") and hasattr(obj, "payor"):
            if current_member.account not in [obj.payee, obj.payor]:
                raise ValueError("The current account is not a party to the transaction")
        
        # Validate rights based on the object's domain
        domain_tuple_list = Domain.find_by_property("class_name", obj.__class__.__name__)
        if not domain_tuple_list:
            raise PermissionError(
                _(f"No domain rights defined for {obj.__class__.__name__}.")
            )
        domain = Domain(domain_tuple_list[0][0])  # Extract the domain instance from the first tuple in the list

        if current_member.role not in domain.rights:
            raise PermissionError(f"Member {current_member} does not have the required permissions to create or update a {domain.label}")
        # else:
        #     _print_object(f"Member {current_member} has the right to create or update this {domain.label}")
