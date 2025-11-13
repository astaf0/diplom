from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['order', 'product_variant', 'price', 'quantity']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'status', 'created_at']
    search_fields = ['user']
    inlines = [OrderItemInline]
    readonly_fields = ['email', 'phone', 'city', 'street',
                       'building', 'flat', 'created_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_variant', 'price', 'quantity']
    readonly_fields = ['order', 'product_variant', 'price', 'quantity']

