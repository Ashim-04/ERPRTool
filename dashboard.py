import dash
from dash import html
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from DataIngestion import DataIngestionContext, CSVDataIngestion
from DataProcessingApplication import DataProcessingContext, SalesTrendsOverTime, ProfitAnalysisByCountry, ProductPerformance, DiscountImpactOnSales, ManufacturingVsSalePrice, CountryWiseSalesDistribution, CorrelationAnalysis

# Load and process data
data_ingestion_context = DataIngestionContext(CSVDataIngestion())
sales_data = data_ingestion_context.ingest('datasets/Financials.csv')

data_processing_context = DataProcessingContext(SalesTrendsOverTime())
sales_trends_data = data_processing_context.process(sales_data)

data_processing_context.set_strategy(ProfitAnalysisByCountry())
profit_by_country_data = data_processing_context.process(sales_data)

data_processing_context = DataProcessingContext(ProductPerformance())
product_performance_data = data_processing_context.process(sales_data)

data_processing_context = DataProcessingContext(DiscountImpactOnSales())
discount_impact_data = data_processing_context.process(sales_data)

data_processing_context.set_strategy(CountryWiseSalesDistribution())
country_wise_sales_data = data_processing_context.process(sales_data)

data_processing_context.set_strategy(CorrelationAnalysis())
correlation_analysis_data = data_processing_context.process(sales_data)


# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='ERP System Reporting tool for Sales Data'),

    # Column selector
    html.H3('Select Columns to Display:'),
    dcc.Checklist(
        id='column-selector',
        options=[{'label': col, 'value': col} for col in sales_data.columns],
        value=sales_data.columns.tolist(),  # Default to all columns
        inline=True,
    ),

    html.Button('Uncheck All', id='uncheck-all-button', n_clicks=0),

    # Data Table
    html.H2("ERP System's Data Table"),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in sales_data.columns],  # Columns to be updated in the callback
        data=sales_data.to_dict('records'),
        filter_action='native',  # Enable filtering
        sort_action='native',  # Enable sorting
        sort_mode='multi',  # Allow multi-column sorting
        page_action='native',  # Enable pagination
        page_size=10,  # Number of rows per page
    ),



    dcc.Graph(
        id='sales-trends',
        figure={
            'data': [
                {'x': sales_trends_data['Date'], 'y': sales_trends_data['TotalSales'], 'type': 'line',
                 'name': 'Sales Trends'},
            ],
            'layout': {
                'title': 'Sales Trends Over Time'
            }
        }
    ),

    dcc.Graph(
        id='profit-by-country',
        figure={
            'data': [
                {'x': profit_by_country_data['Country'], 'y': profit_by_country_data['Profit'], 'type': 'bar', 'name': 'Profit by Country'},
            ],
            'layout': {
                'title': 'Profit Analysis by Country'
            }
        }
    ),

    dcc.Graph(
        id='product-performance',
        figure={
            'data': [
                {'x': product_performance_data['Product'], 'y': product_performance_data['Sales'], 'type': 'bar', 'name': 'Sales'},
                {'x': product_performance_data['Product'], 'y': product_performance_data['Profit'], 'type': 'bar', 'name': 'Profit'},
            ],
            'layout': {
                'title': 'Product Performance',
                'barmode': 'stack'
            }
        }
    ),

    dcc.Graph(
        id='country-wise-sales',
        figure={
            'data': [
                {'x': country_wise_sales_data['Country'], 'y': country_wise_sales_data['Sales'], 'type': 'bar', 'name': 'Sales by Country'},
            ],
            'layout': {
                'title': 'Country-wise Sales Distribution',
                'xaxis': {'title': 'Country'},
                'yaxis': {'title': 'Total Sales'}
            }
        }
    ),

    dcc.Graph(
        id='discount-impact',
        figure={
            'data': [
                {'x': discount_impact_data['Discount Band'], 'y': discount_impact_data['Sales'], 'mode': 'markers', 'type': 'scatter', 'name': 'Discount Impact on Sales'},
            ],
            'layout': {
                'title': 'Discount Impact on Sales'
            }
        }
    ),


    dcc.Graph(
        id='correlation-analysis',
        figure={
            'data': [
                {
                    'z': correlation_analysis_data.values,
                    'x': correlation_analysis_data.columns,
                    'y': correlation_analysis_data.index,
                    'type': 'heatmap',
                    'colorscale': 'Viridis',
                }
            ],
            'layout': {
                'title': 'Correlation Analysis',
                'xaxis': {'title': 'Variables'},
                'yaxis': {'title': 'Variables'},
            }
        }
    ),


])


# Define callback to update table columns
@app.callback(
    Output('table', 'columns'),
    Input('column-selector', 'value')
)
def update_table_columns(selected_columns):
    return [{"name": i, "id": i} for i in selected_columns]

# Callback to uncheck all checklist options
@app.callback(
    Output('column-selector', 'value'),
    Input('uncheck-all-button', 'n_clicks'),
    prevent_initial_call=True
)
def uncheck_all_columns(n_clicks):
    if n_clicks > 0:
        return []
    raise dash.exceptions.PreventUpdate



if __name__ == '__main__':
    app.run_server(debug=True)
