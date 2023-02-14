from timeit import default_timer

from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse

from .models import Product, Order
from .forms import CreateProductForm, CreateNewOrderForm


def shop_index(request: HttpRequest):
    products = [
        ('Laptop', 1999),
        ('Desktop', 2999),
        ('Smartphone', 999),
    ]
    context = {
        "time_running": default_timer,
        "products": products
    }
    return render(request, 'shopapp/shop-index.html', context=context)


def groups_list(request: HttpRequest):
    context = {
        "groups": Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, 'shopapp/groups-list.html', context=context)


def products_list(request: HttpRequest):
    context = {
        "products": Product.objects.all()
    }
    return render(request, 'shopapp/products_list.html', context=context)


def orders_list(request: HttpRequest):
    context = {
        "orders": Order.objects.select_related("user").prefetch_related("products").all()
    }
    return render(request, 'shopapp/orders_list.html', context=context)


def create_product(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CreateProductForm(request.POST)
        if form.is_valid():
            Product.objects.create(**form.cleaned_data)
            url = reverse('shopapp:products_list')
            return redirect(url)
    else:
        form = CreateProductForm()
    context = {
        "form": form
    }
    return render(request, "shopapp/create-product.html", context=context)


def create_order(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CreateNewOrderForm(request.POST)
        if form.is_valid():
            delivery_adress = form.cleaned_data['delivery_adress']
            promocode = form.cleaned_data['promocode']
            user = form.cleaned_data['user']
            products = form.cleaned_data['products']
            order = Order.objects.create(delivery_adress=delivery_adress,
                                         promocode=promocode,
                                         user=user)
            for product in products:
                order.products.add(product.id)
            url = reverse('shopapp:orders_list')
            return redirect(url)
    else:
        form = CreateNewOrderForm()
    context = {
        "form": form
    }
    return render(request, "shopapp/create-order.html", context=context)
