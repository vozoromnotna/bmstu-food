from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView, ListView
from django.contrib.auth.views import LoginView
from .models import Order, OrderDetails
from django.contrib.auth.mixins import LoginRequiredMixin

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
    template_name = "food/orders_view.html"
    model = Order
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('orderdetails_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_details'] = OrderDetails.objects.filter(order__user=self.request.user).select_related('dish')
        context['']
#         Нужно добавить суммы
#         SELECT food_order.id, SUM(count * price)
#         FROM food_order
#         JOIN
#         food_orderdetails
#         ON food_order.id = food_orderdetails.order_id
#         JOIN
#         food_dish
#         ON food_orderdetails.dish_id = food_dish.id
#         GROUP BY food_order.id
        return context
    
