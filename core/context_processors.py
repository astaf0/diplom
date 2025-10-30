from .models import Category
from django.db.models import Count


def categories_context(request):
    product_count = Count('product')
    categories = Category.objects.annotate(
        product_count=Count('product')
    ).order_by('-product_count')

    return {
        'categories_sorted_pr_num': categories,
        'product_count': product_count
    }