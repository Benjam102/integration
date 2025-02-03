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
        if not results:
            return []
        item = results[0]
        extracted_data = {'skyId': item['skyId'], 'entityId': item['entityId']}
        
        return extracted_data
    else:
        return []
    

def get_flights(originSkyId, destinationSkyId, originEntityId, destinationEntityId, date, returnDate):
    # Paramètres de l'API
    url = "https://sky-scrapper.p.rapidapi.com/api/v2/flights/searchFlights"
    
    headers = {
	"x-rapidapi-key": "ca1f4b4b7cmsh445b6ec5a319652p1cf379jsnc9a580c6a33e",
	"x-rapidapi-host": "sky-scrapper.p.rapidapi.com"
}
    querystring = {
        "originSkyId": originSkyId,
        "destinationSkyId": destinationSkyId,
        "originEntityId": originEntityId,
        "destinationEntityId": destinationEntityId,
        "date": date,
        "returnDate": returnDate or "",
        "cabinClass": "economy",
        "adults": "1",
        "childrens": "0",
        "sortBy": "best",
        "limit": "5",
        "currency": "USD",
        "market": "en-US",
        "countryCode": "US"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    response.raise_for_status()
    data = response.json()
    
    flights = []
    if data['status'] and 'data' in data:
        for itinerary in data['data']['itineraries']:
            flights.append({
                "price": itinerary['price']['formatted'],
                "legs": [
                    {
                        "departure": leg['departure'],
                        "arrival": leg['arrival'],
                        "origin": leg['origin']['name'],
                        "destination": leg['destination']['name'],
                        "duration": leg['durationInMinutes']
                    } for leg in itinerary['legs']
                ]
            })
    return flights

flights = []
if __name__ == "__main__":
    origin_data = get_city_id("Toulouse")
    destination_data = get_city_id("Paris")
    print(origin_data, destination_data)
    
    if origin_data and destination_data:
        flights = get_flights(
        origin_data['skyId'], destination_data['skyId'],
        origin_data['entityId'], destination_data['entityId'],
        "2025-02-15", "2025-02-16"
        )
        print(flights)
