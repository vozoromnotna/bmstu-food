
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, DetailView, UpdateView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from ..models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..forms import forms, FoodserviceWorkerForm, FoodserviceForm
from itertools import groupby
from operator import attrgetter
from django.shortcuts import get_object_or_404
from itertools import groupby
from operator import attrgetter


class FoodserviceCreateView(UserPassesTestMixin, CreateView):
    model = Foodservice
    form_class = FoodserviceForm
    template_name = 'food/foodservice/foodservice_form.html'
    
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        
        return False
    
    def get_success_url(self) -> str:
        return reverse_lazy('food:foodservice_detail', kwargs={"title": self.object.title})
    

class WorkerFoodservicesView(LoginRequiredMixin, ListView):
    model = Foodservice
    template_name = "food/foodservice/worker_account.html"
    context_object_name = "foodservices"
    
    def get_queryset(self):
        user = self.request.user
        if not user.groups.filter(name="workers").exists():
            raise PermissionDenied
        return Foodservice.objects.filter(foodserviceworker__worker=user)
    
class FoodserviceWorkersView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = "workers"
    template_name = "food/foodservice/foodservice_workers.html"
    
    def get_queryset(self):
        foodservice = Foodservice.objects.get(title=self.kwargs["title"])
        if self.request.user != foodservice.owner:
            raise PermissionDenied
        return User.objects.filter(foodserviceworker__foodservice=foodservice)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['title']
        return context
    
    
class FoodserviceWorkerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "food/foodservice/foodservice_workers_delete.html"
    context_object_name = "foodservice_worker"
    model = FoodserviceWorker
    def test_func(self):
        return self.request.user == self.get_object().foodservice.owner
    
    def form_valid(self, form):
        worker = self.object.worker
        
        if worker == self.object.foodservice.owner:
            form.add_error(None, forms.ValidationError("Невозможно удалить владельца"))
            return super().form_invalid(form)
        
        self.object.delete()
        
        if (len(Foodservice.objects.filter(foodserviceworker__worker=worker)) == 0):
            group = Group.objects.get(name="workers")
            worker.groups.remove(group)
            
        
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def get_object(self):
        foodservice_title = self.kwargs["title"]
        user_id = self.kwargs["user_id"]
        return FoodserviceWorker.objects.get(foodservice__title=foodservice_title, worker__id=user_id)
    
    
    def get_success_url(self):
        return reverse_lazy("food:foodservice_workers", kwargs = {"title": self.kwargs["title"]})

class FoodserviceWorkerAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = FoodserviceWorker
    form_class = FoodserviceWorkerForm
    template_name = "food/foodservice/foodservice_worker_add.html" 

    def test_func(self):
        foodservice = Foodservice.objects.get(title=self.kwargs['title'])
        return foodservice.owner == self.request.user 
    
    def form_valid(self, form):
        foodservice = Foodservice.objects.get(title=self.kwargs['title'])
        form.instance.foodservice = foodservice
        
        worker_username=form.data["username"]
        if FoodserviceWorker.objects.filter(worker__username=worker_username, foodservice=foodservice).exists():
            form.add_error("username", forms.ValidationError("Работник уже в штате"))
            return super().form_invalid(form)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("food:foodservice_workers", kwargs = {"title": self.kwargs["title"]})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.kwargs["title"]
        return context
    
class FoodserviceOrdersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "food/foodservice/foodservice_orders.html"
    model = OrderDetails
    context_object_name = "orders"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.kwargs["title"]
        return context
    
    def test_func(self):
        foodservice = Foodservice.objects.get(title=self.kwargs["title"])
        res = FoodserviceWorker.objects.filter(worker=self.request.user, foodservice=foodservice).exists()
        return res
    
    def get_queryset(self):
        foodservice = Foodservice.objects.get(title=self.kwargs["title"])
        ordering = '-order__date'
        queryset = OrderDetails.objects.filter(dish__foodservice=foodservice).select_related('order', 'dish').order_by(ordering)
        
        # Группировка заказов по номеру и сортировка по дате
        grouped_orders = []
        queryset = sorted(queryset, key=lambda x: (x.order.id, x.order.date), reverse=True)
        for key, group in groupby(queryset, key=attrgetter('order.id')):
            grouped_orders.append(list(group))
            
        return grouped_orders

class FoodserviceDetailView(DetailView):
    template_name = "food/foodservice/foodservice_detail.html"
    model = Foodservice
    context_object_name = "foodservice"
    def get_object(self):
        return get_object_or_404(Foodservice, title=self.kwargs["title"])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        foodsevice = context["object"]
        context["fields"] = {
            'Название': foodsevice.title,
            'Тип': foodsevice.get_type_display(),
            'Владелец': foodsevice.owner,
        }
        context["title"] = self.kwargs["title"]
        return context

class FoodserviceUpdateView(UserPassesTestMixin, UpdateView):
    template_name = "food/foodservice/foodservice_update.html"
    model = Foodservice
    form_class = FoodserviceForm
    def test_func(self):
        foodservice = Foodservice.objects.get(title=self.kwargs['title'])
        return foodservice.owner == self.request.user 
    
    def get_object(self):
        return get_object_or_404(Foodservice, title=self.kwargs["title"])
    
    def get_success_url(self):
        url = reverse_lazy("food:foodservice_detail", kwargs={"title": self.object.title})
        return url