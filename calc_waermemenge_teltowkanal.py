import pandas as pd
import os
from CoolProp.CoolProp import PropsSI

THIS_PATH = os.path.dirname(os.path.abspath(__file__))

years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

# Path to directory with raw data
t_teltow_path = os.path.join(
    THIS_PATH,
    "raw_data",
    "Teltowkanal_and_Spree_Data",
    "5870100_wassertemperatur_tw_06_04_2016.csv"
)

v_teltow_path = os.path.join(
    THIS_PATH,
    "raw_data",
    "Teltowkanal_and_Spree_Data",
    "5870100_durchfluss_tw_01_03_2000.csv"
)

# Read raw data
t_teltow = pd.read_csv(t_teltow_path, sep=";")
v_teltow = pd.read_csv(v_teltow_path, sep=";")

# Tagesmittelwert-Spalten numerisch machen (Komma → Punkt)
for df in [t_teltow, v_teltow]:
    df["Tagesmittelwert"] = (
        df["Tagesmittelwert"]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

# mögliche Datums-Spaltennamen
DATE_COL = "Datum"   # ggf. anpassen

# Datum konvertieren (robust)
t_teltow[DATE_COL] = pd.to_datetime(
    t_teltow[DATE_COL],
    dayfirst=True,
    errors="coerce"
)

v_teltow[DATE_COL] = pd.to_datetime(
    v_teltow[DATE_COL],
    dayfirst=True,
    errors="coerce"
)

# ungültige Datumszeilen entfernen
t_teltow = t_teltow.dropna(subset=[DATE_COL])
v_teltow = v_teltow.dropna(subset=[DATE_COL])

# Konstante Temperaturdifferenz
DELTA_T = 3.0  # °C

results = []

for year in years:
    # Jahresfilter
    t_year = t_teltow[t_teltow["Datum"].dt.year == year]
    v_year = v_teltow[v_teltow["Datum"].dt.year == year]

    if t_year.empty or v_year.empty:
        continue

    # Mittelwerte
    T_mean = t_year["Tagesmittelwert"].mean()  # °C
    V_mean = v_year["Tagesmittelwert"].mean()  # m³/s

    # Temperatur in Kelvin
    T_K = T_mean + 273.15

    # Stoffwerte Wasser
    rho = PropsSI("D", "T", T_K, "P", 101325, "Water")  # kg/m³
    cp = PropsSI("C", "T", T_K, "P", 101325, "Water")  # J/(kg·K)

    # Nutzwärmeleistung (W)
    Q_nutz_W = rho * cp * V_mean * DELTA_T

    # Umrechnung in MW
    Q_nutz_MW = Q_nutz_W / 1e6

    results.append({
        "Jahr": year,
        "T_mean_°C": T_mean,
        "V_mean_m3s": V_mean,
        "rho_kgm3": rho,
        "cp_JkgK": cp,
        "Q_nutz_MW": Q_nutz_MW
    })

    # Ergebnisse als DataFrame
results_df = pd.DataFrame(results)

print(results_df)
print("")
print(f"Mittlere Nutzwärme: {round(results_df['Q_nutz_MW'].mean(), 0)}")