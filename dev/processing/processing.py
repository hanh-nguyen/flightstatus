import pandas as pd


def merge_one_airport(flights, airports, location: str):
    DROPCOLS = ["IATA_CODE", "COUNTRY"]
    OLDCOLS = ["AIRPORT", "CITY", "STATE", "LATITUDE", "LONGITUDE"]
    NEWCOLS = [old + "_" + location for old in OLDCOLS]
    flights.merge(
        airports, how="left", left_on=location + "_AIRPORT", right_on="IATA_CODE"
    )
    flights.drop_columns(DROPCOLS)
    flights.rename_columns(OLDCOLS, NEWCOLS)
    return flights


def merge_two_airports(flights, airports, locations: list):
    for location in locations:
        flights = merge_one_airport(flights, airports, location)

