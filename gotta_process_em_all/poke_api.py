from urllib.parse import urljoin

import requests


class PokeApi:
    api_url = "https://pokeapi.co/api/v2/"

    def __init__(self):
        pass

    def get_pokemon(self, pokemon_id):
        url = urljoin(self.api_url, f"pokemon/{pokemon_id}")
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
