from django.contrib import admin
from .models import *

@admin.register(Foodservice)
class FoodserviceAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'owner')
    search_fields = ('title', 'type', 'owner__username')
    list_filter = ('type',)

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'foodservice', 'price')
    search_fields = ('foodservice__title',)
    list_filter = ('foodservice', )

@admin.register(FoodserviceWorker)
class FoodserviceWorkerAdmin(admin.ModelAdmin):
    list_display = ('foodservice', 'worker', 'role')
    search_fields = ('foodservice__title', 'worker__username')
    list_filter = ('role',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date')
    search_fields = ('user__username',)
    list_filter = ('date',)
    
@admin.register(OrderDetails)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order', 'dish', 'count')
    search_fields = ('order__user__username', 'dish__foodservice__title')

@admin.register(FavoriteDish)
class FavoriteDishAdmin(admin.ModelAdmin):
    list_display = ('user', 'dish')
    search_fields = ('user__username', 'dish__foodservice__title')

@admin.register(FavoriteFoodservice)
class FavoriteFoodserviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'foodservice')
    search_fields = ('user__username', 'foodservice__title')

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'date')
    list_filter = ('date',)
    
@admin.register(MenuDetails)
class MenuDetailAdmin(admin.ModelAdmin):
    list_display = ('menu', 'dish')
    search_fields = ('dish__foodservice__title', 'menu__id')
    list_filter = ('menu__date',)