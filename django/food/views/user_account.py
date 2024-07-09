from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import ListView, DeleteView, DetailView, CreateView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum, F, DecimalField
from ..models import Order, FavoriteDish, OrderDetails, Dish, Foodservice, FoodserviceWorker, FoodserviceRoles
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from itertools import groupby
from operator import attrgetter

class UserOrdersView(LoginRequiredMixin, ListView):
    template_name = "food/user_account/user_orders.html"
    model = Order
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('orderdetails_set').annotate(
            total_cost=Sum(F('orderdetails__count') * F('orderdetails__dish__price'), output_field=DecimalField())
        )


class UserOrderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = 'food/order/order_detail.html'   
    model = Order
    context_object_name = 'orders'

    def test_func(self):
        self.order: Order = self.get_object()
        self.order_details: QuerySet = OrderDetails.objects.filter(order=self.order)
        
        if self.request.user.is_staff:
            return True
        
        if self.order.user == self.request.user:
            return True
        
        if self.order_details.exists():
            foodservice = self.order_details.first().dish.foodservice
            if FoodserviceWorker.objects.filter(foodservice=foodservice, worker=self.request.user):
                return True
            
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        total_amount = sum(detail.dish.price * detail.count for detail in self.order_details)
        
        context['order'] = self.order
        context['order_details'] = self.order_details
        context['total_amount'] = total_amount

        return context
    

class UserOrdersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "food/user_account/user_orders_list.html"
    model = OrderDetails
    context_object_name = "orders"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.username == self.kwargs["username"]
    
    def get_queryset(self):
        ordering = '-order__date'
        username = self.kwargs['username']
        if self.request.user.is_staff:
            queryset = OrderDetails.objects.filter(order__user__username=username).select_related('order', 'dish').order_by(ordering)
        else:
            queryset = OrderDetails.objects.filter(order__user=self.request.user).select_related('order', 'dish').order_by(ordering)

        grouped_orders = []
        queryset = sorted(queryset, key=lambda x: (x.order.id, x.order.date), reverse=True)
        for key, group in groupby(queryset, key=attrgetter('order.id')):
            grouped_orders.append(list(group))

        return grouped_orders  
    

class UserFavoriteDishView(LoginRequiredMixin, ListView):
    template_name = "food/user_account/favorite_dish.html"
    model = FavoriteDish
    context_object_name = "favorite_dishes"

    def get_queryset(self):
        return FavoriteDish.objects.filter(user=self.request.user)
    
class UserFavoriteDishDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FavoriteDish
    def test_func(self):
        if self.request.user.id != self.kwargs["user_id"]:
            return False
        return True
    
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        object = get_object_or_404(FavoriteDish, user=self.kwargs["user_id"], dish=self.kwargs["dish_id"])
        object.delete()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self) -> str:
        prev_url = self.request.POST.get('next', '/')
        return prev_url
    
class UserFavoriteDishCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = FavoriteDish

    def test_func(self):
        if self.request.user.id != self.kwargs["user_id"]:
            return False
        return True
    
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user = get_object_or_404(User, id=self.kwargs["user_id"])
        dish = get_object_or_404(Dish, id=self.kwargs["dish_id"])
        object = FavoriteDish(user=user, dish=dish)
        try:
            object.save()
            return HttpResponseRedirect(self.get_success_url())
        except:
            return Http404()
        
    def get_success_url(self) -> str:
        prev_url = self.request.POST.get('next', '/')
        return prev_url