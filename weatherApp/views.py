from django.shortcuts import render
import urllib.request
import json
import urllib.parse

def index(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        if not city:  # Check if city is empty
            data = {'error': 'Please enter a city name.'}
            return render(request, "main/index.html", data)

        try:
            city_encoded = urllib.parse.quote(city)  # Encode the city name
            url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city_encoded + '&units=metric&appid=764a04e307258f673879ab700fdba9f4'
            source = urllib.request.urlopen(url).read()
            list_of_data = json.loads(source)

            data = {
                "country_code": str(list_of_data['sys']['country']),
                "coordinate": str(list_of_data['coord']['lon']) + ', ' + str(list_of_data['coord']['lat']),
                "temp": str(list_of_data['main']['temp']) + '°C',
                "pressure": str(list_of_data['main']['pressure']) + ' Pa',
                "humidity": str(list_of_data['main']['humidity']) + '%',
                "main": str(list_of_data['weather'][0]['main']),
                "description": str(list_of_data['weather'][0]['description']),
                "icon": str(list_of_data['weather'][0]['icon']),
            }
            print(data)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                data = {'error': 'City not found. Please try a different name.'}
            else:
                data = {'error': 'An error occurred while fetching weather data.'}
        except Exception as e:
            data = {'error': 'An error occurred: ' + str(e)}

    else:
        data = {}  # Initialize empty data for GET requests

    return render(request, "main/index.html", data)
