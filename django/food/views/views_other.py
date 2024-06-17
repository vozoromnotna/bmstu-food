from django.views.generic import TemplateView, ListView

from ..models import *
from ..forms import *

class IndexView(TemplateView):
    template_name = "food/index.html"

class CreateOrderView(ListView):
    model = Dish
    context_object_name = "dishes"
    template_name="food/order_create.html"
    def get_queryset(self):
        foodservice_title = self.kwargs["title"]
        return Dish.objects.filter(foodservice__title=foodservice_title)
    

    


    
