from django.urls import path
from . import views


urlpatterns = [
    path('account/register', views.UserCreate.as_view())
]
