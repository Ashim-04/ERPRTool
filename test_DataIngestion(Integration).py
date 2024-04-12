import pytest
from DataIngestion import CSVDataIngestion
import pandas as pd

@pytest.fixture
def sample_csv_with_different_delimiter(tmp_path):
    # Create a sample CSV file with a different delimiter
    df = pd.DataFrame({
        'Column1': [1, 2, 3],
        'Column2': ['a', 'b', 'c']
    })
    file_path = tmp_path / "sample_semicolon.csv"
    df.to_csv(file_path, sep=';', index=False)
    return str(file_path)

def test_csv_ingestion_with_different_delimiter(sample_csv_with_different_delimiter):
    # Ingest CSV data assuming the class handles only comma as delimiter
    ingestion_strategy = CSVDataIngestion()
    data = ingestion_strategy.ingest_data(sample_csv_with_different_delimiter)

    # Verify data integrity
    assert not data.empty
    # Additional checks can be added here based on expected behavior

# Adjusted test for data anomalies
def test_csv_ingestion_with_data_anomalies(tmp_path):
    # Create a CSV file with anomalies that should be recognized as NaN
    content = "Column1, Column2\n1, a\n2, \n ,"
    file_path = tmp_path / "sample_anomalies.csv"
    file_path.write_text(content)

    # Ingest data
    ingestion_strategy = CSVDataIngestion()
    data = ingestion_strategy.ingest_data(str(file_path))

    # Verify data handling
    assert not data.empty
    assert data.isnull().sum().sum() > 0  # Expecting missing values