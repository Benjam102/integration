from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

# Importation des modèles
from .models import Airport

from .api.openMeteo import twoWeakWeatherForecast, calculGeneralWeather
from .api.sky_scraper import get_city_id, get_flights

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
    
    first_city = list(L_cities_score[0].keys())[0] if L_cities_score else None
    second_city = list(L_cities_score[1].keys())[0] if L_cities_score else None
    third_city = list(L_cities_score[2].keys())[0] if L_cities_score else None
    flights = []
    
    if request.method == "POST":
        origin = request.POST.get("origin")
        #destination = request.POST.get("destination")
        date = request.POST.get("date")
        return_date = request.POST.get("returnDate")
    else:
        origin = "Paris"
        date = "2025-02-15"
        return_date = "2025-02-16"
    
    if first_city:
        origin_data = get_city_id("Paris")
        destination_data = get_city_id(first_city)
        if len(destination_data)==0:
            destination_data = get_city_id(second_city)
        if len(destination_data)==0:
            destination_data = get_city_id(third_city)
        
        print(origin_data)
        print(destination_data)
            
        if origin_data and destination_data:
            flights = get_flights(
                origin_data['skyId'], destination_data['skyId'],
                origin_data['entityId'], destination_data['entityId'],
                date="2025-02-15",  # Exemple de date à récupérer via la requête,
                returnDate="2025-02-16"  # Exemple de date à récupérer via la requête
            )
    print(flights)
    
    return render(request, "pageAcceuil.html", {"flights": flights})
