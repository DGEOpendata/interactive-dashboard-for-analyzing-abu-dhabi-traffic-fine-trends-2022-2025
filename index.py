python
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Load dataset
data_file = 'Traffic_Fines_2022_2025.xlsx'
data = pd.ExcelFile(data_file).parse('Sheet1')  # Assuming data is on the first sheet

# Initialize Dash app
app = dash.Dash(__name__)

# Create dropdown options for filtering
year_options = [{'label': str(year), 'value': year} for year in data['Year'].unique()]
ticket_type_options = [{'label': ticket_type, 'value': ticket_type} for ticket_type in data['Ticket Type'].unique()]

# Layout of the app
app.layout = html.Div([
    html.H1("Abu Dhabi Traffic Fine Trends (2022-2025)"),
    html.Div([
        html.Label("Year:"),
        dcc.Dropdown(id='year-dropdown', options=year_options, value=None, multi=True),
    ]),
    html.Div([
        html.Label("Ticket Type:"),
        dcc.Dropdown(id='ticket-type-dropdown', options=ticket_type_options, value=None, multi=True),
    ]),
    dcc.Graph(id='trend-graph')
])

# Callback to update the graph based on user input
@app.callback(
    dash.dependencies.Output('trend-graph', 'figure'),
    [
        dash.dependencies.Input('year-dropdown', 'value'),
        dash.dependencies.Input('ticket-type-dropdown', 'value')
    ]
)
def update_graph(selected_years, selected_ticket_types):
    filtered_data = data
    if selected_years:
        filtered_data = filtered_data[filtered_data['Year'].isin(selected_years)]
    if selected_ticket_types:
        filtered_data = filtered_data[filtered_data['Ticket Type'].isin(selected_ticket_types)]

    fig = px.bar(filtered_data, x='Year', y='Count', color='Ticket Type',
                 title="Traffic Fine Trends", labels={'Count': 'Number of Fines'})
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
