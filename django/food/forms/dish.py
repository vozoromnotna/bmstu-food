from django import forms
from ..models import Dish
from django.utils.translation import gettext_lazy as _

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