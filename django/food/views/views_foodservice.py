
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from ..models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from ..forms import forms, FoodserviceWorkerForm


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

        worker = self.object.worker
        
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

class FoodserviceWorkerAddView(LoginRequiredMixin, CreateView):
    model = FoodserviceWorker
    form_class = FoodserviceWorkerForm
    template_name = "food/foodservice_worker_add.html" 

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
        context['title_2'] = self.kwargs['title'] #Иначе шаблон не видит title
        return context