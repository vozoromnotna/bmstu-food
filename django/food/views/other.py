from django.views.generic import ListView
from django.db.models import Prefetch, Subquery, QuerySet, OuterRef
from ..models import *
from datetime import date

class IndexView(ListView):
    model = Foodservice
    template_name = "food/index.html"
    context_object_name = "foodservices"
    def get_queryset(self):
        today = date.today()
        subqry = Subquery(MenuDetails.objects.filter(menu_id=OuterRef('menu_id')).order_by('pk').values_list('id', flat=True)[:4])
        foodservices = Foodservice.objects.prefetch_related(
            Prefetch(
                'menu_set',
                queryset=Menu.objects.filter(date=today).prefetch_related(
                    Prefetch(
                        'menudetails_set',
                        queryset=MenuDetails.objects.filter(id__in=subqry)
                    )
                )
            )
        )
        return foodservices
    
        
        
    

    


    
