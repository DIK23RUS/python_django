"""
В этом модуле лежат различные наборы представлений.

Разные view для интернет-магазина: по товарам, заказам и т.д.
"""
import logging
from timeit import default_timer

from django.core.cache import cache
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth.models import Group
from django.forms import CheckboxSelectMultiple
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.syndication.views import Feed
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Product, Order, ProductImage
from .forms import CreateProductForm, CreateNewOrderForm, GroupForm, ProductForm
from .serializers import ProductSerializer, OrderSerializer

log = logging.getLogger(__name__)

@extend_schema(description="Products view CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    Полный CRUD для сущностей товаров.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "description",
    ]
    @extend_schema(
        summary="Get one Product by ID",
        description="Retrieves **product**, return 404 if product not found",
        responses= {
            200: ProductSerializer,
            404: OpenApiResponse(description='Empty response, product by ID not found'),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = [
        "delivery_adress",
        "promocode",
        "created_at",
        "user",
    ]
    ordering_fields = [
        "user",
        "products",
        "created_at",
    ]



class ShoppIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer,
            "products": products,
            "items": 5,
        }
        log.debug("Products for shop index: %s", products)
        log.info("Rendering shop index")
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


# def groups_list(request: HttpRequest):
#     context = {
#         "groups": Group.objects.prefetch_related('permissions').all(),
#     }
#     return render(request, 'shopapp/groups-list.html', context=context)


class ProductDeteilsView(DetailView):
    template_name = "shopapp/product-deteils.html"
    # model = Product
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


# class ProductDeteilsView(View):
#     def get(self, request: HttpRequest, pk: int) -> HttpResponse:
#         product = get_object_or_404(Product, pk=pk)
#         context = {
#             "product": product
#         }
#         return render(request,'shopapp/product-deteils.html', context=context)
#

class ProductListView(ListView):
    template_name = "shopapp/products_list.html"
    # model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


# class ProductListView(TemplateView):
#     template_name = "shopapp/products_list.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['products'] = Product.objects.all()
#         return context


# def products_list(request: HttpRequest):
#     context = {
#         "products": Product.objects.all()
#     }
#     return render(request, 'shopapp/products_list.html', context=context)


# def orders_list(request: HttpRequest):
#     context = {
#         "orders": Order.objects.select_related("user").prefetch_related("products").all()
#     }
#     return render(request, 'shopapp/order_list.html', context=context)


class OrderListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderCreateView(CreateView):
    model = Order
    fields = "delivery_adress", "promocode", "user", "products"
    success_url = reverse_lazy('shopapp:orders_list')


class OrderUpdateView(UpdateView):
    model = Order
    fields = "delivery_adress", "promocode", "user", "products"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            'shopapp:order_details',
            kwargs={'pk': self.object.pk}
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "shopapp.add_product"
    # def test_func(self):
    #     # return self.request.user.groups.filter(name="secret-group")
    #     return self.request.user.is_superuser
    model = Product
    fields = "name", "price", "description", "discount", "preview"
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "shopapp.change_product"

    def test_func(self):
        return self.get_object().created_by == self.request.user \
            or self.request.user.is_superuser

    model = Product
    # fields = "name", "price", "description", "discount", "preview"
    template_name_suffix = "_update_form"
    form_class = ProductForm

    def get_success_url(self):
        return reverse(
            'shopapp:products_details',
            kwargs={'pk': self.object.pk}
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


# def create_product(request: HttpRequest) -> HttpResponse:
#     if request.method == 'POST':
#         form = CreateProductForm(request.POST)
#         if form.is_valid():
#             Product.objects.create(**form.cleaned_data)
#             url = reverse('shopapp:products_list')
#             return redirect(url)
#     else:
#         form = CreateProductForm()
#     context = {
#         "form": form
#     }
#     return render(request, "shopapp/create-product.html", context=context)


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


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by("pk").all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived,
            }
            for product in products
        ]
        elem = products_data[0]
        name = elem["name"]
        print("name:", name)
        return JsonResponse({"products": products_data})


class OrdersDataExportView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.select_related("user").prefetch_related("products").all()
        orders_data = [
            {
                "pk": order.pk,
                "delivery_adress": order.delivery_adress,
                "promocode": order.promocode,
                "user": order.user.id,
                "products": product.id,
            }
            for order in orders
            for product in order.products.all()
        ]
        return JsonResponse({"orders": orders_data})


class LatestProductsFeed(Feed):
    title = "Products news"
    description = "Updates product list"
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return Product.objects.filter(archived=False).order_by("-created_at")[:5]
    
    def item_title(self, item:Product):
        return item.name
    
    def item_description(self, item:Product):
        return item.description
    

class BuyerListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "shopapp/buyers_list.html"
    context_object_name = "buyers"

    def get_queryset(self):
        return User.objects.annotate(
            order_count=Count("order")
        ).filter(order_count__gt=0)
    

class BuyerOrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "shopapp/buyers_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return Order.objects.filter(user=user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buyer'] = get_object_or_404(User, pk=self.kwargs['pk'])
        return context
    

class BuyerOrdersListExportView(LoginRequiredMixin, APIView):
    def get(self, request, pk):
        
        cache_key = f"user_orders_export_{pk}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        user = get_object_or_404(User, pk=pk)

        orders = Order.objects.filter(user=user).order_by('id')
        serializer = OrderSerializer(orders, many=True)
        cache.set(cache_key, serializer.data, timeout=120)

        return Response(serializer.data, status=status.HTTP_200_OK)