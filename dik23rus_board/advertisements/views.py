from django.shortcuts import render
from django.http import HttpResponse
from django.views import View, generic
from advertisements.models import Advertisement
import random


# Create your views here.

def advertisement_python(request, *args, **kwargs):
    return render(request, 'advertisements/python.html', {})


def advertisement_web_layout(request, *args, **kwargs):
    return render(request, 'advertisements/web_layout.html', {})


def advertisement_final_project(request, *args, **kwargs):
    return render(request, 'advertisements/final_project.html', {})


def advertisement_contacts(request, *args, **kwargs):
    phone_number = '+7-909-303-22-11'
    email_address = 'dik23rus@gmail.com'
    return render(request, 'advertisements/contacts.html',
                  {'phone_number': phone_number, 'email_address': email_address})


def advertisement_about(request, *args, **kwargs):
    name = 'Бесплатные обьявления'
    info = 'Бесплатные объявления в Вашем городе!'
    return render(request, 'advertisements/about.html', {'Name': name, 'Info': info})


def advertisement_categories(request, *args, **kwargs):
    categories = ['Компьютерная техника', 'Личные вещи', 'Хобби', 'Сад и огород', 'Домашние животные', 'Прочее']
    return render(request, 'advertisements/categories.html', {'categories': categories})


class AdvertisementRegions(View):
    def get(self, request):
        regions = ['Краснодарский край', 'Ростовская область', 'Московская область', 'Республика Адыгея',
                   'Новокубанский район']
        return render(request, 'advertisements/regions.html', {'regions': regions})

    def post(self, request):
        return HttpResponse('Регион успешно создан')


class AdvertisementRandom(View):
    def get(self, request):
        advertisements = Advertisement.objects.all()
        len_list = len(advertisements)
        random_numb = random.randint(0, len_list - 1)
        random_advertisement = advertisements[random_numb]
        return render(request, 'advertisements/random.html', {'random_advertisement': random_advertisement})


class AdvertisementListView(generic.ListView):
    model = Advertisement
    template_name = 'dik23rus_board/advertisements/templates/advertisements/advertisement_list.html'
    context_object_name = 'advertisement_list'
    queryset = Advertisement.objects.all()


class AdvertisementDetailView(generic.DetailView):
    model = Advertisement