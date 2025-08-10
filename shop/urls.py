from django.urls import path
from .import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('warenkorb/', views.shop, name='warenkorb'),
    path('kasse/', views.shop, name='kasse'),
]