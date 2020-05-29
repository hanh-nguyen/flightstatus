import pandas as pd
from sklearn.feature_selection import VarianceThreshold


def merge_one_airport(flights: pd.DataFrame, airports: pd.DataFrame, location: str):
    DROPCOLS = ["IATA_CODE"]
    OLDCOLS = ["AIRPORT", "CITY", "STATE", "COUNTRY", "LATITUDE", "LONGITUDE"]
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


def is_international(col):
    return ('INTER' in col.upper())*1


def join_aggregates(data, col, aggregates, agg_name):
    return pd.merge(data, aggregates.to_frame(name=agg_name), how='left', left_on=col, right_index=True)


def define_target(data, target_col, threshold):
    return (data[target_col] > threshold | data[target_col].isnull())*1


def remove_constant_column(data):
    selector = VarianceThreshold()
    selector.fit(data)
    variance_sel = pd.DataFrame({'feature': data.drop(['target', 'experiancustomerid_orig'], axis=1).columns,
                                 'selected': selector.get_support()})
    cols = variance_sel[variance_sel['selected']]['feature'].tolist()
    len(cols)


def get_col_with_null(data):
    table_null = data.isnull().sum()
    return table_null[table_null > 0].index.tolist()
