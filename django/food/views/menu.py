from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..forms import *
from ..models import *

import logging


class MenuListView(ListView):
    model = MenuDetails
    context_object_name = "menu_list"
    template_name = "food/menu/menu_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.kwargs["title"]
        return context


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
            form.add_error("dish", forms.ValidationError(f"{dish} уже есть в меню на {menu}"))
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.kwargs["title"]
        return context

class MenuDeleteView(DeleteView):
    model = MenuDetails
    pk_url_kwarg = 'menu_id'
    context_object_name = "menu_list"
    success_url = reverse_lazy('food:menu')
    template_name = 'food/menu/menu_confirm_delete.html'



# class MenuDetailView(DetailView):
#     model = MenuDetails
#     pk_url_kwarg = 'menu_id'
#     context_object_name = "menu"
#     template_name = 'food/menu_detail.html'
