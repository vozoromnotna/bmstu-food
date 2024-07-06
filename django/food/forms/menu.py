from django import forms
from ..models import MenuDetails, OrderDetails
from django.utils.translation import gettext_lazy as _

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

class CreateOrderForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Логин пользователя")
    
    class Meta:
        model = OrderDetails
        fields = ['dish', 'count']