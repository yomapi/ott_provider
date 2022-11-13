from django.urls import path
from user.views import login, signup

urlpatterns = [
    path("login/", login),
    path("signup/", signup),
]
