from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'food'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('registration', UserRegistrationFromView.as_view(), name='registration'),
    path('registr_done', UserRegistrationDoneView.as_view(), name='registration_done')
]