import django_filters
from django import forms
from .models import ProductVariant


class ProductFilter(django_filters.FilterSet):
    price_range_min = django_filters.NumberFilter(
        field_name='product__price',
        lookup_expr='gte',
        label='',
        widget=forms.NumberInput(attrs={
            'class': 'form-control border-bottom p-2',
            'placeholder': 'От'
        })
    )

    price_range_max = django_filters.NumberFilter(
        field_name='product__price',
        lookup_expr='lte',
        label='',
        widget=forms.NumberInput(attrs={
            'class': 'form-control border-bottom p-2',
            'placeholder': 'До'
        })
    )

    in_stock = django_filters.BooleanFilter(
        method='filter_in_stock',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        label='В наличии'
    )

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset

    color = django_filters.CharFilter(
        field_name='color__name',
        lookup_expr='icontains',
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control border-bottom p-2',
            'placeholder': 'Цвет'
        })
    )

    brand = django_filters.CharFilter(
        field_name='product__brand__name',
        lookup_expr='icontains',
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control border-bottom p-2',
            'placeholder': 'Бренд'
        })
    )

    class Meta:
        model = ProductVariant
        fields = ['price_range_min', 'price_range_max', 'brand', 'in_stock', 'color']