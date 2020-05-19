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

    def rename_column(self, old_colname: str, new_colname: str):
        """How to rename multiple columns?
        """
        self.data = self.data.rename(columns={old_colname: new_colname})

    def drop_columns(self, colnames: list):
        self.data = self.data.drop(colnames, axis=1)

    def save_csv(self, filepath: str):
        """Saves processed data."""
        self.data.to_csv(filepath)

    def merge(self, newdata, how: str, left_on: str, right_on: str):
        self.data = pd.merge(
            self.data, newdata.data, how=how, left_on=left_on, right_on=right_on
        )


class FeatureSelector:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.columns = self.data.columns

    def get_columns(self):
        return self.columns

    def remove_columns(self, removecols: list):
        newcols = list(set(self.columns) - set(removecols))
        self.columns = newcols


if __name__ == "__main__":
    coltypes = {"ORIGIN_AIRPORT": object, "DESTINATION_AIRPORT": object}
    flights = DataProcessor("flights.csv", 100, dtype=coltypes)
    airports = DataProcessor("airports.csv")
    flights.merge(airports, how="inner", left_on="ORIGIN_AIRPORT", right_on="IATA_CODE")
    print(flights.get_columns())
