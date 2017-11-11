import requests


class WeatherApi(object):
    """
    Работа с API wunderground.com
    """
    connection_flag = None

    def __init__(self):
        self.key = ''  # API key wunderground.com
        self.api_url = 'http://api.wunderground.com/api/' + self.key + \
                       '/forecast/q/pws:IMOSKVA645.json'

    def check_weather(self):
        """
        Обрабатывает json файл
        :return: день, температуру, параметры ветра, вероятность осадков
        """
        try:
            req = requests.get(self.api_url)
            forecast = req.json()
            WeatherApi.connection_error_flag = False

            date_day_value = forecast['forecast']['simpleforecast']['forecastday'][0]['date']['day']
            date_month_value = forecast['forecast']['simpleforecast']['forecastday'][0]['date']['month']
            date_year_value = forecast['forecast']['simpleforecast']['forecastday'][0]['date']['year']
            weekday_value = forecast['forecast']['simpleforecast']['forecastday'][0]['date']['weekday']
            temp_low_value = forecast['forecast']['simpleforecast']['forecastday'][0]['low']['celsius']
            temp_high_value = forecast['forecast']['simpleforecast']['forecastday'][0]['high']['celsius']
            wind_low_value = forecast['forecast']['simpleforecast']['forecastday'][0]['avewind']['kph']
            wind_high_value = forecast['forecast']['simpleforecast']['forecastday'][0]['maxwind']['kph']
            wind_dir_value = forecast['forecast']['simpleforecast']['forecastday'][0]['avewind']['dir']
            pop_value = forecast['forecast']['simpleforecast']['forecastday'][0]['pop']

            temp = str(temp_low_value) + " - " + str(temp_high_value) + " °C"
            wind = (str(wind_low_value) + " - " + str(wind_high_value) + " km/h" +
                    " (" + wind_dir_value + ")")
            pop = str(pop_value) + " %"

            return (str(date_day_value), str(date_month_value), str(date_year_value),
                    weekday_value, temp, wind, pop, pop_value)

        except requests.ConnectionError:
            WeatherApi.connection_error_flag = True
            return "-", "-", "-", "No connection", "-", "-", "-", "-"


if __name__ == "__main__":
    print("Это модуль погодного api")
