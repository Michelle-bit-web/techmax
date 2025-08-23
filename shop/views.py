from django.shortcuts import render, redirect
from django.contrib import messages
from . models import *
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def shop(request):
    artikel = Artikel.objects.all()
    ctx = {'artikel': artikel}
    return render(request, 'shop/shop.html', ctx)

def warenkorb(request):
    if request.user.is_authenticated:
        kunde = request.benutzer.kunde
        bestellung, created = Bestellung.objects.get_or_create(kunde=kunde, erledigt=False)
        artikel = bestellung.bestellteartikel_set.all()
    else:
        artikel = []
        bestellung = []
    ctx = {'artikel': artikel, 'bestellung': bestellung}
    return render(request, 'shop/warenkorb.html', ctx)

def kasse(request):
    if request.user.is_authenticated:
        kunde = request.user.kunde
        bestellung, created = Bestellung.objects.get_or_create(kunde=kunde, erledigt=False)
        artikel = bestellung.bestellteartikel_set.all()
    else:
        artikel = []
        bestellung = []

    ctx = {'artikel': artikel, 'bestellung': bestellung}
    return render(request, 'shop/kasse.html', ctx)

def artikelBackend(request):
    daten = json.loads(request.body)
    artikelID = daten['artikelID']
    action = daten['action']
    kunde = request.user.kunde
    artikel = Artikel.objects.get(id=artikelID)
    bestellung, created = Bestellung.objects.get_or_create(kunde=kunde, erledigt=False)
    bestellteArtikel, created = BestellteArtikel.objects.get_or_create(bestellung=bestellung, artikel=artikel)
    if action == 'bestellen':
        bestellteArtikel.menge += 1
        messages.success(request, 'Artikel zum Warenkorb hinzugefügt.')
    elif action == 'entfernen':
        bestellteArtikel.menge -= 1
        messages.warning(request, 'Artikel aus dem Warenkorb entfernt')
    bestellteArtikel.save()
    if bestellteArtikel.menge <= 0:
        bestellteArtikel.delete()
    return JsonResponse('Artikel hinzugefügt', safe=False)

def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shop')
        else:
            messages.error(request, 'Benutzername oder Passwort ist falsch.')
    return render(request, 'shop/login.html', {'page': page})

def logoutUser(request):
    logout(request)
    return redirect('shop')

def regUser(request):
    page = 'reg'
    form = UserCreationForm
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            benutzer = form.save(commit=False)
            benutzer.save()

            kunde = Kunde(name=request.POST['username'], benutzer=benutzer)
            kunde.save()
            bestellung = Bestellung(kunde=kunde)
            bestellung.save()

            login(request, benutzer)
            return redirect('shop')
        else:
            messages.error(request, 'Fehlerhafte Eingabe.')
    
    ctx = {'form': form, 'page': page}
    return render(request, 'shop/login.html', ctx)