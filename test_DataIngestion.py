import pytest
from DataIngestion import DataIngestionStrategy, CSVDataIngestion, DataIngestionContext
import pandas as pd
from unittest.mock import Mock


# Test the Abstract Base Class DataIngestionStrategy
def test_DataIngestionStrategy_cannot_be_instantiated():
    with pytest.raises(TypeError):
        DataIngestionStrategy()


# Test the concrete class CSVDataIngestion
class TestCSVDataIngestion:
    def test_ingest_valid_csv(self, tmp_path):
        # Create a sample CSV file
        df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        file_path = tmp_path / "sample.csv"
        df.to_csv(file_path, index=False)

        # Test data ingestion
        ingestion = CSVDataIngestion()
        result = ingestion.ingest_data(file_path)
        pd.testing.assert_frame_equal(result, df)

    def test_ingest_empty_csv(self, tmp_path):
        # Create an empty CSV file
        file_path = tmp_path / "empty.csv"
        file_path.write_text('')

        ingestion = CSVDataIngestion()
        with pytest.raises(pd.errors.EmptyDataError):
            ingestion.ingest_data(file_path)

    def test_ingest_nonexistent_file(self):
        ingestion = CSVDataIngestion()
        with pytest.raises(FileNotFoundError):
            ingestion.ingest_data("nonexistent.csv")


# Test the context class DataIngestionContext
class TestDataIngestionContext:
    def test_context_uses_strategy(self):
        strategy = Mock(spec=DataIngestionStrategy)
        context = DataIngestionContext(strategy)
        context.ingest("path/to/data")
        strategy.ingest_data.assert_called_once_with("path/to/data")

    def test_context_changes_strategy(self):
        strategy1 = Mock(spec=DataIngestionStrategy)
        strategy2 = Mock(spec=DataIngestionStrategy)
        context = DataIngestionContext(strategy1)
        context.set_strategy(strategy2)
        context.ingest("path/to/data")
        strategy2.ingest_data.assert_called_once_with("path/to/data")
        strategy1.ingest_data.assert_not_called()
