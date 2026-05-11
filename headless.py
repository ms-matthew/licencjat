#uruchomienie bez gui - tabelka w terminalu, pokazuje ostatnie 10 krokow

from model import Model

m = Model(seed=42)
for _ in range(50):
    m.step()

print("\nStatystyki modelu (ostatnie 10 krokow):\n")
print(m.datacollector.get_model_vars_dataframe().tail(10))
