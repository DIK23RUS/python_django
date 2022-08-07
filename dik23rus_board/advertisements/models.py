from django.db import models


# Create your models here.

class Advertisement(models.Model):
    title = models.CharField(max_length=1500)
    description = models.TextField(null=True, default='', verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.IntegerField(verbose_name='Цена', default=0)
    views_count = models.IntegerField(verbose_name='Количество просмотров', default=0)
