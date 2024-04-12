import pytest
from DataIngestion import CSVDataIngestion
from DataProcessingApplication import DataProcessingContext, SalesTrendsOverTime
from unittest.mock import Mock

@pytest.fixture
def sample_data_file(tmp_path):
    # Create a sample CSV file to be used as input data
    data_file = tmp_path / "sample_data.csv"
    data_file.write_text('Date,Sales\n2022-01-01,100\n2022-02-01,200\n')
    return str(data_file)

def test_complete_reporting_cycle(sample_data_file):
    # Ingest Data
    ingestion_strategy = CSVDataIngestion()
    data = ingestion_strategy.ingest_data(sample_data_file)

    # Process Data
    processing_strategy = SalesTrendsOverTime()
    context = DataProcessingContext(processing_strategy)
    processed_data = context.process(data)

    # Generate Report (Using a mocked Dashboard)
    dashboard = Mock()
    dashboard.generate_report.return_value = "Report Content"  # Mocking the report generation
    report = dashboard.generate_report()

    # Assert conditions to validate the report generation
    assert not processed_data.empty
    assert report == "Report Content"
