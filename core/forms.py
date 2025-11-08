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