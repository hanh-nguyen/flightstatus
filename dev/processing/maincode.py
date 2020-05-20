import code2 as c

coltypes = {"ORIGIN_AIRPORT": object, "DESTINATION_AIRPORT": object}
flights = c.DataProcessor("flights.csv", 100, dtype=coltypes)
airports = c.DataProcessor("airports.csv")
holidays = c.DataProcessor("2015_Public_Holidays.csv")
# add new variables based on departure and arrival airports
# TODO: write pytest to check if any airport can't be matched
c.merge_two_airports(flights, airports, ["ORIGIN", "DESTINATION"])
# add holiday days
flights.merge(holidays, how="left", on=["MONTH", "DAY"])
print(flights.get_columns())
print(len(flights.get_columns()))
