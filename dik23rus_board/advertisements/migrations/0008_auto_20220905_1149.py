# Generated by Django 2.2 on 2022-09-05 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0007_auto_20220905_1108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='advertisements',
        ),
        migrations.AddField(
            model_name='advertisements',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='advertisements.Author', verbose_name='Автор'),
        ),
    ]
