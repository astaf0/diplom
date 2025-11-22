from django import forms
from .models import *


class AddProductReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1 звезда'),
        (2, '2 звезды'),
        (3, '3 звезды'),
        (4, '4 звезды'),
        (5, '5 звезд'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
    )
    class Meta:
        model = ProductReview
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
            }),
        }
        labels = {
            'text': 'Текст отзыва',
        }


class SearchForm(forms.Form):
    q = forms.CharField(
        label='',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'class': 'form-control search-input',
            'placeholder': 'Поиск'
        })
    )


class SortForm(forms.Form):
    SORT_CHOICES = [
        ('', 'Без сортировки'),
        ('price_asc', 'Дешевые'),
        ('price_desc', 'Дорогие'),
        ('new', 'Новые'),
    ]

    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='',
        widget=forms.RadioSelect(attrs={
            'onchange': 'this.form.submit()',
        })
    )