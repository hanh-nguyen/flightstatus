import pandas as pd
from processing import merge_two_airports, categorize_multiple

COLTYPES = {"ORIGIN_AIRPORT": object, "DESTINATION_AIRPORT": object}
CAT_FEATURES = ['AIRLINE', 'DESTINATION_AIRPORT', 'ORIGIN_AIRPORT']

flights = pd.read_csv("./data/raw/flights.csv", nrows=100, dtype=COLTYPES)
airports = pd.read_csv("./data/raw/airports.csv")
holidays = pd.read_csv("./data/raw/2015_Public_Holidays.csv")

"""Merge data files
TODO: 
write pytest to check if any airport can't be matched (missing in city, state, ...)
check if the # columns & rows are expected
"""
flights = merge_two_airports(flights, airports, ["ORIGIN", "DESTINATION"])
flights = flights.merge(holidays, how="left", on=["MONTH", "DAY"])

"""Create new features
"""
flights = categorize_multiple(flights, CAT_FEATURES)
print(flights.columns)
print(flights.shape)
