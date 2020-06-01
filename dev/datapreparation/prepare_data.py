import pandas as pd
from datapreparation import *
import os
from sklearn.feature_selection import VarianceThreshold
from pandas.api.types import is_string_dtype, is_numeric_dtype

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

COLTYPES = {"ORIGIN_AIRPORT": object, "DESTINATION_AIRPORT": object}
AIRPORTS = ['ORIGIN_AIRPORT', 'DESTINATION_AIRPORT']
AIRPORT_NAMES = ['AIRPORT_ORIGIN', 'AIRPORT_DESTINATION']
COORDINATES = ['LONGITUDE', 'LATITUDE']
UNAVAILABLE = ['ARRIVAL_TIME', 'ARRIVAL_DELAY', 'DIVERTED', 'CANCELLED', 'CANCELLATION_REASON',
               'AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY',
               'DEPARTURE_TIME', 'DEPARTURE_DELAY', 'TAXI_OUT', 'WHEELS_OFF',
               'ELAPSED_TIME', 'AIR_TIME', 'WHEELS_ON', 'TAXI_IN']
DUP_COLS = ['AIRPORT_ORIGIN', 'AIRPORT_DESTINATION']
EXTRA = ['DATE']
flights = pd.read_csv("./data/dev/flights.csv", dtype=COLTYPES)
# remove ineligible airport codes
for airport in AIRPORTS:
    flights = flights[flights[airport].str.isalpha()]

# remove 6 rows whose schedule time is missing
flights.dropna(subset=['SCHEDULED_TIME'], inplace=True)

airports = pd.read_csv("./data/dev/airports.csv")
airports.loc[airports.IATA_CODE == 'PBG', 'LATITUDE'] = 44.6521
airports.loc[airports.IATA_CODE == 'PBG', 'LONGITUDE'] = -73.4679
airports.loc[airports.IATA_CODE == 'ECP', 'LATITUDE'] = 30.3549
airports.loc[airports.IATA_CODE == 'ECP', 'LONGITUDE'] = -85.7995
airports.loc[airports.IATA_CODE == 'UST', 'LATITUDE'] = 29.9544
airports.loc[airports.IATA_CODE == 'UST', 'LONGITUDE'] = -81.3429

holidays = pd.read_csv("./data/dev/2015_Public_Holidays.csv")

# Merge data files
flights = merge_two_airports(flights, airports, ["ORIGIN", "DESTINATION"])
flights = flights.merge(holidays, how="left", on=["MONTH", "DAY"])

# Define target: flights departed 15 mins or more later than the scheduled departured
flights['TARGET'] = define_target(flights, 'DEPARTURE_DELAY', 15)

# Create new features
# flags for holiday, weekend, international airport
# traffic estimate based on flight counts for date, month, airport, airline


flights['HOLIDAY_FLAG'] = flights['HOLIDAY'].notnull()*1
flights['WEEKEND'] = (flights['DAY_OF_WEEK'].isin([6, 7]))*1
flights['DATE'] = pd.to_datetime(
    [f'{y}-{m}-{d}' for y, m, d in zip(flights.YEAR, flights.MONTH, flights.DAY)])

for col in ['DATE', 'MONTH', 'AIRLINE']:
    aggregate = flights[col].value_counts()
    flights = join_aggregates(flights, col, aggregate, col+"_TRAFFIC")

airport_size = flights[AIRPORTS[0]].value_counts(
).add(flights[AIRPORTS[1]].value_counts(), fill_value=0)

for airport in AIRPORTS:
    flights = join_aggregates(
        flights, airport, airport_size, airport+"_TRAFFIC")

for airport in AIRPORT_NAMES:
    airport_intl = airport+"_INTL"
    flights[airport_intl] = flights[airport].apply(is_international)

for coordinate in COORDINATES:
    flights[coordinate+"_DIF"] = flights[coordinate +
                                         '_ORIGIN'] - flights[coordinate+'_DESTINATION']

flights.drop(UNAVAILABLE + EXTRA + DUP_COLS, axis=1, inplace=True)

STR_VAR = [v for v in flights.columns if is_string_dtype(flights[v])]
flights = categorize_multiple(flights, STR_VAR)
flights.drop(STR_VAR, axis=1, inplace=True)

NULL_VAR = get_col_with_null(flights)
NUM_VAR_COMPLETE = [v for v in flights.columns if is_numeric_dtype(
    flights[v]) and v not in NULL_VAR]
selector = VarianceThreshold()
selector.fit(flights[NUM_VAR_COMPLETE])
NUM_VAR_REMOVED = [NUM_VAR_COMPLETE[i] for i in range(
    len(NUM_VAR_COMPLETE)) if selector.get_support()[i] == False]
flights.drop(NUM_VAR_REMOVED, axis=1, inplace=True)

flights.to_csv("./data/dev/flights_processed.csv", index=False)
