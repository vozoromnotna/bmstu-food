from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import *

app_name = 'food'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('registration', UserRegistrationFromView.as_view(), name='registration'),
    path('login', UserLoginFormView.as_view(), name='login'),
    path('registr_done', UserRegistrationDoneView.as_view(), name='registration_done'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('orders', UserOrdersView.as_view(), name="orders"),
    path('favorite_dish', UserFavoriteDishView.as_view(), name="favorite_dish"),
]