from django.shortcuts import render
from . models import *

# Create your views here.

def shop(request):
    artikel = Artikel.objects.all()
    ctx = {'artikel': artikel}
    return render(request, 'shop/shop.html', ctx)

def warenkorb(request):
    if request.user.is_authenticated:
        kunde = request.user.kunde
        bestellung, created = Bestellung.objects.get_or_create(kunde=kunde, erledigt=False)
        artikel = bestellung.bestellteartikel_set.all()
    else:
        artikel = []
    ctx = {'artikel': artikel}
    return render(request, 'shop/warenkorb.html', ctx)

def kasse(request):
    return render(request, 'shop/kasse.html')