from django.db.models.signals import pre_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart, CartItem


@receiver(user_logged_in)
def migrate_cart_on_login(sender, request, user, **kwargs):
    anonymous_cart = getattr(request, 'cart', None)

    if anonymous_cart and anonymous_cart.items.exists():
        user_cart, created = Cart.objects.get_or_create(user=user)

        if not created:
            for anonymous_item in anonymous_cart.items.all():
                try:
                    user_item = user_cart.items.get(
                        product_variant=anonymous_item.product_variant
                    )
                    new_quantity = user_item.quantity + anonymous_item.quantity
                    if new_quantity > anonymous_item.product_variant.stock:
                        new_quantity = anonymous_item.product_variant.stock
                    user_item.quantity = new_quantity
                    user_item.save()
                except CartItem.DoesNotExist:
                    CartItem.objects.create(
                        cart=user_cart,
                        product_variant=anonymous_item.product_variant,
                        quantity=anonymous_item.quantity
                    )
        else:
            anonymous_cart.items.update(cart=user_cart)

        anonymous_cart.delete()

        request.cart = user_cart