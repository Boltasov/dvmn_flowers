from django.urls import path
from . import views


app_name = 'shop'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<int:id>/', views.show_card, name='card'),
    path('order/', views.order, name='order'),
    path('pay/<int:order_id>', views.pay_form, name='pay_form'),
]
