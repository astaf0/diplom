from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import random
import string


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен для заполнения')
        email = self.normalize_email(email)

        if not extra_fields.get('username'):
            extra_fields['username'] = generate_username()

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


def generate_username():
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    return f'Пользователь-{random_part}'


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email адрес', unique=True)
    username = models.CharField('имя пользователя', max_length=150, unique=True)
    phone = models.CharField('телефон', max_length=20, blank=True)
    is_active = models.BooleanField('активен', default=True)
    is_staff = models.BooleanField('сотрудник', default=False)
    date_joined = models.DateTimeField('дата регистрации', default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = generate_username()
        super().save(*args, **kwargs)
