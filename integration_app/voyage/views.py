from django.shortcuts import render
from django.http import HttpResponse

# Importation des modèles
from .models import Airport

from .api.openMeteo import twoWeakWeatherForecast, calculGeneralWeather

def acceuil(request):
    countryChoosen = "France"
    best_weather = 1000
    weather_city = 0

    country = Airport.objects.filter(country=countryChoosen).values_list('city', flat=True)
    
    #for i in range(0, len(country)) :
        #df = twoWeakWeatherForecast(country[i].latitude, country[i].longitude)
        #weather_city = calculGeneralWeather(df)

        #if(weather_city < best_weather) :
            #best_weather = weather_city
            #best_city = country[i].

        
    print(country)

    return render(request, "pageAcceuil.html")
