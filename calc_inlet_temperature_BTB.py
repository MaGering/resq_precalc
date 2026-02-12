import pandas as pd
import os

THIS_PATH = os.path.dirname(os.path.abspath(__file__))

# Path to directory with raw data
t_btb_path = os.path.join(
    THIS_PATH,
    "raw_data",
    "BTB_temperatures",
    "BTB_temperatures_2025.csv"
)

t_btb = pd.read_csv(t_btb_path, sep=";")

t_vl_mean = t_btb["TUC_VZ_WISTA_DurFlTemp_VL (°C)"].mean()
t_rl_mean = t_btb["TUC_VZ_WISTA_DurFlTemp_RL (°C)"].mean()

print(f"Mittlere Vorlauftemperatur: {round(t_vl_mean, 0)} °C\n"
      f"Mittlere Rücklauftemperatur: {round(t_rl_mean, 0)} °C")