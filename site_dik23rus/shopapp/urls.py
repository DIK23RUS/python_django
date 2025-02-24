from django.urls import path, include
from rest_framework.routers import DefaultRouter

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
                    OrderCreateView,
                    ProductsDataExportView,
                    OrdersDataExportView,
                    ProductViewSet,
                    OrderViewSet,
                    LatestProductsFeed,
                    BuyerListView,
                    BuyerOrdersListView,
                    BuyerOrdersListExportView,
                    )

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    path("", ShoppIndexView.as_view(), name="index"),
    path("api/", include(routers.urls)),
    path("groups/", GroupsView.as_view(), name="groups_list"),
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/<int:pk>/", ProductDeteilsView.as_view(), name="products_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="products_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="products_delete"),
    path("products/create/", ProductCreateView.as_view(), name="product-create"),
    path("products/export/", ProductsDataExportView.as_view(), name="products-export"),
    path("orders/", OrderListView.as_view(), name="orders_list"),
    path("orders/<int:pk>/", OrderDetailsView.as_view(), name="order_details"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/export/", OrdersDataExportView.as_view(), name="orders-export"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("products/latest/feed/", LatestProductsFeed(), name="products-feed"),
    path("buyers/", BuyerListView.as_view(), name="buyers_list"),
    path("buyers/<int:pk>/", BuyerOrdersListView.as_view(), name="buyer_order_list"),
    path("buyers/<int:pk>/export/", BuyerOrdersListExportView.as_view(), name="buyer_order_export"),
    # path("orders/create/", create_order, name="create-order"),
]
