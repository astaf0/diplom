from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = ([
    path('', main, name='main'),
    path('catalog/<str:category_slug>', catalog_category, name='catalog_category'),
    path('products/<str:product_slug>-<str:color_slug>', product_details, name='product_details'),
    path('reviews/my', my_reviews, name='my_reviews'),
    path('reviews/my/<int:review_id>/delete', delete_my_review, name='delete_my_review'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))