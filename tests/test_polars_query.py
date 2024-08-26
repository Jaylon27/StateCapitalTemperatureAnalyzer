import pytest
from unittest.mock import patch
import polars as pl
from polars_query import PolarsQuery

# Sample data for testing
sample_csv_data = [
    {"State": "NY", "Capital": "Albany", "Country": "USA"},
    {"State": "CA", "Capital": "Sacramento", "Country": "USA"},
    {"State": "TX", "Capital": "Austin", "Country": "USA"}
]

# Mock data for the temperature column
mock_temperature_df = pl.DataFrame([
    {"State": "NY", "Capital": "Albany", "Country": "USA", "Temperature": 75.0},
    {"State": "CA", "Capital": "Sacramento", "Country": "USA", "Temperature": 75.0},
    {"State": "TX", "Capital": "Austin", "Country": "USA", "Temperature": 75.0}
])

# Mock data for the weather API
mock_temperature_data = { "main": { "temp": 75.0 }}

# Test for valid input and successful data retrieval
@patch('polars.read_csv')
@patch.object(PolarsQuery, 'query')
def test_query_success(mock_get_temperature, mock_read_csv):

    # Mock the CSV file data
    mock_read_csv.return_value = pl.DataFrame(sample_csv_data)

    # Mock the temperature fetching
    mock_get_temperature.return_value = (mock_temperature_df, 75.0)

     # Create an instance of PolarsQuery
    query = PolarsQuery(letter='A', file='fake_file.csv', url='http://fakeurl.com', units='imperial')

    temperature_df, average_temp = query.query()
   
    # Check the results
    assert temperature_df is not None
    assert average_temp == 75.0
    assert temperature_df.shape == (3, 4)  # Check that the DataFrame has 4 columns including 'Temperature'
    assert 'Temperature' in temperature_df.columns

# Test for invalid letter input
def test_invalid_letter():
    with pytest.raises(ValueError, match="Please enter a valid single letter."):
        PolarsQuery(letter='AB', file='fake_file.csv', url='http://fakeurl.com', units='imperial')


# Test for empty filtered DataFrame
@patch('polars.read_csv')
@patch.object(PolarsQuery, 'query')
def test_no_data(mock_get_temperature, mock_read_csv):
    # Mock the CSV file data with no matching rows
    mock_read_csv.return_value = pl.DataFrame(sample_csv_data)
    
    # Mock the temperature fetching
    mock_get_temperature.return_value = (mock_temperature_df, None)
    
    # Create an instance of PolarsQuery with a letter that does not match any state
    query = PolarsQuery(letter='Z', file='fake_file.csv', url='http://fakeurl.com', units='imperial')
    
    # Execute the query
    temperature_df, average_temp = query.query()
    
    # Check the results
    assert average_temp is None
