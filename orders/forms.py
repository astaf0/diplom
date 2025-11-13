from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Order


class OrderForm(forms.ModelForm):
    phone = PhoneNumberField(
        label='Телефон',
        region='RU',
    )

    class Meta:
        model = Order
        fields = [
            'email', 'phone', 'city', 'street',
            'building', 'flat'
        ]
        labels = {
            'email': 'Email',
            'city': 'Город',
            'street': 'Улица',
            'building': 'Дом',
            'flat': 'Квартира',
        }

