import pandas as pd
import json
import xml.etree.ElementTree as et
from abc import ABC, abstractmethod

# Interface for data ingestion
class DataIngestionStrategy(ABC):
    @abstractmethod
    def ingest_data(self, file_path):
        pass

# Concrete class for CSV data ingestion
class CSVDataIngestion(DataIngestionStrategy):
    def ingest_data(self, file_path):
        return pd.read_csv(file_path)

# Concrete class for JSON data ingestion
class JSONDataIngestion(DataIngestionStrategy):
    def ingest_data(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

# Placeholder concrete class for XML data ingestion
class XMLDataIngestion(DataIngestionStrategy):
    def ingest_data(self, file_path):
        tree = et.parse(file_path)
        root = tree.getroot()
        # The XML parsing logic would be more complex and is dependent on the XML schema
        # This is a placeholder to demonstrate how one might start implementing XML ingestion
        data = [{child.tag: child.text for child in root} for child in root]
        return pd.DataFrame(data)

# Context class for data ingestion
class DataIngestionContext:
    def __init__(self, strategy: DataIngestionStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: DataIngestionStrategy):
        self._strategy = strategy

    def ingest(self, file_path):
        return self._strategy.ingest_data(file_path)