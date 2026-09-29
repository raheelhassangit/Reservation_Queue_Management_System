from django.urls import path
from . import views_web

urlpatterns = [
    path("login/", views_web.login_page, name="login-page"),
    path("register/", views_web.register_page, name="register-page"),
]