from django.urls import path, include
from .routers import router
from .views import login, register

urlpatterns = [
    path("login/", login),
    path("register/", register),
    path("", include(router.urls)),
]