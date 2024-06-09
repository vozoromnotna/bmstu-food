from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, DetailView, UpdateView

from ..forms import *
from ..models import *


class MenuListView(ListView):
    model = MenuDetails
    context_object_name = "menu_list"
    template_name = "food/menu_list.html"


class MenuCreateView(CreateView):
    model = MenuDetails
    form_class = MenuForm
    template_name = 'food/menu_form.html'
    success_url = reverse_lazy('food:menu')


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
