import random
import mesa


class Zasob(mesa.Agent):
    # zasob do zjedzenia (+5 energii)

    def __init__(self, model):
        super().__init__(model)

    def step(self):
        pass


class Agent(mesa.Agent):
    # agnet, ktory chodzi po gridzie

    def __init__(self, model):
        super().__init__(model)

        # energia ( <= 0 agent umiera)
        self.energia = 10

        # counter zjedzonych zasobów 
        self.zjedzone = 0

    def step(self):
        self.rusz_sie()
        self.energia -= 1
        self.zjedz_zasob()

        if self.energia <= 0:
            self.model.grid.remove_agent(self)
            self.remove()

    def rusz_sie(self):
        #idzie w strone najblizszego zasobu, jesli go nie widzi to chodzi losowo

        # ilosc pól widzianych przez agenta
        WZROK = 4

        # wszystkie pola ktore widzi
        widoczne = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False, radius=WZROK
        )

        # znajdz najblizszy zasob
        cel = None
        najmniejsza_odleglosc = 999
        for pole in widoczne:
            for obj in self.model.grid.get_cell_list_contents([pole]):
                if isinstance(obj, Zasob):
                    d = max(
                        abs(pole[0] - self.pos[0]),
                        abs(pole[1] - self.pos[1]),
                    )
                    if d < najmniejsza_odleglosc:
                        najmniejsza_odleglosc = d
                        cel = pole

        # sasiednie pola do ruchu (8 kierunkow)
        sasiedzi = list(self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        ))

        if cel is not None:
            # wybiera pole ktore jest najblizej celu
            nowa_pozycja = min(sasiedzi, key=lambda p: max(
                abs(p[0] - cel[0]), abs(p[1] - cel[1])
            ))
        else:
            # nie widzi zadnego zasobu, idzie losowo
            nowa_pozycja = random.choice(sasiedzi)

        self.model.grid.move_agent(self, nowa_pozycja)

    def zjedz_zasob(self):
        # jezeli na danym polu jest zasob to go zjada 
        for obj in self.model.grid.get_cell_list_contents([self.pos]):
            if isinstance(obj, Zasob):
                self.energia += 5
                self.zjedzone += 1
                self.model.grid.remove_agent(obj)
                obj.remove()
                return


class Model(mesa.Model):
    # grid 10x10, ogolnie pole "gry"

    def __init__(self, n_agentow=10, n_zasobow=15, seed=42, width=10, height=10):
        super().__init__(seed=seed)
        random.seed(seed)

        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.szerokosc = width
        self.wysokosc = height
        self.cel_zasobow = n_zasobow

        # tworzymy agnetow i umieszczamy ich na losowych polach
        for _ in range(n_agentow):
            a = Agent(self)
            x = random.randrange(width)
            y = random.randrange(height)
            self.grid.place_agent(a, (x, y))

        # tworzymy zasoby i umieszczamy je na losowych polach
        for _ in range(n_zasobow):
            self._dodaj_zasob()

        # statystyki co step
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Zywi": lambda m: sum(1 for a in m.agents if isinstance(a, Agent)),
                "Sr_energia": lambda m: _srednia_energia(m),
                "Zjedzone_lacznie": lambda m: sum(
                    a.zjedzone for a in m.agents if isinstance(a, Agent)
                ),
            }
        )
        self.datacollector.collect(self)

    def _dodaj_zasob(self):
        z = Zasob(self)
        x = random.randrange(self.szerokosc)
        y = random.randrange(self.wysokosc)
        self.grid.place_agent(z, (x, y))

    def step(self):
        # kazdy agent wykonuje swoj krok, kolejność jest losowa
        agenci = [a for a in self.agents if isinstance(a, Agent)]
        random.shuffle(agenci)
        for a in agenci:
            a.step()

        # dodawanie nowego zasobu (30% szans jesli jest ich mniej niz cel zasobow)
        zasoby = sum(1 for a in self.agents if isinstance(a, Zasob))
        if zasoby < self.cel_zasobow and random.random() < 0.3:
            self._dodaj_zasob()

        self.datacollector.collect(self)


def _srednia_energia(model):
    agenci = [a for a in model.agents if isinstance(a, Agent)]
    if not agenci:
        return 0
    return sum(a.energia for a in agenci) / len(agenci)
