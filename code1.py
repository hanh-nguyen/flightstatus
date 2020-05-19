import pandas as pd


class DataProcessor:
    """Base processor to be used for all preparation.
    """

    def __init__(self, filepath: str, nrows=None, dtype=None):
        """How to handle error if file does not exist?
        How to take all arguments as method pd.read_csv?
        """
        self.filepath = filepath
        self.data = pd.read_csv(filepath, nrows=nrows, dtype=dtype)

    def get_data(self):
        return self.data

    def get_columns(self):
        return self.data.columns

    def rename_columns(self, old_cols: list, new_cols: list):
        self.data = self.data.rename(columns=dict(zip(old_cols, new_cols)))

    def drop_columns(self, colnames: list):
        self.data = self.data.drop(colnames, axis=1)

    def save_csv(self, filepath: str):
        """Saves processed data."""
        self.data.to_csv(filepath)

    def merge(self, newdata, *args, **kwargs):
        self.data = pd.merge(self.data, newdata.data, *args, **kwargs)


class FeatureSelector:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.columns = self.data.columns

    def get_columns(self):
        return self.columns

    def remove_columns(self, removecols: list):
        newcols = list(set(self.columns) - set(removecols))
        self.columns = newcols


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


if __name__ == "__main__":
    coltypes = {"ORIGIN_AIRPORT": object, "DESTINATION_AIRPORT": object}
    flights = DataProcessor("flights.csv", 100, dtype=coltypes)
    airports = DataProcessor("airports.csv")
    merge_two_airports(flights, airports, ["ORIGIN", "DESTINATION"])
    holidays = DataProcessor("2015_Public_Holidays.csv")
    # flights.merge(holidays, how="left", on=["MONTH", "DAY"])
    print(flights.get_columns())
    print(len(flights.get_columns()))
