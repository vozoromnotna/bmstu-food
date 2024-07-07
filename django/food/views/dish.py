from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404

from ..forms import *
from ..models import *


class DishListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Dish
    context_object_name = "dish_list"
    template_name = "food/dish/dish_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.kwargs["title"]
        return context
    
    def get_queryset(self):
        return Dish.objects.filter(foodservice__title = self.kwargs["title"])
    
    def test_func(self):
        return FoodserviceWorker.objects.filter(worker=self.request.user, foodservice__title=self.kwargs["title"]).exists()


class DishCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'food/dish/dish_form.html'
    success_url = reverse_lazy('food:dish')
    
    def form_valid(self, form):
        dish = form.save(commit=False)
        dish.foodservice = Foodservice.objects.get(title=self.kwargs["title"])
        dish.save()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)
    
    def test_func(self):
        return FoodserviceWorker.objects.filter(worker=self.request.user, foodservice__title=self.kwargs["title"]).exists()
    
    def get_success_url(self) -> str:
        return reverse_lazy('food:dish', kwargs={'title':self.kwargs["title"]})


class DishDetailView(DetailView):
    model = Dish
    pk_url_kwarg = 'dish_id'
    context_object_name = "dish"
    template_name = 'food/dish/dish_detail.html'
    

class DishDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Dish
    pk_url_kwarg = 'dish_id'
    context_object_name = "dish"
    success_url = reverse_lazy('food:dish')
    template_name = 'food/dish/dish_confirm_delete.html'
    
    def test_func(self):
        dish = self.get_object()
        self.foodservice_title = dish.foodservice.title
        return FoodserviceWorker.objects.filter(worker=self.request.user, foodservice__title=dish.foodservice).exists()
    
    def get_success_url(self) -> str:
        return reverse_lazy('food:dish', kwargs={'title':self.foodservice_title})


class DishUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Dish
    form_class = DishForm
    template_name = 'food/dish/dish_update.html'
    pk_url_kwarg = 'dish_id'

    def get_success_url(self):
        return reverse_lazy('food:dish_detail', kwargs={'dish_id': self.object.id})
    
    def test_func(self):
        dish = self.get_object()
        return FoodserviceWorker.objects.filter(worker=self.request.user, foodservice__title=dish.foodservice).exists()
    
    def form_valid(self, form):
        dish = form.save(commit=False)
        success_url = self.get_success_url()
        dish.save()
        return HttpResponseRedirect(success_url)
