import os
import pandas as pd

# Scenario name
scenario_name = "try_extr1_rcp85.p3"

# Define your paths
path_weatherdata = "/home/marie/Repositories/oemof-B3/raw/weatherdata"
wista_weatherdata = f"/home/marie/Downloads/{scenario_name}.txt"

# Read the WISTA TXT file
df_wista = pd.read_csv(wista_weatherdata, delimiter=';', engine='python')

# Read and update all CSVs
for filename in os.listdir(path_weatherdata):
    if filename.endswith('.csv'):
        file_path = os.path.join(path_weatherdata, filename)
        df = pd.read_csv(file_path)

        # Ensure both have same number of rows before overwriting
        if len(df) != len(df_wista):
            print(f"Skipping {filename}: row count mismatch ({len(df)} vs {len(df_wista)})")
            continue

        # Overwrite the specified columns
        try:
            df['ghi'] = df_wista['radiation_downwelling']
            df['dni'] = df_wista['radiation_direct']
            df['dhi'] = df_wista['radiation_diffuse']
            df['temp_air'] = df_wista['air_temperature_mean']
            df['wind_speed'] = df_wista['wind_speed']

            # Save back to the same file (overwrite)
            df.to_csv(file_path, index=False)
            print(f"Updated and saved: {filename}")
        except KeyError as e:
            print(f"Skipping {filename}: missing column {e}")