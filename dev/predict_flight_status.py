import pandas as pd
from datapreparation import *
import os

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

COLTYPES = {"ORIGIN_AIRPORT": object, "DESTINATION_AIRPORT": object}
CAT_FEATURES = ['AIRLINE', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT']
AIRPORTS = ['ORIGIN_AIRPORT', 'DESTINATION_AIRPORT']
COORDINATES = ['LONGITUDE', 'LATITUDE']

flights = pd.read_csv("./data/dev/flights.csv", nrows=100, dtype=COLTYPES)
airports = pd.read_csv("./data/dev/airports.csv")
holidays = pd.read_csv("./data/dev/2015_Public_Holidays.csv")

# Merge data files
flights = merge_two_airports(flights, airports, ["ORIGIN", "DESTINATION"])
flights = flights.merge(holidays, how="left", on=["MONTH", "DAY"])

# Define target
flights['TARGET'] = define_target(flights, 'DEPARTURE_DELAY', 15)

# Create new features
# flags for holiday, weekend, international airport
# traffic estimate based on flight counts for date, month, airport, airline

flights = categorize_multiple(flights, CAT_FEATURES)
flights['HOLIDAY_FLAG'] = flights['HOLIDAY'].notnull()*1
flights['WEEKEND'] = (flights['DAY_OF_WEEK'].isin([6, 7]))*1
flights['DATE'] = pd.to_datetime(
    [f'{y}-{m}-{d}' for y, m, d in zip(flights.YEAR, flights.MONTH, flights.DAY)])

for col in ['DATE', 'MONTH', 'AIRLINE']:
    aggregate = flights[col].value_counts()
    flights = join_aggregates(flights, col, aggregate, col+"_TRAFFIC")

airport_size = flights[AIRPORTS[0]].value_counts(
) + flights[AIRPORTS[1]].value_counts()

for airport in AIRPORTS:
    airport_intl = airport+"_INTL"
    flights[airport_intl] = flights[airport].apply(is_international)
    flights = join_aggregates(
        flights, airport, airport_size, airport+"_TRAFFIC")

for coordinate in COORDINATES:
    flights[coordinate+"_DIF"] = flights[coordinate +
                                         '_ORIGIN'] - flights[coordinate+'_DESTINATION']

# print(flights.columns)
print(flights.shape)
