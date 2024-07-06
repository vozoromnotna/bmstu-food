from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from ..forms import *
from ..models import *


class DishListView(ListView, LoginRequiredMixin, UserPassesTestMixin):
    model = Dish
    context_object_name = "dish_list"
    template_name = "food/dish/dish_list.html"

    def test_func(self):
        dish = Dish.objects.get(name=self.kwargs["name"])
        res = FoodserviceWorker.objects.filter(worker=self.request.user, foodservice=foodservice).exists()
        return res


class DishCreateView(CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'food/dish/dish_form.html'
    success_url = reverse_lazy('food:dish')


class DishDetailView(DetailView):
    model = Dish
    pk_url_kwarg = 'dish_id'
    context_object_name = "dish"
    template_name = 'food/dish/dish_detail.html'





class DishDeleteView(DeleteView):
    model = Dish
    pk_url_kwarg = 'dish_id'
    context_object_name = "dish"
    success_url = reverse_lazy('food:dish')
    template_name = 'food/dish/dish_confirm_delete.html'


class DishUpdateView(UpdateView):
    model = Dish
    form_class = DishForm
    template_name = 'food/dish/dish_update.html'
    pk_url_kwarg = 'dish_id'

    def get_success_url(self):
        return reverse_lazy('food:dish_detail', kwargs={'dish_id': self.object.id})
