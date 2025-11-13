from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import ProductVariant
from .forms import CartAddForm, CartUpdateForm


def cart_details(request):
    cart_data = request.cart.get_cart_data()

    for item in cart_data['items']:
        item.update_form = CartUpdateForm(initial={'quantity': item.quantity})

    context = {
        'cart': request.cart,
        'cart_data': cart_data,
    }
    return render(request, 'cart/cart_details.html', context)


@require_POST
def add_to_cart(request, variant_id):
    product_variant = get_object_or_404(ProductVariant, id=variant_id)
    form = CartAddForm(request.POST)

    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        request.cart.add_product(product_variant, quantity)
    return redirect(request.META.get('HTTP_REFERER', 'cart:details'))


@require_POST
def update_cart_item(request, item_id):
    form = CartUpdateForm(request.POST)

    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        request.cart.update_item_quantity(item_id, quantity)
    return redirect(request.META.get('HTTP_REFERER', 'cart:details'))


@require_POST
def remove_from_cart(request, item_id):
    request.cart.remove_item(item_id)
    return redirect('cart:details')


def clear_cart(request):
    request.cart.clear()
    return redirect('cart:details')
