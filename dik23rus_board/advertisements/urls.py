from django.urls import path
from .import views

urlpatterns = [
    path('', views.advertisement_list, name='advertisement_list'),
    path('python/', views.advertisement_python, name='advertisement_python'),
    path('web_layout/', views.advertisement_web_layout, name='advertisement_web_layout'),
    path('final_project/', views.advertisement_final_project, name='advertisement_final_project')
]