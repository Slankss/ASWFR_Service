import requests


def get_weather(api_key, city):
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }

    try:
        response = requests.get(url=url, params=params)
        response.raise_for_status()  # Check for HTTP errors
        weather_data = response.json()

        print(f"City: {weather_data['name']}")
        print(f"Temperature: {weather_data['main']['temp']} °C")
        print(f"Weather: {weather_data['weather'][0]['description']}")

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")


# Replace 'your_api_key' with your actual OpenWeatherMap API key
api_key = 'your_api_key'
city = 'London'
get_weather(api_key, city)
