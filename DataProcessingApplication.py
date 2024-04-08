import pandas as pd
import numpy as np
from abc import ABC, abstractmethod

class DataProcess(ABC):
    @abstractmethod
    def process_data(self, data):
        pass


class SalesTrendsOverTime(DataProcess):
    def process_data(self, data):
        # Ensure 'Date' is in datetime format
        data['Date'] = pd.to_datetime(data['Date'])

        # Group by year and month, then sum the sales
        grouped = data.groupby([data['Date'].dt.year.rename('Year'), data['Date'].dt.month.rename('Month')])[
            'Sales'].sum().reset_index(name='TotalSales')

        # Reconstruct the 'Date' column for ease of plotting
        grouped['Date'] = pd.to_datetime(grouped.assign(DAY=1)[['Year', 'Month', 'DAY']])

        # Ensure 'Date' is the first column if needed
        cols = ['Date'] + [col for col in grouped.columns if col != 'Date']
        return grouped[cols]


class ProfitAnalysisByCountry(DataProcess):
    def process_data(self, data):
        return data.groupby('Country')['Profit'].sum().reset_index()

class ProductPerformance(DataProcess):
    def process_data(self, data):
        return data.groupby('Product')[['Sales', 'Profit']].sum().reset_index()

class DiscountImpactOnSales(DataProcess):
    def process_data(self, data):
        return data[['Discount Band', 'Sales', 'Profit']]

class MonthlySalesDistribution(DataProcess):
    def process_data(self, data):
        data['Date'] = pd.to_datetime(data['Date'])
        return data.groupby(data['Date'].dt.month)['Sales'].sum().reset_index(name='MonthlySales')


class CountryWiseSalesDistribution(DataProcess):
    def process_data(self, data):
        return data.groupby('Country')['Sales'].sum().reset_index()


class CorrelationAnalysis(DataProcess):
    def process_data(self, data):
        # Updated function to handle non-convertible strings
        def convert_currency(val):
            try:
                # Removing currency symbols and commas
                val = val.replace(',', '').replace('$', '')
                # Converting to float or returning NaN for non-convertible values
                return float(val) if val.strip() != '' and val.strip() != '-' else np.nan
            except Exception as e:
                return np.nan  # Return NaN for any other conversion errors

        # Apply conversion on all specified columns
        for col in ['Units Sold', 'Manufacturing Price', 'Sale Price', 'Gross Sales', 'Discounts', 'Sales', 'Profit']:
            data[col] = data[col].apply(convert_currency)

        return data[['Units Sold', 'Manufacturing Price', 'Sale Price', 'Gross Sales', 'Discounts', 'Sales', 'Profit']].corr()



class DataProcessingContext:
    def __init__(self, strategy: DataProcess):
        self._strategy = strategy

    def set_strategy(self, strategy: DataProcess):
        self._strategy = strategy

    def process(self, data):
        return self._strategy.process_data(data)
