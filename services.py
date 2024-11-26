import datetime
import logging
import os
import requests

from dotenv import load_dotenv

load_dotenv()

WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')


class WeatherReport:
    def __init__(self):
        self.path = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'

    def get_weather(self, location: str, initial_date: str | None = None):
        if initial_date:
            try:
                start_date = datetime.datetime.strptime(initial_date, '%d/%m/%Y')
            except ValueError as date_error:
                raise date_error
        else:
            start_date = datetime.datetime.now()
        final_date = start_date + datetime.timedelta(days=7)
        path = self.path + f'{location}/{start_date.date()}/{final_date.date()}'
        logging.debug(f'path to call: {path}')
        path += f'?key={WEATHER_TOKEN}'
        request = requests.get(path)
        request.raise_for_status()
        try:
            response = [{
                'datetime': day_data['datetime'],
                'temp': day_data['temp'],
                'humidity': day_data['humidity'],
                'windspeed': day_data['windspeed'],
                'conditions': day_data['conditions']
            } for day_data in request.json()['days']]
        except KeyError as e:
            logging.error(f'Error parsing data {e}')
            raise
        return response


if __name__ == '__main__':
    weather = WeatherReport()
    weather.get_weather('Sydney', '8/8/2024')
