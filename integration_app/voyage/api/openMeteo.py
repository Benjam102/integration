import openmeteo_requests
import requests_cache
import pandas as pd
from pandas import DataFrame
from retry_requests import retry
from typing import List, Dict, Tuple, Optional


def twoWeakWeatherForecast(latitude: float, longitude: float) -> DataFrame :
    """
    function that provides a code to give the general weather for each day of the two weeks

    Parameters:
        latitude: Latitute of the city
        Longitude : Longitude of the city

    Returns:
        daily_dataframe: DataFrame with each day with his code  
    """

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    
    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
    	"latitude": latitude,
    	"longitude": longitude,
    	"daily": "weather_code",
    	"forecast_days": 14
    }
    responses = openmeteo.weather_api(url, params=params)
    
    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    
    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
    	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
    	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
    	freq = pd.Timedelta(seconds = daily.Interval()),
    	inclusive = "left"
    )}
    
    daily_data["weather_code"] = daily_weather_code
    
    daily_dataframe = pd.DataFrame(data = daily_data)
    
    return daily_dataframe


def calculGeneralWeather(df_city: DataFrame) -> int :
    return df_city['weather_code'].sum()