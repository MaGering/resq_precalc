import pandas as pd
import os

THIS_PATH = os.path.dirname(os.path.abspath(__file__))

# Path to directory with raw data to load
abwaermepot_path = os.path.join(
    THIS_PATH,
    "raw_data",
    "Abwaermepotenzial_Adlershof_BfEE",
    "Abwaermepotenzial_Adlershof_BfEE.csv"
)

abwaermepot = pd.read_csv(abwaermepot_path, sep=",")

temperaturbereiche = abwaermepot["Temperaturbereich"].unique()
verfuegbarkeit = abwaermepot["Durchschnittliche tägl. Verfügbarkeit (in h)"].unique()

Test = 0