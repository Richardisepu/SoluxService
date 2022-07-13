from django.shortcuts import render

def red_tiendas(request):
    
    return render(request, 'generic/redTiendas.html')


def preguntas_frecuentes(request):    
    return render(request, 'generic/FAQs.html')

def acerca_de(request):    
    return render(request, 'generic/about-us.html')