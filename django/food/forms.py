from django import forms
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.forms import AuthenticationForm, UsernameField 

from .models import FoodserviceWorker

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