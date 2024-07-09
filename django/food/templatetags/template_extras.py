from django import template
from food.models import Foodservice, FoodserviceWorker

register = template.Library()

@register.inclusion_tag('base/stylized_form.html')
def stylize_form(form, button_label):
    return {'form': form, 'button_label': button_label }

@register.inclusion_tag('base/dish_card.html')
def dish_card(dish, is_description=False, is_calorie=False, is_deletable=False, is_editable=False,
              is_to_favorite=False, delete_url=None, edit_url=None, to_favorite_url=None,
              favorite_status=False, is_more=False, more_url=None):
    return locals()

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