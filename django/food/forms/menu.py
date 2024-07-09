from django import forms
from ..models import MenuDetails, OrderDetails, Dish
from django.utils.translation import gettext_lazy as _

class MenuForm(forms.ModelForm):
    class Meta:
        model = MenuDetails
        fields = ['dish']
        labels = {
            'dish': _('Блюдо'),
        }
    def __init__(self, *args, **kwargs):
        foodservice = kwargs.pop('foodservice', None)
        super(MenuForm, self).__init__(*args, **kwargs)
        if foodservice:
            self.fields['dish'].queryset = Dish.objects.filter(foodservice=foodservice)
            
class CreateOrderForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Логин пользователя")
    
    class Meta:
        model = OrderDetails
        fields = ['dish', 'count']