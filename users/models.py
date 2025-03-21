from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import forms

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='user/avatars', verbose_name='аватар', blank=True, null=True)
    phone_number = models.CharField(max_length=15, verbose_name='номер телефона', blank=True, null=True)
    country = models.CharField(max_length=200, verbose_name='Страна', blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Номер телефона должен состоять только из цифр')
        return phone_number

    def __str__(self):
        return self.email