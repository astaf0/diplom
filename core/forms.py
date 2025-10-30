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
        fields = ['author', 'text', 'rating']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user and self.user.is_authenticated:
            self.fields['author'].widget = forms.HiddenInput()
            self.fields['author'].required = False

        for field_name in self.fields:
            self.fields[field_name].help_text = None
            self.fields[field_name].widget.attrs.update({
                'autocomplete': 'off',
            })
        self.fields['text'].widget.attrs.update({
            'rows': 3,
        })
        self.fields['author'].label = 'Ваше имя'