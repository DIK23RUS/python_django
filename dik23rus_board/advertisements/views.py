from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def advertisement_list(request, *args, **kwargs):
    return render(request, 'advertisement/advertisement_list.html', {})


def advertisement_python(request, *args, **kwargs):
    return render(request, 'advertisement/python.html', {})


def advertisement_web_layout(request, *args, **kwargs):
    return render(request, 'advertisement/web_layout.html', {})


def advertisement_final_project(request, *args, **kwargs):
    return render(request, 'advertisement/final_project.html', {})
