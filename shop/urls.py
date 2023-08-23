from django.urls import path
from . import views


app_name = 'shop'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('catalog/', views.catalog, name='catalog'),
]