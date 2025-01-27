from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

# Importation des modèles
from .models import Airport

from .api.openMeteo import twoWeakWeatherForecast, calculGeneralWeather

def acceuil(request):
    # Normalement disponible via la requête
    countryChoosen = "France"

    # Récupérer les villes du pays sélectionné
    cities_country_chosen = Airport.objects.filter(country=countryChoosen)
    
    L_cities_score = []

    # Déterminer les trois villes avec le meilleur temps sur un horizon de deux semaines
    for c in cities_country_chosen:
        weather = twoWeakWeatherForecast(c.latitude, c.longitude)    # Météo sur deux semaines
        score_weather = calculGeneralWeather(weather)                # Temps général sur les deux semaines

        # Eviter d'avoir trois fois la même ville
        if not any(c.city in cle_valeur for cle_valeur in L_cities_score) :
            if (len(L_cities_score) < 3) :
                L_cities_score.append({c.city : score_weather})
                L_cities_score.sort(key=lambda x : list(x.values())[0])
            else :
                for j in range(2, -1, -1) :
                    if (score_weather < list(L_cities_score[j].values())[0]) :
                        L_cities_score[j] = {c.city : score_weather}
                        L_cities_score.sort(key=lambda x : list(x.values())[0])
                        break                           

        
    print(L_cities_score)

    return render(request, "pageAcceuil.html")
