from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import *

app_name = 'food'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('registration', UserRegistrationFromView.as_view(), name='registration'),
    path('login', UserLoginFormView.as_view(), name='login'),
    path('registr_done', UserRegistrationDoneView.as_view(), name='registration_done'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('orders', UserOrdersView.as_view(), name='orders'),
    path('favorite_dish', UserFavoriteDishView.as_view(), name='favorite_dish'),
    path('favorite_dish/delete/<int:pk>/', UserFavoriteDishDeleteView.as_view(), name='favorite_dish_delete'),
    path('worker_account', WorkerFoodservicesView.as_view(), name='worker_account'),
    path('foodsevice/<str:title>/workers/', FoodserviceWorkersView.as_view(), name='foodservice_workers'),
    path('foodsevice/<str:title>/workers/delete/<int:user_id>/', FoodserviceWorkerDeleteView.as_view(), name='foodservice_worker_delete'),
    path('foodservice/<str:title>/workers/add/', FoodserviceWorkerAddView.as_view(), name='foodservice_worker_add'),

    path('dish/', DishListView.as_view(), name='dish'),
    path('dish/create/', DishCreateView.as_view(), name='dish_form'),
    path('foodservice/create/', FoodserviceCreateView.as_view(), name='foodservice_form'),
    path('dish/<int:dish_id>/', DishDetailView.as_view(), name='dish_detail'),
    path('dish/<int:dish_id>/delete/', DishDeleteView.as_view(), name='delete_dish'),
    path('dish/<int:dish_id>/update/', DishUpdateView.as_view(), name='update_dish'),

    path('menu/', MenuListView.as_view(), name='menu'),
    path('menu/create/', MenuCreateView.as_view(), name='menu_form'),
    path('menu/<int:menu_id>/delete/', MenuDeleteView.as_view(), name='delete_menu'),
]
