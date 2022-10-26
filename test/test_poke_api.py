import pytest

from gotta_process_em_all.poke_api import PokeApi


class TestPokeApi:
    @pytest.mark.parametrize("pokemon_id, name", (
            (25, "pikachu"),
            (10, "caterpie"),
    ))
    def test_get_pokemons(self, pokemon_id, name):
        poke_api = PokeApi()
        picachu = poke_api.get_pokemon(pokemon_id)
        assert picachu["name"] == name

    def test_get_pikachu(self, data_regression):
        poke_api = PokeApi()
        picachu = poke_api.get_pokemon(25)
        data_regression.check(picachu)