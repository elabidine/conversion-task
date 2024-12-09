from django.contrib.auth.backends import BaseBackend
from core.enums.status import Status
from user.models import User


class FlexUpAuthBackend(BaseBackend):
     def get_user(self, user_id):
         try:
             return User.objects.get(pk=user_id)
         except (User.DoesNotExist, User.MultipleObjectsReturned):
             return None

     def authenticate(self, request, email=None, password=None):
         if email and password:
             try:
                 user = User.objects.get(email=email)
                 if user.check_password(password):
                     return user
             except(User.DoesNotExist, User.MultipleObjectsReturned):
                 return None
         return None
