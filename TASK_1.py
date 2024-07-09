import requests
import pandas as pd

class RestCountriesAPI:
    def __init__(self):
        self.api_url = "https://restcountries.com/v3.1/all"

    def fetch_data(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_country_data(self):
        data = self.fetch_data()
        countries = []
        for country in data:
            name = country.get('name', {}).get('common', 'N/A')
            capital = country.get('capital', ['N/A'])[0]
            flag = country.get('flags', {}).get('png', 'N/A')
            countries.append({'Name': name, 'Capital': capital, 'Flag': flag})

        return countries

    def display_data(self):
        country_data = self.get_country_data()
        df = pd.DataFrame(country_data)
        print(df)

api = RestCountriesAPI()
api.display_data()