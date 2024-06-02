from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView
from .forms import *
class IndexView(TemplateView):
    template_name = "food/index.html"

class UserRegistrationDoneView(TemplateView):
    template_name = "registration/registration_done.html"

class UserRegistrationFromView(FormView):
    template_name = "registration/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy('food:registration_done')
    
    def form_valid(self, form:UserRegistrationForm):
        user:User = form.instance
        password = form.clean_password()
        user.set_password(password)
        user.save()
        return super().form_valid(form)
