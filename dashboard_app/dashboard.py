import dash
from dash import dcc, html
import plotly.express as px
from polars_query import PolarsQuery


# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([

    # Title
    html.H1("Temperature of Capital Cities by State Initial"),
    
    # Search box to select the state initial
    dcc.Input(
        id='state-initial-input',
        type='text',
        placeholder='Search',
        value='A',  # Default value
        debounce=True,
        className='dash-input',
        style={'width': '70px'}
    ),
    
    # Bar chart
    dcc.Graph(id='temperature-bar-chart', className='dash-graph'),
    
    # Summary statistics
    html.Div(id='summary-stats', className='summary-stats')
    ], 
    
    className='main-container')

# Callback to update the bar chart and summary statistics based on selected state initial
@app.callback(
    [dash.dependencies.Output('temperature-bar-chart', 'figure'),
     dash.dependencies.Output('summary-stats', 'children')],
    [dash.dependencies.Input('state-initial-input', 'value')]
)
def update_dashboard(selected_letter):
    selected_letter = selected_letter.upper().strip() # Convert the input letter to uppercase and remove any leading/trailing whitespace

    # Validate that the input is a single alphabetic letter
    if len(selected_letter) != 1 or not selected_letter.isalpha():
        return dash.no_update, "Please enter a single letter (A-Z)."
    
    # Create an instance of PolarsQuery with the given parameters
    query = PolarsQuery(
        letter=selected_letter,
        file="capitals.csv" ,
        url='http://api.openweathermap.org/data/2.5/weather',
        units='imperial' #Fahrenheit
    )

    # Execute the query to get the filtered DataFrame and average temperature
    filtered_df, avg_temp = query.query()

    
    # Check if no data is returned or the DataFrame is empty
    if filtered_df is None or filtered_df.is_empty():
        return dash.no_update, f"No data available for states starting with the letter '{selected_letter}'. Please try another letter."
    
    # Create Bar Chart
    bar_chart = px.bar(
        filtered_df, 
        x='Capital', 
        y='Temperature',
        title=f'Temperature of Capital Cities in States Starting with {selected_letter}',
        labels={'Temperature': 'Temperature (°F)'},
        text='Temperature',
        hover_data={'State' : True} 
    )

    # Add a dashed horizontal line at the average temperature with a label "Avg" positioned at the top right of the chart
    bar_chart.add_hline(y=avg_temp, line_dash="dash", annotation_text="Avg", annotation_position="top right")
    
    # Find the highest and lowest temperatures
    min_temp = filtered_df['Temperature'].min()
    max_temp = filtered_df['Temperature'].max()

    # Find the index of the rows with the lowest and highest temperature
    idx_min_temp = filtered_df['Temperature'].arg_min()
    idx_max_temp = filtered_df['Temperature'].arg_max()

    # Get the capital associated with the lowest temperature
    capital_min_temp = filtered_df[idx_min_temp, 'Capital']
    capital_max_temp = filtered_df[idx_max_temp, 'Capital']
   
    # Summary Statistics
    summary = [
        html.P([html.Strong("Number of States: "), f"{len(filtered_df)}"]),
        html.P([html.Strong("Average Temperature: "), f"{avg_temp} °F"]),
        html.P([html.Strong("Highest Temperature: "), f"{max_temp} °F ({capital_max_temp})"]),
        html.P([html.Strong("Lowest Temperature: "), f"{min_temp} °F ({capital_min_temp})"]) 
        ]

    return bar_chart, summary

# Run app
if __name__ == '__main__':
    app.run_server(port=8050, host='0.0.0.0')
