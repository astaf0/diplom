from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import *
from .models import *
from .filters import *



def main(request):
    products = ProductVariant.objects.all()[:8]
    context = {'products': products}
    return render(request, 'index.html', context)


def catalog_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = ProductVariant.objects.all().filter(product__category__slug=category_slug)

    product_filter = ProductFilter(request.GET, queryset=products)

    context = {
        'category': category,
        'filter': product_filter,
        'products': product_filter.qs,
    }
    return render(request, 'catalog_category.html', context)


def product_details(request, product_slug, color_slug):
    product = get_object_or_404(Product, slug=product_slug)
    product_variant = get_object_or_404(
        ProductVariant.objects.select_related('product', 'color'),
        product__slug=product_slug,
        color__slug=color_slug
    )

    images = ProductVariantImage.objects.filter(variant=product_variant)

    product_colors = ProductVariant.objects.filter(
        product__slug=product_slug
    ).select_related('color')

    reviews = product.reviews.all()

    if request.method == 'POST':
        form = AddProductReviewForm(request.POST, user=request.user)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product

            if request.user.is_authenticated:
                review.user = request.user
                review.author = request.user.username
            else:
                review.user = None
                review.author = form.cleaned_data['author']

            review.save()
            return redirect('product_details',
                            product_slug=product_slug, color_slug=color_slug)
    else:
        form = AddProductReviewForm(user=request.user)

    context = {
        'product': product,
        'product_variant': product_variant,
        'product_colors': product_colors,
        'reviews': reviews,
        'form': form,
        'images': images
    }
    return render(request, 'product_details.html', context)


@require_POST
def delete_review(request, review_id):
    review_to_delete = get_object_or_404(ProductReview, id=review_id)
    review_to_delete.delete()
    return redirect('reviews')



# -------------------------------------------------------------------------
# Для авторизованных пользователей


@login_required
def my_reviews(request):
    user = request.user
    reviews = ProductReview.objects.filter(user=user)
    context = {'reviews': reviews,}
    return render(request, 'my_reviews.html', context)


@login_required
@require_POST
def delete_my_review(request, review_id):
    user = request.user
    review_to_delete = get_object_or_404(ProductReview, id=review_id, user=user)
    review_to_delete.delete()
    return redirect('my_reviews')