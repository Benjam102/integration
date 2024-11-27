from django.urls import path, include
from . import views

# On relie les URLs aux fonctions de views.py #
urlpatterns = [
    path('', views.acceuil, name='acceuil'),
]
