import requests
import json

class WeatherDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_data(self, url, capital , state, country, units):

        # Construct the query string to inject into url parameters
        query_string = f"{capital},{state},{country}"

        parameters = {
            'appid': self.api_key,
            'q': query_string, # Location query string (capital, state, country)
            'units': units # Units for temperature (e.g., imperial for Fahrenheit)
        }

        # Make an HTTP GET request to the weather API 
        response = requests.get(url,params=parameters)

        # Check if the response status code indicates an error (non-200 status code)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.status_code} {response.text}")
        
        return json.loads(response.content) # Return json data
    
    def get_current_temperature(self, url, capital, state, country, units):

        # Fetch weather data for the specified location
        data = self.fetch_data(url, capital , state, country, units)

        # Extract the current temperature from the fetched data
        current_temperature = data["main"]["temp"]

        return round(current_temperature)
    




