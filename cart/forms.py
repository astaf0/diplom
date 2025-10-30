from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        max_value=100,
        initial=1,
        widget=forms.NumberInput()
    )


class CartUpdateForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=0,
        max_value=100,
        initial=1,
        widget=forms.NumberInput()
    )