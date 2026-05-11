# Model wieloagentowy — walka o zasoby

Prosty model symulacyjny napisany w Pythonie z użyciem biblioteki [Mesa](https://mesa.readthedocs.io/).
Na planszy 10×10 poruszają się agenci, którzy szukają i zjadają zasoby, żeby nie stracić energii.
Agent traci 1 jednostkę energii na każdy krok, a po zjedzeniu zasobu odzyskuje 5. Gdy energia spadnie do zera — agent ginie.

## Zasady modelu

- **Agent** — porusza się po siatce (8 kierunków). Jeśli w zasięgu wzroku (4 pola) widzi zasób, idzie w jego stronę; jeśli nie widzi nic — porusza się losowo.
- **Zasob** — nieruchomy obiekt, który po zjedzeniu daje agentowi +5 energii.
- Co krok z 30% prawdopodobieństwem pojawia się nowy zasób, dopóki ich liczba jest mniejsza niż zadany limit.
- Zbierane statystyki: liczba żywych agentów, średnia energia, łączna liczba zjedzonych zasobów.

## Wymagania

- Python 3.10+
- Pakiety z pliku `requirements.txt` (mesa, solara, altair, matplotlib, pandas, numpy)

## Instalacja

W katalogu projektu:

```bash
py -m pip install -r requirements.txt
```

(zamiast `py` może być `python` lub `python3` — zależnie od systemu)

## Uruchomienie

### 1. Wersja z wizualizacją (przeglądarka)

```bash
py -m solara run run.py
```

Otworzy się strona w przeglądarce z siatką, agentami i wykresami. Po lewej stronie są suwaki do zmiany parametrów (liczba agentów, liczba zasobów, ziarno losowe).

### 2. Wersja bez GUI (terminal)

```bash
py headless.py
```

Uruchamia 50 kroków symulacji i wypisuje tabelkę ze statystykami z ostatnich 10 kroków.

## Pliki

| Plik | Opis |
|------|------|
| `model.py` | logika modelu — klasy `Agent`, `Zasob`, `Model` |
| `app.py` | konfiguracja wizualizacji (rysowanie agentów, suwaki, wykresy) |
| `run.py` | punkt wejścia dla wersji z wizualizacją |
| `headless.py` | uruchomienie symulacji w terminalu, bez interfejsu |
| `requirements.txt` | lista wymaganych pakietów |
