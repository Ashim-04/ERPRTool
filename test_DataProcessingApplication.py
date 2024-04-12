import pytest
from DataProcessingApplication import (
    DataProcess, SalesTrendsOverTime, ProfitAnalysisByCountry, ProductPerformance,
    DiscountImpactOnSales, MonthlySalesDistribution, CountryWiseSalesDistribution,
    CorrelationAnalysis, DataProcessingContext
)
import pandas as pd
from unittest.mock import Mock

# Test the Abstract Base Class DataProcess
def test_DataProcess_cannot_be_instantiated():
    with pytest.raises(TypeError):
        DataProcess()

# Create a fixture for sample data
@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'Date': pd.date_range(start='2022-01-01', periods=4, freq='M'),
        'Sales': [100, 200, 150, 250],
        'Country': ['US', 'US', 'UK', 'UK'],
        'Product': ['A', 'B', 'A', 'B'],
        'Profit': [50, 80, 60, 100],
        'Discount Band': ['Low', 'Medium', 'High', 'Low']
    })

# Example test for one of the concrete classes
class TestSalesTrendsOverTime:
    def test_process_data(self, sample_data):
        processor = SalesTrendsOverTime()
        result = processor.process_data(sample_data)
        assert not result.empty
        assert 'Year' in result.columns
        assert 'Month' in result.columns
        assert 'TotalSales' in result.columns



# Tests for ProfitAnalysisByCountry
class TestProfitAnalysisByCountry:
    def test_process_data(self, sample_data):
        processor = ProfitAnalysisByCountry()
        result = processor.process_data(sample_data)
        assert not result.empty
        assert 'Country' in result.columns
        assert 'Profit' in result.columns
        # More assertions can be added to verify correctness of the processed data

# Tests for ProductPerformance
class TestProductPerformance:
    def test_process_data(self, sample_data):
        processor = ProductPerformance()
        result = processor.process_data(sample_data)
        assert not result.empty
        assert 'Product' in result.columns
        assert 'Sales' in result.columns
        assert 'Profit' in result.columns
        # Verify the correctness of the aggregation

# Tests for DiscountImpactOnSales
class TestDiscountImpactOnSales:
    def test_process_data(self, sample_data):
        processor = DiscountImpactOnSales()
        result = processor.process_data(sample_data)
        assert not result.empty
        assert 'Discount Band' in result.columns
        assert 'Sales' in result.columns
        assert 'Profit' in result.columns
        # Additional checks can be added to verify the data integrity

# Tests for MonthlySalesDistribution
class TestMonthlySalesDistribution:
    def test_process_data(self, sample_data):
        processor = MonthlySalesDistribution()
        result = processor.process_data(sample_data)
        assert not result.empty
        assert 'Date' in result.columns  # Updated to reflect the actual column name
        assert 'MonthlySales' in result.columns
        # Additional checks can be added, such as ensuring that 'Date' column contains months

# Tests for CountryWiseSalesDistribution
class TestCountryWiseSalesDistribution:
    def test_process_data(self, sample_data):
        processor = CountryWiseSalesDistribution()
        result = processor.process_data(sample_data)
        assert not result.empty
        assert 'Country' in result.columns
        assert 'Sales' in result.columns
        # Validate the correct aggregation of sales by country

# Tests for CorrelationAnalysis
class TestCorrelationAnalysis:
    def test_process_data(self, sample_data):
        processor = CorrelationAnalysis()
        # Updating sample data to include necessary columns for correlation analysis
        additional_data = pd.DataFrame({
            'Units Sold': [100, 150, 200, 250],
            'Manufacturing Price': [10, 20, 10, 30],
            'Sale Price': [20, 30, 20, 40],
            'Gross Sales': [2000, 3000, 4000, 5000],
            'Discounts': [200, 300, 400, 500],
            'Sales': [1800, 2700, 3600, 4500],
            'Profit': [900, 1350, 1800, 2250]
        })
        sample_data = pd.concat([sample_data, additional_data], axis=1)
        result = processor.process_data(sample_data)
        assert not result.empty
        # The result should be a correlation matrix
        assert result.shape[0] == result.shape[1]
        # More detailed checks can be added to verify the correctness of the correlation values

# Test for DataProcessingContext
class TestDataProcessingContext:
    def test_context_uses_strategy(self, sample_data):
        strategy = Mock(spec=DataProcess)
        context = DataProcessingContext(strategy)
        context.process(sample_data)
        strategy.process_data.assert_called_once_with(sample_data)

    def test_context_changes_strategy(self, sample_data):
        strategy1 = Mock(spec=DataProcess)
        strategy2 = Mock(spec=DataProcess)
        context = DataProcessingContext(strategy1)
        context.set_strategy(strategy2)
        context.process(sample_data)
        strategy2.process_data.assert_called_once_with(sample_data)
        strategy1.process_data.assert_not_called()