import pandas as pd


def merge_one_airport(flights: pd.DataFrame, airports: pd.DataFrame, location: str):
    DROPCOLS = ["IATA_CODE", "COUNTRY"]
    OLDCOLS = ["AIRPORT", "CITY", "STATE", "LATITUDE", "LONGITUDE"]
    NEWCOLS = [old + "_" + location for old in OLDCOLS]
    flights = flights.merge(
        airports, how="left", left_on=location + "_AIRPORT", right_on="IATA_CODE"
    )
    flights.drop(DROPCOLS, axis=1, inplace=True)
    flights.rename(columns=dict(zip(OLDCOLS, NEWCOLS)), inplace=True)
    return flights


def merge_two_airports(flights, airports, locations: list):
    for location in locations:
        flights = merge_one_airport(flights, airports, location)
    return flights


def categorize(data: pd.DataFrame, feature: str):
    data[feature+"_CAT"] = data[feature].astype("category").cat.codes + 1
    return data


def categorize_multiple(data, features: list):
    for feature in features:
        data = categorize(data, feature)
    return data
