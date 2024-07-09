from django import forms
from ..models import FavoriteDish
from django.utils.translation import gettext_lazy as _

class FavoriteForm(forms.ModelForm):
    class Meta:
        model = FavoriteDish
        fields = ['user', 'dish']
        labels = {
            'dish': _('Блюдо'),
        }