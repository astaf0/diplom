from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Order, OrderItem

@login_required
def new_order(request):
    cart_data = request.cart.get_cart_data()
    print(request.POST)

    if not cart_data['items']:
        return redirect('cart:detail')

    initial_data = {
        'email': request.user.email,
        'phone': getattr(request.user, 'phone', ''),
    }

    if request.method == 'POST':
        form = OrderForm(request.POST, initial=initial_data)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = request.cart.subtotal
            order.user = request.user
            order.save()

            for cart_item in cart_data['items']:
                OrderItem.objects.create(
                    order=order,
                    product_variant=cart_item.product_variant,
                    price=cart_item.product_variant.product.price,
                    quantity=cart_item.quantity,
                )
            request.cart.clear()
            return redirect('main')
    else:
        form = OrderForm(initial=initial_data)

    context = {
        'cart_data': cart_data,
        'form': form,
    }
    return render(request, 'orders/checkout.html', context)


def my_orders(request):
    orders = Order.objects.all().filter(user=request.user)
    context = {
        'orders': orders,
    }

    return render(request, 'orders/my_orders.html', context)
