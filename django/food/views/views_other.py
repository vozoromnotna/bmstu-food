from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

import json

from ..models import *
from ..forms import *

class IndexView(TemplateView):
    template_name = "food/index.html"

class CreateOrderView(ListView, LoginRequiredMixin):
    model = Dish
    context_object_name = "dishes"
    template_name="food/order_create.html"
    def get_queryset(self):
        foodservice_title = self.kwargs["title"]
        return Dish.objects.filter(foodservice__title=foodservice_title)
    
    
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        order = body["order"]
        username = body["username"]
        user = User.objects.filter(username=username).first()
        if (not user):
            return HttpResponse(content="UserNotExist")
        
        orderObject = Order(user=user)
        orderObject.save()
        
        for position in order:
            dish = Dish.objects.filter(name=position["dish"]).first()
            if (not dish):
                return HttpResponse(content="DishNotFound") 
            OrderDetails(order=orderObject, dish=dish, count=position["count"]).save()
            
        
        return HttpResponseRedirect(reverse_lazy("food:order_create_success"))
    
class CreateOrderSuccessView(TemplateView):
    template_name = "food/order_create_success.html"
        
        
    

    


    
