from django.urls import path
from .views import *


urlpatterns = ([
    path('checkout', new_order, name='new_order'),
    path('my', my_orders, name='my_orders'),

])