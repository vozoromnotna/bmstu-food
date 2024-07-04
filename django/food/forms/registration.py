from django import forms
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.forms import AuthenticationForm, UsernameField 

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
    
    error_messages = {
        "invalid_login": _(
            "Логин и пароль не совпадают"
        ),
        "inactive": _("Пользователь не подтвердил email"),
    }

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
        labels = {
            'username':_('Логин'),
            'first_name':_('Имя'),
            'last_name':_('Фамилия'),
        }
        

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password']