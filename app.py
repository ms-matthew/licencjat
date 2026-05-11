# wizualizacja modelu - siatka i wykresy w przegladarce

from mesa.visualization import (
    SolaraViz,
    make_space_component,
    make_plot_component,
)

from model import Agent, Model, Zasob


def jak_narysowac(agent):
    # definiuje rysowanie agenta
    if isinstance(agent, Zasob):
        return {"color": "gold", "marker": "s", "size": 25}

    # kolor agenta zmienia się w zależności od energii (czerwony - mało, zielony - dużo)
    poziom = min(max(agent.energia / 15.0, 0), 1)
    r = int(255 * (1 - poziom))
    g = int(255 * poziom)
    return {
        "color": f"#{r:02x}{g:02x}40",
        "marker": "o",
        "size": 60 + 4 * max(agent.energia, 0),
    }


parametry = {
    "n_agentow": {
        "type": "SliderInt", "value": 10, "label": "Liczba agentow",
        "min": 2, "max": 30, "step": 1,
    },
    "n_zasobow": {
        "type": "SliderInt", "value": 15, "label": "Liczba zasobow",
        "min": 0, "max": 50, "step": 1,
    },
    "seed": {
        "type": "SliderInt", "value": 42, "label": "Ziarno losowe",
        "min": 0, "max": 999, "step": 1,
    },
    "width": 10,
    "height": 10,
}

page = SolaraViz(
    Model(),
    components=[
        make_space_component(jak_narysowac),
        make_plot_component(["Zywi"]),
        make_plot_component(["Sr_energia"]),
        make_plot_component(["Zjedzone_lacznie"]),
    ],
    model_params=parametry,
    name="Model wieloagentowy - walka o zasoby",
)
