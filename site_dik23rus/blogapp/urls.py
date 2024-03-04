from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (ArticleListView,)


app_name = "blogapp"

routers = DefaultRouter()
routers.register("articles", ArticleListView)

urlpatterns = [
    path("articles/", ArticleListView.as_view(), name="articles"),
]