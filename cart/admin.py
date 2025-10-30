from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product_variant']
    readonly_fields = ['added_at']
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'total_items', 'subtotal', 'created_at']
    list_filter = ['created_at']
    search_fields = ['session_key']
    inlines = [CartItemInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product_name', 'color_name', 'quantity', 'total_price', 'added_at']
    list_filter = ['added_at', 'cart']
    search_fields = ['cart__session_key', 'product_variant__product__name']
    raw_id_fields = ['cart', 'product_variant']
    readonly_fields = ['added_at']

    def product_name(self, obj):
        return obj.product_variant.product.name

    product_name.short_description = 'Товар'

    def color_name(self, obj):
        return obj.product_variant.color.name

    color_name.short_description = 'Цвет'