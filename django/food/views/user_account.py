from django.db.models.query import QuerySet
from django.views.generic import ListView, DeleteView, DetailView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum, F, DecimalField
from ..models import Order, FavoriteDish, OrderDetails, Dish, Foodservice
from django.urls import reverse_lazy
from django.contrib.auth.models import User

class UserOrdersView(LoginRequiredMixin, ListView):
    template_name = "food/user_account/user_orders.html"
    model = Order
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('orderdetails_set').annotate(
            total_cost=Sum(F('orderdetails__count') * F('orderdetails__dish__price'), output_field=DecimalField())
        )


    
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