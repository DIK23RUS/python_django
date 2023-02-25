from django.urls import path

from .views import (ShoppIndexView,
                    GroupsView,
                    ProductListView,
                    ProductDeteilsView,
                    OrderListView,
                    OrderDetailsView,
                    ProductCreateView,
                    ProductUpdateView,
                    create_order,
                    ProductDeleteView,
                    OrderUpdateView,
                    OrderDeleteView,
                    OrderCreateView)

app_name = "shopapp"
urlpatterns = [
    path("", ShoppIndexView.as_view(), name="index"),
    path("groups/", GroupsView.as_view(), name="groups_list"),
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/<int:pk>/", ProductDeteilsView.as_view(), name="products_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="products_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="products_delete"),
    path("products/create/", ProductCreateView.as_view(), name="product-create"),
    path("orders/", OrderListView.as_view(), name="orders_list"),
    path("orders/<int:pk>/", OrderDetailsView.as_view(), name="order_details"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    # path("orders/create/", create_order, name="create-order"),
]
