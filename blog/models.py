from django.db import models


class Article(models.Model):
    name = models.CharField(max_length=300, verbose_name="заголовок")
    description = models.TextField(verbose_name="содержимое")
    photo = models.ImageField(
        upload_to="blog/photo", verbose_name="Превью", blank=True, null=True
    )
    created_at = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="признак публикации", auto_now=True)
    views_counter = models.PositiveIntegerField(
        verbose_name="количество просмотров", default=0
    )


class Meta:
    verbose_name = "Модель"
    verbose_name_plural = "Модели"


def __str__(self):
    return self.name
