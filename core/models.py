from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Count
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'бренд'
        verbose_name_plural = 'бренды'


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def average_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or None

    def get_rating_display(self):
        avg_rating = self.average_rating()
        return f"{avg_rating:.1f}" if avg_rating else "Нет оценок"

    def reviews_count(self):
        return self.reviews.count()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class Color(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'цвет'
        verbose_name_plural = 'цвета'


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    main_image = models.ImageField(upload_to='products/main/')
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'вариант товара'
        verbose_name_plural = 'варианты товара'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.color.name}"


class ProductVariantImage(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/extra/')

    class Meta:
        verbose_name = 'фотография товара'
        verbose_name_plural = 'фотографии товара'


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ['-created_at']
        unique_together = ['product', 'user']

    def get_relative_date(self):
        now = timezone.now()
        today = now.date()

        if self.created_at.date() == today:
            return f"сегодня в {self.created_at.strftime('%H:%M')}"

        elif self.created_at.date() == today - timezone.timedelta(days=1):
            return f"вчера в {self.created_at.strftime('%H:%M')}"

        else:
            return self.created_at.strftime("%d.%m.%Y")

    def __str__(self):
        return self.text[:40]
