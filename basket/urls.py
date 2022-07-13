from django.urls import path

from . import views

from basket.transbankpay import webpay_plus_create, commitpay

app_name = 'basket'

urlpatterns = [
    path('', views.basket_summary, name='basket_summary'),
    path('add/', views.basket_add, name='basket_add'),
    path('delete/', views.basket_delete, name='basket_delete'),
    path('update/', views.basket_update, name='basket_update'),
    path('webpay-plus-create', webpay_plus_create, name='webpay-plus-create'),
    path('commit-pay/', commitpay),
]
