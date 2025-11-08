from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = ([
    path('checkout', new_order, name='new_order'),
    path('my', my_orders, name='my_orders'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))