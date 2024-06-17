from django import forms
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.forms import AuthenticationForm, UsernameField 

from .models import *

from django.forms import ModelForm

class CustomUserAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label=_("Логин"),
        widget=forms.TextInput(attrs={"autofocus": True})
        )
    password = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'username':_('Логин'),
            'first_name':_('Имя'),
            'last_name':_('Фамилия'),
            'email':_('Email')
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password']

class FoodserviceWorkerForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Логин пользователя")

    class Meta:
        model = FoodserviceWorker
        fields = ['username']

    def save(self, commit=True):
        worker = User.objects.get(username=self.cleaned_data['username'])
        foodservice_worker = super().save(commit=False)
        foodservice_worker.worker = worker
        foodservice_worker.role = "worker"
        
        if commit:
            foodservice_worker.save()
            workers_group = Group.objects.get(name="workers")
            workers_group.user_set.add(worker)
    
        return foodservice_worker
    
    def clean_username(self):
        cd = self.cleaned_data
        user = User.objects.filter(username=cd["username"])
        if not user.exists():
            raise forms.ValidationError("Такого пользователя не существует")
        
        
        return cd["username"]


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'image', 'foodservice', 'price', 'energy', 'carbohydrates', 'fat', 'proteins']
        labels = {
            'name': _('Наименование'),
            'description': _('Описание'),
            'image': _('Фотография'),
            'foodservice': _('Заведение'),
            'price': _('Цена, руб.'),
            'energy': _('Энергетическая ценность, ккал.'),
            'carbohydrates': _('Углеводы, г.'),
            'fat': _('Жиры, г.'),
            'proteins': _('Белки, г.')
        }

class FoodserviceForm(forms.ModelForm):
    class Meta:
        model = Foodservice
        fields = ['title', 'type', 'owner']
        labels = {
            'title': _('Название'),
            'type': _('Тип заведения'),
            'owner': _('Владелец')
        }


class MenuForm(forms.ModelForm):
    # dish = forms.CharField(max_length=150, label="Блюдо")
    # menu = forms.CharField(max_length=150, label="Меню")


    class Meta:
        model = MenuDetails
        fields = ['dish', 'menu']
        labels = {
            'dish': _('Блюдо'),
            'menu': _('Меню')
        }

