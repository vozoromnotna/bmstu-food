from django import template
from food.models import Foodservice, FoodserviceWorker

register = template.Library()

@register.inclusion_tag('base/stylized_form.html')
def stylize_form(form, button_label):
    return {'form': form, 'button_label': button_label }

@register.inclusion_tag('base/dish_card.html')
def dish_card(dish, is_short, is_editable=False, edit_url=None):
    return {'dish': dish, 'is_short': is_short, 'is_editable': is_editable, 'edit_url': edit_url }

@register.simple_tag
def multiply(a, b):
    return a * b

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 

@register.filter(name='is_owner') 
def is_owner(user, foodservice):
    if (not user.is_authenticated):
        return False
    if type(foodservice) == str:
        foodservice = Foodservice.objects.get(title=foodservice)
    return foodservice.owner == user

@register.filter(name='is_worker') 
def is_worker(user, foodservice):
    if (not user.is_authenticated):
        return False
    if type(foodservice) == str:
        foodservice = Foodservice.objects.get(title=foodservice)
    return FoodserviceWorker.objects.filter(worker=user, foodservice=foodservice).exists()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)