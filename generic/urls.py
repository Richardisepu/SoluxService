from django.urls import path

from . import views

app_name = 'generic'

urlpatterns = [
    path('', views.red_tiendas, name='red_tiendas'),
    path('preguntas_frecuentes', views.preguntas_frecuentes, name='preguntas_frecuentes'),
    path('acerca_de_nosotros', views.acerca_de, name='acerca_de_nosotros'),
]