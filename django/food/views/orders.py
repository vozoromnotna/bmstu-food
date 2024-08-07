from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

import json
from datetime import date

from ..models import *
from ..forms import *


class CreateOrderView(ListView, LoginRequiredMixin):
    model = Dish
    context_object_name = "dishes"
    template_name="food/order/order_create.html"
    def get_queryset(self):
        foodservice_title = self.kwargs["title"]
        return Dish.objects.filter(foodservice__title=foodservice_title, menudetails__menu__date=date.today()).prefetch_related("menudetails_set")
    
    
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        order = body["order"]
        username = body["username"]
        user = User.objects.filter(username=username).first()
        if (not user):
            return HttpResponse(content="UserNotExist")
        
        orderObject = Order(user=user)
        
        orderDetails = []
        
        for position in order:
            dish = Dish.objects.filter(name=position["dish"]).first()
            
            if (not dish):
                return HttpResponse(content="DishNotFound") 
            if int(position["count"]) < 1:
                return HttpResponse(content="DishCountError")
            
            orderDetails.append(OrderDetails(order=orderObject, dish=dish, count=position["count"]))
        
        
        orderObject.save()
        for od in orderDetails: od.save()
        
        return HttpResponseRedirect(reverse_lazy("food:order_create_success"))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.kwargs["title"]
        return context
    
class CreateOrderSuccessView(TemplateView):
    template_name = "food/order/order_create_success.html"