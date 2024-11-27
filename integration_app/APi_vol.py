import requests

def get_city_id(city_name):

    url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchAirport"

    querystring = {"query":city_name,"locale":"en-US"}

    headers = {
        "x-rapidapi-key": "ca1f4b4b7cmsh445b6ec5a319652p1cf379jsnc9a580c6a33e",
        "x-rapidapi-host": "sky-scrapper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring).json()
    
    if response['status']:
        results = response['data']
        extracted_data = [{'skyId': item['skyId'], 'entityId': item['entityId']} for item in results]
        
        return extracted_data
    else:
        return []
    

def get_flights(originSkyId, destinationSkyId, originEntityId, destinationEntityId, date, returnDate):
    # Paramètres de l'API
    url = "https://api.exemple.com/v1/flights"
    
    headers = {
	"x-rapidapi-key": "ca1f4b4b7cmsh445b6ec5a319652p1cf379jsnc9a580c6a33e",
	"x-rapidapi-host": "sky-scrapper.p.rapidapi.com"
    }
    querystring = {"originSkyId":originSkyId,"destinationSkyId":destinationSkyId,
    "originEntityId":originEntityId,"destinationEntityId":destinationEntityId,
    "date":date,"returnDate":returnDate,"cabinClass":"economy",
    "adults":"1","childrens":"0","sortBy":"best","limit":"5","currency":"USD",
    "market":"en-US","countryCode":"US"}
    
    # Appel de l'API
    response = requests.get(url, headers=headers, params=querystring)
    response.raise_for_status()
    data = response.json()  # Convertir la réponse JSON
    
    # Transform the data for a better utilisability 
    flights = []
    if data.get('status'):
        itineraries = data['data']['itineraries']
        for itinerary in itineraries:
            price = itinerary['price']['formatted']
            legs = itinerary['legs']
            flights.append({
                "price": price,
                "legs": [
                    {
                        "departure": leg['departure'],
                        "arrival": leg['arrival'],
                        "origin": leg['origin']['name'],
                        "destination": leg['destination']['name'],
                        "duration": leg['durationInMinutes']
                    } for leg in legs
                ]
            })
    return flights