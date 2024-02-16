from django.urls import path

from .views import hello_world_view, GroupsListView, ProductListView, OrderListView


app_name = "myapiapp"

urlpatterns = [
    path("hello/", hello_world_view, name="hello"),
    path("groups/", GroupsListView.as_view(), name="groups"),
    path("products/", ProductListView.as_view(), name="products"),
    path("orders/", OrderListView.as_view(), name="Orders"),
]