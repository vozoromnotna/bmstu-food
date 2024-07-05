from django import forms
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import (
    validate_password,
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator
)
from django.core.exceptions import ValidationError

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
        password = cd.get('password')
        password2 = cd.get('password2')
        
        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords don\'t match.')
        
        user = User(username=cd.get('username'), 
        first_name=cd.get('first_name'), 
        last_name=cd.get('last_name'), 
        email=cd.get('email'))
        
        validators = [
            UserAttributeSimilarityValidator(user_attributes=['username', 'first_name', 'last_name', 'email']),
            MinimumLengthValidator(min_length=8),
            CommonPasswordValidator(),
            NumericPasswordValidator(),
        ]
        
        errors = []
        for validator in validators:
            try:
                validator.validate(password, user)
            except ValidationError as error:
                if isinstance(validator, UserAttributeSimilarityValidator):
                    errors.append('Пароль слишком похож на ваше имя, фамилию или email. ')
                elif isinstance(validator, MinimumLengthValidator):
                    errors.append('Пароль слишком короткий. Он должен содержать как минимум 8 символов. ')
                elif isinstance(validator, CommonPasswordValidator):
                    errors.append('Пароль слишком распространён. ')
                elif isinstance(validator, NumericPasswordValidator):
                    errors.append('Пароль не может состоять только из цифр. ')
        
        if errors:
            raise ValidationError(errors)
        
        return password2