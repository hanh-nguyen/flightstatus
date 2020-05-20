from os.path import join
import pandas as pd

COLTYPES = {"ORIGIN_AIRPORT": object, "DESTINATION_AIRPORT": object}

flights = pd.read_csv("../data/raw/flights.csv", 100, dtype=COLTYPES)
airports = pd.read_csv("../data/raw/airports.csv")
holidays = pd.read_csv("../data/raw/2015_Public_Holidays.csv")

"""Merge files to append more features
"""
# TODO: write pytest to check if any airport can't be matched
c.merge_two_airports(flights, airports, ["ORIGIN", "DESTINATION"])
# add holiday days
flights.merge(holidays, how="left", on=["MONTH", "DAY"])
print(flights.get_columns())
print(len(flights.get_columns()))
