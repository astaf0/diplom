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


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


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


class Color(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    main_image = models.ImageField(upload_to='products/main/')
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.color.name}"


class ProductVariantImage(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/extra/')


class ProductReview(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст отзыва', blank=True)
    rating = models.IntegerField(verbose_name='Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
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
