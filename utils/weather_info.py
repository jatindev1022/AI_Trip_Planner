import requests
class WeatherForecastTool:
    def __init__(self, api_key: str):
        self.api_key = api_key
        # UPDATE 1: New Base URL
        self.base_url = "https://api.weatherapi.com/v1"

    def get_current_weather(self, place: str):
        """Get current weather of a place"""
        try:
            # UPDATE 2: Change endpoint to /current.json
            url = f"{self.base_url}/current.json"
            params = {
                "q": place,
                "key": self.api_key, # UPDATE 3: Use "key" instead of "appid"
            }
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            raise e
    
    def get_forecast_weather(self, place: str):
        """Get weather forecast of a place"""
        try:
            # UPDATE 4: Change endpoint to /forecast.json
            url = f"{self.base_url}/forecast.json"
            params = {
                "q": place,
                "key": self.api_key, # UPDATE 5: Use "key"
                "days": 3,           # WeatherAPI uses 'days' instead of 'cnt'
                "aqi": "no"
            }
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            raise e