from django.views.generic import ListView
from django.db.models import Prefetch
from ..models import *

class IndexView(ListView):
    model = Foodservice
    template_name = "food/index.html"
    context_object_name = "foodservices"
    def get_queryset(self):
        foodservices = Foodservice.objects.prefetch_related(
            Prefetch(
                'menu_set',
                queryset=Menu.objects.prefetch_related(
                    Prefetch(
                        'menudetails_set',
                        queryset=MenuDetails.objects.select_related('dish')
                    )
                )
            )
        )
        return foodservices
    
        
        
    

    


    
