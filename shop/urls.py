from django.urls import path
from . import views


app_name = 'shop'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<int:id>/', views.show_card, name='card'),
    path('order/', views.order, name='order'),
    path('pay/<int:order_id>', views.pay_form, name='pay_form'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz_step/<int:event_id>', views.quiz_step, name='quiz_step'),
    path('result/<int:event_id>/<str:price_level>', views.result, name='result'),
    path('consultation/', views.consultation, name='consultation'),
]
