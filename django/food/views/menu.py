import datetime
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, DetailView, UpdateView

from ..forms import *
from ..models import *

import logging


class MenuListView(ListView):
    model = MenuDetails
    context_object_name = "menu_list"
    template_name = "food/menu/menu_list.html"

    def get_queryset(self):
        menus = Menu.objects.only('id').filter(date = datetime.date.today())
        return MenuDetails.objects.filter(menu__in=menus)


# logger = logging.getLogger('__name__')

class MenuCreateView(CreateView):
    model = MenuDetails
    form_class = MenuForm
    template_name = 'food/menu/menu_form.html'
    success_url = reverse_lazy('food:menu')

    def form_invalid(self, form):
        dish = form.cleaned_data['dish']
        menu = form.cleaned_data['menu']
        if MenuDetails.objects.filter(dish=dish).exists():
            if MenuDetails.objects.filter(menu=menu).exists():
                form.add_error("dish", forms.ValidationError(f"{dish} уже есть в меню на {menu}"))
                return super().form_invalid(form)


class MenuDeleteView(DeleteView):
    model = MenuDetails
    pk_url_kwarg = 'menu_id'
    context_object_name = "menu_list"
    success_url = reverse_lazy('food:menu')
    template_name = 'food/menu/menu_confirm_delete.html'
