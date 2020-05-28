import pytest
import pandas as pd
import os
from datapreparation import is_international, merge_one_airport

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# merge_one_airport
COLTYPES = {"ORIGIN_AIRPORT": object, "DESTINATION_AIRPORT": object}


def test_merge_one_airport():
    raw_data = pd.read_csv("./data/raw/flights.csv", nrows=100, dtype=COLTYPES)
    airports = pd.read_csv("./data/raw/airports.csv")
    merged_data = merge_one_airport(raw_data, airports, "ORIGIN")


class TestIsInternational:
    def test_empty_string(self):
        assert is_international("") == 0

    def test_contain_inter_uppercase(self):
        assert is_international("INTER") == 1

    def test_contain_inter_lowercase(self):
        assert is_international("inter") == 1

    def test_contain_inter_camelcase(self):
        assert is_international("inter") == 1

    def test_without_international(self):
        assert is_international("abc") == 0
