from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', cart_details, name='details'),
    path('add/<int:variant_id>', add_to_cart, name='add'),
    path('update/<int:item_id>', update_cart_item, name='update'),
    path('remove/<int:item_id>', remove_from_cart, name='remove'),
    path('clear', clear_cart, name='clear'),
]