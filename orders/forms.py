from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Order


class OrderForm(forms.ModelForm):
    phone = PhoneNumberField(
        label='Телефон',
        region='RU',
        widget=forms.TextInput(attrs={
            'placeholder': '+7 999 999 99 99',
        })
    )

    class Meta:
        model = Order
        fields = [
            'email', 'phone', 'city', 'street',
            'building', 'entrance', 'flat'
        ]
        labels = {
            'email': 'Email',
            'city': 'Город',
            'street': 'Улица',
            'building': 'Дом',
            'entrance': 'Подъезд',
            'flat': 'Квартира',
        }

