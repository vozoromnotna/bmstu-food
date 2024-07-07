from django.db.models.query import QuerySet
from django.views.generic import ListView, DeleteView, DetailView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum, F, DecimalField
from ..models import Order, FavoriteDish, OrderDetails, Dish, Foodservice, FoodserviceWorker, FoodserviceRoles
from django.urls import reverse_lazy
from django.contrib.auth.models import User
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
        return self.request.user.is_authenticated
    


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        order_details = OrderDetails.objects.filter(order=order)
        
        total_amount = sum(detail.dish.price * detail.count for detail in order_details)
        
        context['order'] = order
        context['order_details'] = order_details
        context['total_amount'] = total_amount

        return context
    

class CommonUserOrdersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "food/user_account/user_orders_list.html"
    model = OrderDetails
    context_object_name = "orders"
   

    def test_func(self):
        return self.request.user.is_authenticated
    
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['foodservice_title'] = self.get_queryset()[0][0].dish.foodservice.title        
        return context   

class UserFavoriteDishView(LoginRequiredMixin, ListView):
    template_name = "food/user_account/favorite_dish.html"
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