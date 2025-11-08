from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    readonly_fields = ['product_variant', 'quantity', 'added_at']
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'total_items', 'subtotal', 'created_at']
    inlines = [CartItemInline]
    readonly_fields = ['session_key', 'user', 'created_at', 'updated_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product_variant', 'quantity', 'added_at']
    readonly_fields = ['added_at']