import pandas as pd
from processing import merge_two_airports

COLTYPES = {"ORIGIN_AIRPORT": object, "DESTINATION_AIRPORT": object}

flights = pd.read_csv("./data/raw/flights.csv", nrows=100, dtype=COLTYPES)
airports = pd.read_csv("./data/raw/airports.csv")
holidays = pd.read_csv("./data/raw/2015_Public_Holidays.csv")

"""Merge files to append more features
TODO: write pytest to check if any airport can't be matched
"""
flights = merge_two_airports(flights, airports, ["ORIGIN", "DESTINATION"])
flights = flights.merge(holidays, how="left", on=["MONTH", "DAY"])
print(flights.columns)
print(len(flights))
