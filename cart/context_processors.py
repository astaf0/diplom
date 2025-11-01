from .models import Cart


def cart_context(request):
    if hasattr(request, 'cart'):
        return {
            'cart_total_items': request.cart.total_items,
            'cart_subtotal': request.cart.subtotal,
            'cart': request.cart,
        }
    else:
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()

            cart, created = Cart.objects.get_or_create(
                session_key=request.session.session_key
            )

        return {
            'cart_total_items': cart.total_items,
            'cart_subtotal': cart.subtotal,
            'cart': cart,
        }