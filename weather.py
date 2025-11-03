from dotenv import load_dotenv
from pprint import pprint
import requests
import os

load_dotenv()

def get_current_weather(city='Pune City', country='IN'):
    request_url = f"http://api.openweathermap.org/data/2.5/weather?appid={os.getenv('API_KEY')}&q={city},{country}&units=metric"

    weather_data = requests.get(request_url).json()
    return weather_data

if __name__ == '__main__':
    print('\nCurrent Weather Data\n')
    
    city = input('Enter City Name (default: Pune City): ') or 'Pune City'
    country = input('Enter Country Code (default: IN): ') or 'IN'

    weather_data = get_current_weather(city, country)
    print("/n")
    pprint(weather_data)

