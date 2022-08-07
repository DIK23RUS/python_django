from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from advertisements.models import Advertisement
import random


# Create your views here.

def advertisement_list(request, *args, **kwargs):
    advertisements = {
        'Процессор Ryzen3 3600': 'Продам процессор в отличном состоянии, все вопросы по в чате магазина, без торга',
        'Стиральная машина Bosh': 'Продам стиралку, барабан под замену, в остальном все в полном порядке',
        'Весенняя рассада': 'Саженцы малины, яблок, груши и прочей пенсионерской радости, вопросы по почте',
        'Услуги прокачки персонажей в ММОРПГ': 'Прокачаю Вашего персонажа быстро во всех популярных ММОРПГ'}
    return render(request, 'advertisement/advertisement_list.html', {'advertisements': advertisements})


def advertisement_python(request, *args, **kwargs):
    return render(request, 'advertisement/python.html', {})


def advertisement_web_layout(request, *args, **kwargs):
    return render(request, 'advertisement/web_layout.html', {})


def advertisement_final_project(request, *args, **kwargs):
    return render(request, 'advertisement/final_project.html', {})


def advertisement_contacts(request, *args, **kwargs):
    phone_number = '+7-909-303-22-11'
    email_address = 'dik23rus@gmail.com'
    return render(request, 'advertisement/contacts.html',
                  {'phone_number': phone_number, 'email_address': email_address})


def advertisement_about(request, *args, **kwargs):
    name = 'Бесплатные обьявления'
    info = 'Бесплатные объявления в Вашем городе!'
    return render(request, 'advertisement/about.html', {'Name': name, 'Info': info})


def advertisement_categories(request, *args, **kwargs):
    categories = ['Компьютерная техника', 'Личные вещи', 'Хобби', 'Сад и огород', 'Домашние животные', 'Прочее']
    return render(request, 'advertisement/categories.html', {'categories': categories})


class AdvertisementRegions(View):
    def get(self, request):
        regions = ['Краснодарский край', 'Ростовская область', 'Московская область', 'Республика Адыгея',
                   'Новокубанский район']
        return render(request, 'advertisement/regions.html', {'regions': regions})

    def post(self, request):
        return HttpResponse('Регион успешно создан')


class AdvertisementRandom(View):
    def get(self, request):
        advertisements = Advertisement.objects.all()
        len_list = len(advertisements)
        random_numb = random.randint(0, len_list - 1)
        random_advertisement = advertisements[random_numb]
        return render(request, 'advertisement/random.html', {'random_advertisement': random_advertisement})
