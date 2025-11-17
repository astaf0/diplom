from .models import Category
from .forms import SearchForm


def categories_context(request):
    categories = Category.objects.all().order_by('name')
    return {'categories': categories}


def search_form(request):
    initial = {'q': request.GET.get('q', '')}
    return {
        'search_form': SearchForm(initial=initial),
    }