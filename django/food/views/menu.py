import datetime
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, DetailView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..forms import *
from ..models import *

import logging
from datetime import date

class MenuListView(ListView):
    model = MenuDetails
    context_object_name = "menu_list"
    template_name = "food/menu/menu_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.kwargs["title"]
        return context

    def get_queryset(self):
        today = date.today()
        menus = Menu.objects.only('id').filter(date=today, foodservice__title = self.kwargs["title"])
        return MenuDetails.objects.filter(menu__in=menus)

class MenuCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MenuDetails
    form_class = MenuForm
    template_name = 'food/menu/menu_form.html'
    
    def get_form_kwargs(self):
        kwargs = super(MenuCreateView, self).get_form_kwargs()
        kwargs['foodservice'] = Foodservice.objects.get(title=self.kwargs["title"])
        return kwargs
    
    def form_valid(self, form): 
        today = date.today()
        menu_details:MenuDetails = form.save(False)
        menu_query = Menu.objects.filter(foodservice__title=self.kwargs["title"], date=today)
        if not menu_query.exists():
            menu = Menu()
            menu.foodservice = Foodservice.objects.get(title=self.kwargs["title"])
            menu.save()
            
        menu_details.menu = menu_query.first()
        try:
            menu_details.save()
        except:
            form.add_error("dish", forms.ValidationError(f"{menu_details.dish} уже есть в меню на {menu_details.menu}"))
            return super().form_invalid(form)
        
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.kwargs["title"]
        return context
    
    def test_func(self):
        return FoodserviceWorker.objects.filter(worker=self.request.user, foodservice__title=self.kwargs["title"]).exists()
    
    def get_success_url(self):
        return reverse_lazy("food:menu", kwargs={"title":self.kwargs["title"]})

class MenuDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MenuDetails
    context_object_name = "menu_list"
    template_name = 'food/menu/menu_confirm_delete.html'
    def test_func(self):
        self.menu_details:MenuDetails = self.get_object() 
        return FoodserviceWorker.objects.filter(worker=self.request.user, foodservice=self.menu_details.menu.foodservice).exists()
    
    def get_success_url(self) -> str:
        return reverse_lazy("food:menu", kwargs={"title": self.menu_details.menu.foodservice.title})
      

class FavoriteCreateView(CreateView):
    model = FavoriteDish
    form_class = FavoriteForm
    template_name = 'food/menu/favorite_form.html'
    success_url = reverse_lazy('food:menu')

    def form_invalid(self, form):
        dish = form.cleaned_data['dish']
        if FavoriteDish.objects.filter(dish=dish).exists():
            form.add_error("dish", forms.ValidationError(f"{dish} уже есть в избранном"))
            return super().form_invalid(form)
