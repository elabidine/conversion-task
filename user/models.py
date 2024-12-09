from core.enums.status import Status, StatusShortList
from core.models.flexup_enum_field import FlexUpEnumField
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        """
        Create and return a user with an email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser,PermissionsMixin):
    """ Custom user model that supports using email instead of username.

    Fields:
        - email: Email address
        - is_superuser: Boolean to indicate if the user is a superuser
        - is_staff: Boolean to indicate if the user is a staff member
        - main_account: The Individual associated with the user
        - status: The status of the user
        - is_email_verified: Boolean to indicate if the email has been verified
        - joined_datetime: The date the user joined the platform

    Properties:
        - is_active: Boolean to indicate if the user is active (status is ACTIVE and email is verified)

    Methods:
        - login_with_user_data: Authenticate a user with email and password
        - verify_email: mark the email as verified and set the user status to ACTIVE
        - close: Close the user account
        - clean: Validate the user status
        - save: Validate the user status and save the user

    UserManager Methods:
        - create_user: Create a user with email and password
        - create_superuser: Create a superuser with email and password
      """
# Required input fields
    email = models.EmailField(max_length=254, unique=True)

# Optional input fields
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

# Calculated fields
    # main_account = models.OneToOneField("account.Individual", on_delete=models.PROTECT, null=True, blank=True, related_name='user')
    status = FlexUpEnumField(flexup_enum=Status, choices=StatusShortList, default=Status.PENDING)
    is_email_verified = models.BooleanField(default=False) # The user has clicked on the email validation link
    joined_datetime = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        # if self.main_account:
        #     return  f"{self.main_account.name.strip()} ({self.email}) 🧑‍💻{self.status.symbol}"   # Fab→JB: 2024-10-22 we need to recover the statuts symbol from the base Status Enum class
        return f"{self.email} 🧑‍💻{self.status.symbol}"

    @property
    def is_active(self):
        """ Return True if the user status is ACTIVE and email is verified. """
        if self.status == Status.ACTIVE and self.is_email_verified:
            return True

    @classmethod
    def login_with_user_data(cls, **user_data):
        """ Authenticate a user with email and password, and return the user object """
        user = authenticate(email=user_data['email'], password=user_data['password'])

        if user is None:
            raise ValueError("Invalid credentials")

        if not user.is_email_verified:
            raise ValueError("Email not verified")

        if user.status is Status.SUSPENDED:
            raise ValueError("User has been suspended")

        if user.status is Status.CLOSED:
            raise ValueError("User account has been closed")

        return user

    def verify_email(self):
        """  Mark the email as verified and set the user status to ACTIVE """
        self.is_email_verified = True
        self.save()

    def close(self):
        self.status = Status.CLOSED
        self.save()
        # if self.main_account:
        #     self.main_account.status = Status.CLOSED
        #     self.main_account.save()
        # if self.memberships.count() > 0:
        #     for member in self.memberships.all():
        #         member.status = Status.CLOSED
        #         member.save()

    def clean(self):
        # if self.status.value not in dict(StatusShortList):   # Old version
        if not Status.is_valid(self.status, StatusShortList):
            raise ValueError(f"Invalid user status: {self.status}")

        if self.is_email_verified and self.status == Status.PENDING:
            self.status = Status.ACTIVE

        if not self.is_email_verified and self.status == Status.ACTIVE:
            self.status = Status.PENDING

    def save(self, *args, **kwargs):
        self.clean_fields(exclude=['status'])
        self.clean()
        super(User, self).save(*args, **kwargs)

    # @property
    # def name(self):
    #     return self.main_account.name if self.main_account else self.email
    
    # @property
    # def first_name(self):
    #     return self.main_account.first_name if self.main_account else self.email
    
    # @property
    # def last_name(self):
    #     return self.main_account.last_name if self.main_account else self.email
