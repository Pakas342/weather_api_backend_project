import json

import datetime
import logging
import os

import requests

from dotenv import load_dotenv
import redis

load_dotenv()
r = redis.Redis(host='localhost', port=6379, db=0)

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
        cache_key = f'weather:{location}/{start_date.date()}'
        response = r.get(cache_key)
        if response:
            return json.loads(response)
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
        try:
            r.set(cache_key, json.dumps(response), ex=3800)
        except redis.RedisError as e:
            logging.error(f"Failed to cache: {e}")
        return response


if __name__ == '__main__':
    weather = WeatherReport()
    weather.get_weather('Sydney', '8/8/2024')
