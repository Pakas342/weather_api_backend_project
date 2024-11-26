from fastapi.exceptions import HTTPException
from fastapi import FastAPI

from services import WeatherReport

weather = WeatherReport()

app = FastAPI()


@app.get('/{city}')
def get_city_data(city: str, initial_date: str | None):
    try:
        response = weather.get_weather(location=city, initial_date=initial_date)
    except ValueError as date_error:
        raise HTTPException(
            status_code=400,
            detail=f'The given initial date is not valid dd/mm/yyyy format: {initial_date}'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error while requesting data: {e}')
    return response
