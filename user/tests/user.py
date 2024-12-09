from django.db import Error
from core.enums.status import Status
from datetime import date
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from user.models import User
# from utils.tests.print_var import print_var

class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls): # data shared between all tests, should not be modified by any test
        cls.user_data = {
            'email': 'user1@example.com',
            'password': 'securepassword123'
        }

# Signup tests

    def test_01_signup_user_without_email_validation(self):
        # Given a user who has filled in the signup form

        # When the system creates the user
        user = User.objects.create_user(**self.user_data)
        # print_var(user)

        # Then the user status is pending, is_email_verified is False
        self.assertEqual(user.status, Status.PENDING)
        self.assertFalse(user.is_email_verified)

        # And date joined is today, is_staff and is_superuser are False, main_account is None
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.main_account, None)
        self.assertEqual(user.joined_datetime.date(), date.today())

        # And password is hashed in the database
        self.assertNotEqual(user.password, self.user_data['password'])

        # And user label is the email and the status symbol
        self.assertEqual(str(user), "user1@example.com 🧑‍💻🕒")
        self.assertEqual(user.__str__(), "user1@example.com 🧑‍💻🕒")


    def test_02_signup_user_fails_if_email_exists(self):
        # Given a user who has already signed up
        User.objects.create_user(**self.user_data)

        # When the a user tries to sign up again with the same email
        # Then an error is raised
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**self.user_data)


    def test_03_signup_user_fails_if_email_not_valid(self):
        # Given a user who has filled in the signu up form with an invalid email

        user2_data = {
            'email': 'invalidemail',
            'password': 'securepassword123'
        }

        # When the system tries to create the user
        # Then an error is raised
        with self.assertRaisesRegex(ValidationError, "Enter a valid email address"):
            User.objects.create_user(**user2_data)

        # Signup fails without email
        with self.assertRaises(TypeError):
            User.objects.create_user(password='securepassword123')

# Email validation & status change tests

    def test_04_verifies_email_succeeds(self):
        # print_var()
        # Given a user who has signed up
        user = User.objects.create_user(**self.user_data)

        # When the user verifies their email
        user.verify_email()

        # Then the email is verified the status is set to active and label is updated
        self.assertEqual(user.is_email_verified, True)
        self.assertEqual(user.status, Status.ACTIVE)
        self.assertEqual(user.is_active, True)
        self.assertEqual(str(user), "user1@example.com 🧑‍💻🟢")
        # print_var("user.status.symbol active", user.status.symbol)

        # When the email validation is set to false (for example if the user changes their email)
        user.is_email_verified = False
        user.save()

        # Then the status is set to pending
        self.assertEqual(user.status, Status.PENDING)
        self.assertEqual(user.is_active, False)

        # When the user is retrieved from the database
        user2 = User.objects.get(email=self.user_data['email'])

        # Then string representation is the same as before
        self.assertEqual(str(user2), "user1@example.com 🧑‍💻🕒")
        # print_var("user.status.symbol pending", user.status.symbol)


# Login tests

    def test_05_login_suceeds(self):
        # Given an active user with a verified email
        user = User.objects.create_user(**self.user_data, status=Status.ACTIVE, is_email_verified=True)

        # When the user tries to login
        logged_user = User.login_with_user_data(**self.user_data)

        # Then the logged user is the same as the user
        self.assertEqual(logged_user, user)


    def test_06_login_fail_if_email_not_verified(self):
        # Given a user who has signed up, but not yet verified his email
        user = User.objects.create_user(**self.user_data)

        # When the user tries to login, an error is raised and the message is "Email not verified"
        with self.assertRaisesRegex(ValueError, 'Email not verified'):
            User.login_with_user_data(**self.user_data)


    def test_07_login_fails_with_invalid_credentials(self):
        # Given a user who has not signed up
        user = User.objects.create_user(**self.user_data)

        # When the user tries to login, an error is raised
        with self.assertRaisesRegex(ValueError, "Invalid credentials"):
            User.login_with_user_data(email='wrong@example.com', password=self.user_data['password'])

        # When the user tries to login with the wrong password, an error is raised
        with self.assertRaisesRegex(ValueError, "Invalid credentials"):
            User.login_with_user_data(email=self.user_data['email'], password='wrongpassword')


    def test_08_login_fails_with_inactive_user(self):
        # Given a user whose status is suspended
        user = User.objects.create_user(**self.user_data, is_email_verified=True, status=Status.SUSPENDED)

        # When the user tries to login, an error is raised and the message is "User account has been suspended"
        with self.assertRaisesRegex(ValueError, "User has been suspended"):
            User.login_with_user_data(**self.user_data)

    def test_09_login_fails_with_closed_user(self):
        # Given a user whose status is closed
        user = User.objects.create_user(**self.user_data, is_email_verified=True, status=Status.CLOSED)

        # When the user tries to login, an error is raised and the message is "User account has been closed"
        with self.assertRaisesRegex(ValueError, "User account has been closed"):
            User.login_with_user_data(**self.user_data)


# User status change tests

    def test_10_assign_invalid_status_fails(self):
        # Given a user who has signed up
        user = User.objects.create_user(**self.user_data)

        # When the system tries to assign an invalid status
        user.status = Status.TERMINATED

        # Then an error is raised and the message starts with "Invalid user status"
        with self.assertRaisesRegex(ValueError, 'Invalid user status'):
            user.save()
