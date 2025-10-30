from django.db import models
from core.models import ProductVariant
from decimal import Decimal


class Cart(models.Model):
    session_key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.session_key

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    def add_product(self, product_variant, quantity=1):
        if quantity > product_variant.stock:
            quantity = product_variant.stock

        if quantity <= 0:
            return None

        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            product_variant=product_variant,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product_variant.stock:
                cart_item.quantity = product_variant.stock
            cart_item.save()
        return cart_item


    def remove_item(self, item_id):
        try:
            item = self.items.get(id=item_id)
            item.delete()
            return True
        except CartItem.DoesNotExist:
            return False

    def update_item_quantity(self, item_id, quantity):
        try:
            item = self.items.get(id=item_id)
            if quantity > 0:
                if quantity > item.product_variant.stock:
                    quantity = item.product_variant.stock
                item.quantity = quantity
                item.save()
            else:
                item.delete()
            return True
        except CartItem.DoesNotExist:
            return False

    def clear(self):
        self.items.all().delete()

    def get_cart_data(self):
        items = self.items.select_related('product_variant__product', 'product_variant__color').all()
        cart_data = {
            'items': items,
            'total_items': self.total_items,
            'subtotal': self.subtotal,
        }
        return cart_data


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product_variant')

    def __str__(self):
        return f"{self.product_variant} x {self.quantity}"

    @property
    def total_price(self):
        return Decimal(str(self.product_variant.product.price)) * self.quantity
