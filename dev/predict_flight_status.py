import pandas as pd
from processing import *

COLTYPES = {"ORIGIN_AIRPORT": object, "DESTINATION_AIRPORT": object}
CAT_FEATURES = ['AIRLINE', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT']
AIRPORTS = ['ORIGIN_AIRPORT', 'DESTINATION_AIRPORT']
COORDINATES = ['LONGITUDE', 'LATITUDE']

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

"""Create categorical features
"""
flights = categorize_multiple(flights, CAT_FEATURES)

"""Create airport-related features:
- international airport flag
- airport size estimate based on flight counts
"""
airport_size = flights[AIRPORTS[0]].value_counts(
) + flights[AIRPORTS[1]].value_counts()

for airport in AIRPORTS:
    airport_intl = airport+"_INTL"
    flights[airport_intl] = flights[airport].apply(is_internationl)
    flights = join_aggregates(flights, airport, airport_size, airport+"_SIZE")

"""Create airline-related features:
- airline size estimate based on flight counts
"""
airline_size = flights['AIRLINE'].value_counts()
flights = join_aggregates(flights, 'AIRLINE', airline_size, "AIRLINE_SIZE")

"""Create flight-related features:
- flight distance
"""
for coordinate in COORDINATES:
    coordinate_dif =
    flights[coordinate+"_DIF"] = flights[coordinate +
                                         '_ORIGIN'] - flights[coordinate+'_DESTINATION']


print(flights.columns)
print(flights.shape)
