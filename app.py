import pandas as pd

import panel as pn

pn.extension()
import hvplot.pandas  # noqa


class App:
    """To run: panel serve app.py"""

    def __init__(self):
        self.pokemons = pd.read_csv("pokemons.csv")
        self.selector = pn.widgets.Select(name='pokemon', options=list(self.pokemons["name"]))

        selected_pokemon = self.get_selected_pokemon(self.selector.value)
        self.details = pn.pane.HTML(self.get_pokemon_details(selected_pokemon))
        self.plot = self.create_bmi_plot()
        self.image = pn.pane.PNG(selected_pokemon["sprite"][0])
        self.selector.link(self.image, callbacks={"value": self.callback_on_change})

    def layout(self):
        return pn.Row(
            pn.Column(self.selector, self.details, self.image),
            pn.Column(self.plot),
        )

    def create_bmi_plot(self):
        return self.pokemons.hvplot.scatter(x="weight", y="height", color="type",
                                            hover_cols=["name", "weight", "height", "bmi", "type"])

    def get_selected_pokemon(self, name):
        return self.pokemons[self.pokemons["name"] == name].head(1)

    def get_pokemon_details(self, pokemon: pd.DataFrame):
        pokemon_columns = pokemon.loc[:, pokemon.columns != 'sprite']
        return pokemon_columns.to_html()

    def callback_on_change(self, target, event):
        pokemon_name = event.new
        pokemon = self.get_selected_pokemon(pokemon_name)
        self.image.object = pokemon["sprite"].values[0]
        self.details.object = self.get_pokemon_details(pokemon)


App().layout().servable()
