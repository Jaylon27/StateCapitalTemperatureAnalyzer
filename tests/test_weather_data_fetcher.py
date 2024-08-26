import pytest
import requests
import json
from unittest.mock import patch
from weather_data_fetcher import WeatherDataFetcher


# Mock data for the weather API
mock_response_data = { "main": { "temp": 71 } }

@patch('requests.get')
def test_fetch_data_success(mock_get):

    # Mock the behavior of requests.get to return a successful response
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = json.dumps(mock_response_data)
    
    # Initialize the WeatherDataFetcher with a fake API key
    fetcher = WeatherDataFetcher(api_key='fake_api_key')
    
    # Call the fetch_data method with test parameters
    result = fetcher.fetch_data('http://fakeurl.com', 'Atlanta', 'GA', 'US', 'imperial')
    
    # Verify that the result matches the mock data
    assert result ==  mock_response_data

    mock_get.assert_called_once_with(
        'http://fakeurl.com',
        params={
            'appid': 'fake_api_key',
            'q': 'Atlanta,GA,US',
            'units': 'imperial'
        }
    )

# Test for the fetch_data method when the API call fails
@patch('requests.get')
def test_fetch_data_failure(mock_get):

    # Test that an exception is raised when fetch_data fails
    mock_get.return_value.status_code = 404
    mock_get.return_value.text = 'Not Found'

    # Initialize the WeatherDataFetcher with a fake API key
    fetcher = WeatherDataFetcher(api_key='fake_api_key')

    # Test that an exception is raised when fetch_data fails
    with pytest.raises(Exception) as exc_info:
        fetcher.fetch_data('http://fakeurl.com', 'Atlanta', 'GA', 'US', 'imperial')

    # Verify that the exception message matches the expected failure message
    assert str(exc_info.value) == "Failed to fetch data: 404 Not Found"

# Test for the get_current_temperature method
@patch('requests.get')
def test_get_current_temperature(mock_get):
    
    # Mock the behavior of requests.get to return a successful response
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = json.dumps(mock_response_data)
    
    # Initialize the WeatherDataFetcher with a fake API key
    fetcher = WeatherDataFetcher(api_key='fake_api_key')

    # Call the get_current_temperature method with test parameters
    temperature = fetcher.get_current_temperature('http://fakeurl.com', 'Atlanta', 'GA', 'US', 'imperial')
    
    # Check that the temperature matches the mock data
    assert temperature == 71