import json

import pytest

from poke_pipeline import PokePipeline


class TestPokePipeline:
    @pytest.mark.integration
    def test_fetch_all_from_api(self, file_regression):
        pipeline = PokePipeline()
        all_pokemons = pipeline.fetch_all_from_api(max_pokemon_id=9)
        file_regression.check(json.dumps(all_pokemons), extension=".json")

    def test_clean_bulba(self, data_regression):
        bulba = json.load(open("test/test_data/bulbasaur.json"))
        pipeline = PokePipeline()
        selected_bulba = pipeline.clean_pokemon(bulba)
        data_regression.check(selected_bulba)

    def test_save_to_file(self, file_regression):
        bulba = json.load(open("test/test_data/bulbasaur.json"))
        pipeline = PokePipeline()
        pokemons = [pipeline.clean_pokemon(bulba)]
        pipeline.dump_to_file(pokemons)
        file_regression.check(open(pipeline.file_path).read(), extension=".csv")

    def test_catch_em_all(self, file_regression):
        pipeline = PokePipeline()
        pipeline.catch_em_all()
        file_regression.check(open(pipeline.file_path).read(), extension=".csv")






