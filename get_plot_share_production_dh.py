import pandas as pd
import os
import matplotlib.pyplot as plt

THIS_PATH = os.path.dirname(os.path.abspath(__file__))

# Path to directory with datapackage to load
generation_dhc_path = os.path.join(
    THIS_PATH,
    "raw_data",
    "Langfristszenarien",
    "Erzeugung_Wärmenetze_Deutschland_Generation_Heatgrids_Germany.csv"
)

plot_results_path = os.path.join(
    THIS_PATH,
    "results",
    "Anteil_an_Erzeugung_Wärmenetze_Deutschland.png"
)

# Create  path for results (we use the datapackage_dir to store results)
results_path = os.path.join(
    os.path.expanduser(THIS_PATH), "results", "Langfrist", "plots"
)

generation_dhc = pd.read_csv(generation_dhc_path, sep=",")

# Compute the share of each technology in the respective year
generation_dhc["Anteil an Erzeugung in % / Share of generation in %"] = (
    generation_dhc["Erzeugung in TWh / Generation in TWh"] /
    generation_dhc.groupby("Jahr / Year")["Erzeugung in TWh / Generation in TWh"].transform("sum") * 100
)

# Prepare data for plotting
pivot = generation_dhc.pivot_table(
    index="Jahr / Year",
    columns="Technologie / Technology",
    values="Anteil an Erzeugung in % / Share of generation in %",
    aggfunc="sum"
)

# Plot the stacked bar chart
pivot.plot(kind="bar", stacked=True, figsize=(12,7), colormap="tab20b")

plt.title("Anteil der Technologien an der Wärmeerzeugung pro Jahr", fontsize=14)
plt.ylabel("Anteil an Erzeugung (%)")
plt.xlabel("Jahr")
plt.legend(title="Technologie", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.savefig(plot_results_path)
plt.show()
