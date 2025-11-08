from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from core.models import ProductVariant

User = get_user_model()


class Order(models.Model):
    STATUS_CHOICES = [
        ('В обработке', 'В обработке'),
        ('Принят', 'Принят'),
        ('Отменен', 'Отменен'),
        ('Собирается', 'Собирается'),
        ('Готов к доставке', 'Готов к доставке'),
        ('Завершен', 'Завершен'),
        ('Возвращен', 'Возвращен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        choices=STATUS_CHOICES,
        default='В обработке',
    )
    email = models.EmailField()
    phone = PhoneNumberField(region='RU')
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    building = models.CharField(max_length=10)
    entrance = models.CharField(max_length=10, blank=True, null=True)
    flat = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ {self.id}, {self.email}"

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant,  on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} шт. {self.product_variant}"

    class Meta:
        verbose_name = 'товар заказа'
        verbose_name_plural = 'товары заказа'