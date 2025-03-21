from django.db import models
from users.models import User

class NewModel(models.Model):
    name = models.CharField(max_length=300, verbose_name="заголовок")
    description = models.TextField(verbose_name="содержимое")
    photo = models.ImageField(upload_to="newmodel/photo", verbose_name="Превью", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="признак публикации", auto_now=True)
    views_counter = models.PositiveIntegerField(verbose_name='количество просмотров', default=0)

    class Meta:
        verbose_name = "Модель"
        verbose_name_plural = "Модели"


    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="наименование продукта")
    description = models.TextField(verbose_name="описание продукта", blank=True, null=True)
    photo = models.ImageField(upload_to="product/photo", verbose_name="Фото продукта", blank=True, null=True)
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        verbose_name="категория",
        blank=True,
        null=True,
        related_name="products",
    )
    price = models.IntegerField(verbose_name="цена за покупку")
    created_at = models.DateTimeField(verbose_name="дата создания", auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(verbose_name="дата последнего изменения", auto_now=True, blank=True, null=True)
    views_counter = models.PositiveIntegerField(verbose_name='количество просмотров', default=0)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Владелец')
    publish_product = models.BooleanField(default=True, blank=True, null=True)


    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['category', 'name']
        permissions = [
            ('can_unpublish_product', 'Can unpublish product')
        ]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="наименование категории")
    description = models.TextField(verbose_name="описание категории", blank=True, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
