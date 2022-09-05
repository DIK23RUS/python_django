from django.urls import path
from . import views

urlpatterns = [
    # path('', views.advertisement_list, name='advertisement_list'),
    path('', views.AdvertisementListView.as_view(), name='advertisement'),
    path('<int:pk>/', views.AdvertisementDetailView.as_view(), name='advertisement-detail'),
    path('python/', views.advertisement_python, name='advertisement_python'),
    path('web_layout/', views.advertisement_web_layout, name='advertisement_web_layout'),
    path('final_project/', views.advertisement_final_project, name='advertisement_final_project'),
    path('contacts/', views.advertisement_contacts, name='advertisement_contacts'),
    path('about/', views.advertisement_about, name='advertisement_about'),
    path('categories/', views.advertisement_categories, name='advertisement_categories'),
    path('regions/', views.AdvertisementRegions.as_view()),
    path('random/', views.AdvertisementRandom.as_view()),
]
