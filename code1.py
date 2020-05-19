import os
from abc import ABCMeta, abstractmethod


class DataProcessor(metaclass=ABCMeta):
    """Base processor to be used for all preparation."""

    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_directory = output_directory

    @abstractmethod
    def read(self):
        """Read raw data."""
        pass

    @abstractmethod
    def process(self):
        """Processes raw data. This step should create the raw dataframe with all the required features. Shouldn't implement statistical or text cleaning."""
        pass

    @abstractmethod
    def save(self):
        """Saves processed data."""
        pass
