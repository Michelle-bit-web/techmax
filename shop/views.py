from django.shortcuts import render
from . models import *

# Create your views here.

def shop(request):
    artikel = Artikel.objects.all()
    ctx = {'artikel': artikel}
    return render(request, 'shop/shop.html', ctx)

def warenkorb(request):
    return render(request, 'shop/warenkorb.html')

def kasse(request):
    return render(request, 'shop/kasse.html')