from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=1,
    )


class CartUpdateForm(forms.Form):
    quantity = forms.IntegerField()