import uuid
from typing import Dict, List

from gotta_process_em_all.poke_api import PokeApi
import pandas as pd


class PokePipeline:
    """
    1. The name, id, base_experience, weight, height and order of all Pokémon that appear in the any of the games red, blue, leafgreen or white.
    2. The name of the slot 1 (and if available 2) type of each of the Pokémon's types.
    3. The Body Mass Index of the Pokémon (hint: The formula for BMI is weight (kg) /height (m2))
    4. The first letter of names of the Pokémon should be capitalized.
    5. The url of the front_default sprite.
    6. Prepare the data in an appropriate data format. Consider if it should be multiple or a single file.
    """

    def __init__(self):
        self.api = PokeApi()
        self.file_path = "pokemons.csv"
        self.basic_props = ("name", "id", "base_experience", "weight", "height", "order")

    def catch_em_all(self):
        pokemons = self.fetch_all_from_api()
        pokemons = self.clean_all_pokemons(pokemons)
        self.dump_to_file(pokemons)
        return pokemons

    def clean_all_pokemons(self, pokemons: List[dict]):
        return [self.clean_pokemon(pokemon) for pokemon in pokemons]

    def fetch_all_from_api(self, max_pokemon_id=152) -> List[dict]:
        return [self.api.get_pokemon(i) for i in range(1, max_pokemon_id)]

    def dump_to_file(self, pokemons: List[Dict]):
        df = pd.DataFrame(pokemons).set_index("id")
        df.to_csv(self.file_path)

    def clean_pokemon(self, pokemon: Dict):
        new_pokemon = {}
        new_pokemon.update(self.get_basic_properties(pokemon))
        new_pokemon["name"] = str(new_pokemon["name"]).capitalize()
        new_pokemon["bmi"] = self.calculate_bmi(new_pokemon)
        new_pokemon["type"] = self.get_pokemon_type(pokemon)
        new_pokemon["sprite"] = pokemon["sprites"]["front_default"]
        return new_pokemon

    def get_pokemon_type(self, pokemon):
        # Here we assume that they are orderd by slot number. Currently we are not limiting it to 2 slots only.
        return "/".join([element_type["type"]["name"] for element_type in pokemon["types"]])

    def calculate_bmi(self, new_pokemon: Dict):
        pokemon_height = new_pokemon["height"] * 0.3048  # Conversion from feet to meter
        return float(new_pokemon["weight"]) / float(pokemon_height ** 2)

    def get_basic_properties(self, pokemon) -> Dict:
        return {property_name: pokemon[property_name] for property_name in self.basic_props}

    def gdpr_comply_pokemon(self, pokemon: Dict):
        gdpr_string = str(pokemon["id"]) + str(pokemon["name"])
        pokemon["id"] = hash(gdpr_string)
        del pokemon["name"]
        return pokemon

