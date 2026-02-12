import os
import pandas as pd
import re

# Define your directory
this_path = os.path.dirname(os.path.abspath(__file__))
el_prices_path = os.path.join(this_path, "raw_data", "Strompreise")

# Dictionary to store yearly mean values
yearly_means = {}

# Loop through files in the directory
for filename in os.listdir(el_prices_path):
    if filename.endswith('.csv'):
        # Extract year from filename using regex
        match = re.search(r'(\d{4})', filename)
        if match:
            year = match.group(1)
            filepath = os.path.join(el_prices_path, filename)

            # Read CSV file
            try:
                df = pd.read_csv(filepath)

                # Flatten all numeric values for mean (assuming TS data is in columns)
                numeric_cols = df.select_dtypes(include='number')
                if not numeric_cols.empty:
                    mean_val = numeric_cols.stack().mean()
                    yearly_means[year] = mean_val
                else:
                    print(f"No numeric data found in {filename}")
            except Exception as e:
                print(f"Error reading {filename}: {e}")

# Print mean values per year
for year in sorted(yearly_means):
    print(f"{year}: Mean Value = {yearly_means[year]:.2f}")