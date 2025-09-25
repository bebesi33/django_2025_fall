import urllib.request
import json


try:
    city_encoded = "Budapest"
    api_key = "Másold be ide az API kulcsodat a honlapról"
    api_response = urllib.request.urlopen(
        f"https://api.openweathermap.org/data/2.5/weather?q={city_encoded}&appid={api_key}"
    ).read()
    weather_data = json.loads(api_response)
except urllib.error.HTTPError as e:
    if e.code == 404:
        error_message = f"The requested city '{city_encoded}' is not available."
    else:
        error_message = "An error occurred during the request."
