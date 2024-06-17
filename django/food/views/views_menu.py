from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, DetailView, UpdateView

from ..forms import *
from ..models import *

import logging


class MenuListView(ListView):
    model = MenuDetails
    context_object_name = "menu_list"
    template_name = "food/menu_list.html"


# logger = logging.getLogger('__name__')

class MenuCreateView(CreateView):
    model = MenuDetails
    form_class = MenuForm
    template_name = 'food/menu_form.html'
    success_url = reverse_lazy('food:menu')

    def form_valid(self, form):
         # logger.critical('ааааааааа')
        dish = Dish.objects.get(name=self.kwargs['dish'])
        # logger.critical(dish)
    #     menu = Menu.objects.get(date=self.kwargs['menu'])
    #     logger.critical(menu)
    #     dish = Dish(id=7)
    #
        # if MenuDetails.objects.filter(dish=dish).exists():
        #     form.add_error("dish", forms.ValidationError(f'Блюдо уже есть в меню на'))
        #     return super().form_invalid(form)
        # return super().form_valid(form)
        # dish = Dish.objects.get(name=self.kwargs['dish'])
        # form.instance.dish = dish
        # print('ааааа')
        # dish_name = form.data["dish"]
        if MenuDetails.objects.filter(dish=dish).exists():
            form.add_error("dish", forms.ValidationError("абоба"))
            return super().form_invalid(form)
        return super().form_valid(form)


class MenuDeleteView(DeleteView):
    model = MenuDetails
    pk_url_kwarg = 'menu_id'
    context_object_name = "menu_list"
    success_url = reverse_lazy('food:menu')
    template_name = 'food/menu_confirm_delete.html'



# class MenuDetailView(DetailView):
#     model = MenuDetails
#     pk_url_kwarg = 'menu_id'
#     context_object_name = "menu"
#     template_name = 'food/menu_detail.html'
