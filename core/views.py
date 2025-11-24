from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Count

from .forms import *
from .models import *



def test404(request):
    return render(request, 'page_404.html')


def custom_404(request, exception):
    return render(request, 'page_404.html', status=404)

def search(request):
    form = SearchForm(request.GET or None)
    products = ProductVariant.objects.all()

    query = request.GET.get('q')

    if query:
        products = ProductVariant.objects.search(query=query)

    sort_form = SortForm(request.GET or None)
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('product__price')
    elif sort == 'price_desc':
        products = products.order_by('-product__price')
    elif sort == 'new':
        products = products.order_by('-created_at')

    context = {
        'form': form,
        'sort_form': sort_form,
        'products': products,
        'query': query,
        'results_count': products.count(),
    }
    return render(request, 'search_results.html', context)



def main(request):
    products = ProductVariant.objects.all()[:8]
    popular_categories = Category.objects.annotate(
        product_count=Count('product')
    ).order_by('-product_count')
    context = {
        'products': products,
        'popular_categories': popular_categories,
    }
    return render(request, 'index.html', context)


def catalog_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    popular_categories = Category.objects.annotate(
        product_count=Count('product')
    ).order_by('-product_count')
    products = ProductVariant.objects.all().filter(product__category__slug=category_slug)

    sort_form = SortForm(request.GET or None)

    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('product__price')
    elif sort == 'price_desc':
        products = products.order_by('-product__price')
    elif sort == 'new':
        products = products.order_by('-created_at')


    context = {
        'category': category,
        'popular_categories': popular_categories,
        'products': products,
        'sort_form': sort_form,
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
    user_has_review = False
    if request.user.is_authenticated:
        user_has_review = product.reviews.filter(user=request.user).exists()

    if request.method == 'POST':
        if request.user.is_authenticated:
            if not user_has_review:
                form = AddProductReviewForm(request.POST)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.user = request.user
                    review.product = product
                    review.save()
                    return redirect('product_details',
                                  product_slug=product_slug,
                                  color_slug=color_slug)
        else:
            return redirect('login')
    else:
        form = AddProductReviewForm()

    context = {
        'product': product,
        'product_variant': product_variant,
        'product_colors': product_colors,
        'reviews': reviews,
        'form': form,
        'images': images,
        'user_has_review': user_has_review,
    }
    return render(request, 'product_details.html', context)



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