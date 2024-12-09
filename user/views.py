from django.shortcuts import render

from django.contrib.auth import authenticate, login


def _login(*, username, password, request=None):
    user = authenticate(request=request, username=username, password=password)

    if request and user:
        login(request, user=user)
    return user


# Create your views here.
