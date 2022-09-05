from django.db import models


# Create your models here.

class Advertisement(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    description = models.TextField(null=True, default='', verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    price = models.IntegerField(verbose_name='Цена', default=0)
    views_count = models.IntegerField(verbose_name='Количество просмотров', default=0)
    status = models.ForeignKey('AdvertisementStatus', default=None, null=True, on_delete=models.CASCADE,
                               related_name='advertisements', verbose_name='Статус')
    type = models.ForeignKey('AdvertisementType', default=None, null=True, on_delete=models.CASCADE, verbose_name='Тип')
    heading = models.ForeignKey('AdvertisementHeading', default=None, null=True, on_delete=models.CASCADE,
                                verbose_name='Категория')
    author = models.ForeignKey('Author', default=None, null=True, on_delete=models.CASCADE, verbose_name='Автор')


    def __str__(self):
        return self.title

    class Meta:
        db_table = "Advertisement"


class AdvertisementStatus(models.Model):
    name = models.CharField(max_length=100, verbose_name='Статус')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "AdvertisementStatus"


class AdvertisementType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Тип')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "AdvertisementType"


class AdvertisementHeading(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "AdvertisementHeading"


class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name='ФИО')
    email = models.EmailField(max_length=50, verbose_name='Почта')
    phone = models.CharField(max_length=15, verbose_name='Номер телефона')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Author"
