import pandas as pd
import os
import numpy as np

THIS_PATH = os.path.dirname(os.path.abspath(__file__))

# Input directory
try_path = os.path.join(
    THIS_PATH,
    "raw_data",
    "Testreferenzjahre"
)

# Output directory
output_path = os.path.join(
    THIS_PATH,
    "results",
    "Testreferenzjahre"
)

os.makedirs(output_path, exist_ok=True)

# Stefan-Boltzmann constant [W/m²K⁴]
SIGMA = 5.67e-8


def calculate_longwave_radiation(df):
    """
    Berechnet die abwärtsgerichtete langwellige Strahlung (Infrarotstrahlung)
    """

    # --- Temperatur in Kelvin ---
    # Umrechnung: T[K] = T[°C] + 273.15
    T = df["air_temperature_mean"] + 273.15

    # --- Taupunkttemperatur ---
    Td = df["dew_point"]

    # --- Dampfdruck e (Magnus-Formel) ---
    # e = 6.11 * exp((17.27 * Td) / (Td + 237.3))
    e = 6.11 * np.exp((17.27 * Td) / (Td + 237.3))

    # --- Atmosphärischer Emissionsgrad (Brutsaert, 1975) ---
    # ε_clear = 1.24 * (e / T)^(1/7)
    epsilon_clear = 1.24 * (e / T) ** (1/7)

    # --- Bewölkung normieren ---
    cloud = df["cloud_cover"].copy()
    if cloud.max() == 8:
        cloud = cloud / 8
    else:
        raise ValueError("Cloud is not in expected range!")

    # --- Wolkenkorrektur ---
    # ε = ε_clear * (1 + 0.22 * n²)
    epsilon = epsilon_clear * (1 + 0.22 * cloud**2)

    # Constrain epsilon to maximum 1 because it can not be higher
    epsilon = np.clip(epsilon, 0, 1)

    # --- Stefan-Boltzmann-Gesetz ---
    # L↓ = ε * σ * T⁴
    L_down = epsilon * SIGMA * T**4

    return L_down


# --- Verarbeitung aller Dateien ---
for file in os.listdir(try_path):
    if file.endswith(".txt"):
        file_path = os.path.join(try_path, file)

        print(f"Processing: {file}")

        # Datei laden (Trennzeichen ggf. anpassen!)
        df = pd.read_csv(file_path, sep=";")

        # Berechnung durchführen
        df["radiation_longwave_downwelling"] = calculate_longwave_radiation(df)

        # Output-Dateiname
        output_file = file.replace(".txt", ".csv")
        output_file_path = os.path.join(output_path, output_file)

        # Speichern
        df.to_csv(output_file_path, index=False)

print("Fertig! Alle Dateien wurden verarbeitet.")
