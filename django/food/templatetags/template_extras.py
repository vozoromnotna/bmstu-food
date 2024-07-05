from django import template
from food.models import Foodservice

register = template.Library()

@register.inclusion_tag('base/stylized_form.html')
def stylize_form(form, button_label):
    return {'form': form, 'button_label': button_label }

@register.simple_tag
def multiply(a, b):
    return a * b

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 

@register.filter(name='is_owner') 
def is_owner(user, foodservice):
    if type(foodservice) == str:
        foodservice = Foodservice.objects.get(title=foodservice)
    return foodservice.owner == user

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)