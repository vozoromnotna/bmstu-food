from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView, ListView, DeleteView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import LoginView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F, DecimalField

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
        password = form.cleaned_data["password"]
        user.set_password(password)
        user.save()
        return super().form_valid(form)
    
class UserLoginFormView(LoginView):
    authentication_form = CustomUserAuthenticationForm
    

class UserOrdersView(LoginRequiredMixin, ListView):
    template_name = "food/orders.html"
    model = Order
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('orderdetails_set').annotate(
            total_cost=Sum(F('orderdetails__count') * F('orderdetails__dish__price'), output_field=DecimalField())
        )
    
class UserFavoriteDishView(LoginRequiredMixin, ListView):
    template_name = "food/favorite_dish.html"
    model = FavoriteDish
    context_object_name = "favorite_dishes"

    def get_queryset(self):
        return FavoriteDish.objects.filter(user=self.request.user)
    
class UserFavoriteDishDeleteView(LoginRequiredMixin, DeleteView):
    model = FavoriteDish
    success_url = reverse_lazy("food:favorite_dish")
    def form_valid(self, form):
        user = self.object.user
        if user != self.request.user:
            raise PermissionDenied
        return super().form_valid(form)
    

class WorkerFoodservicesView(LoginRequiredMixin, ListView):
    model = Foodservice
    template_name = "food/worker_account.html"
    context_object_name = "foodservices"
    
    def get_queryset(self):
        user = self.request.user
        if not user.groups.filter(name="workers").exists():
            raise PermissionDenied
        return Foodservice.objects.filter(foodserviceworker__worker=user)
    
class FoodserviceWorkersView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = "workers"
    template_name = "food/foodservice_workers.html"
    
    def get_queryset(self):
        foodservice = Foodservice.objects.get(title=self.kwargs["title"])
        if self.request.user != foodservice.owner:
            raise PermissionDenied
        return User.objects.filter(foodserviceworker__foodservice=foodservice)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_2'] = self.kwargs['title'] #Иначе шаблон не видит title
        return context
    
    
class FoodserviceWorkerDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "food/foodservice_workers_delete.html"
    context_object_name = "foodservice_worker"
    model = FoodserviceWorker
    def form_valid(self, form):
        
        if self.request.user != self.object.foodservice.owner:
            raise PermissionDenied

        self.object.delete()
        
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def get_object(self):
        foodservice_title = self.kwargs["title"]
        user_id = self.kwargs["user_id"]
        return FoodserviceWorker.objects.get(foodservice__title=foodservice_title, worker__id=user_id)
    
    
    def get_success_url(self):
        return reverse_lazy("food:foodservice_workers", kwargs = {"title": self.kwargs["title"]})

    
