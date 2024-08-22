import polars as pl
from weather_data_fetcher import WeatherDataFetcher

class PolarsQuery:
    def __init__(self, letter, file, url, units):

        # Validate that the provided letter is a single alphabetic character
        if not (letter.isalpha() and len(letter) == 1):
            raise ValueError("Please enter a valid single letter.")
        
        self.letter = letter.upper()
        self.file = file
        self.url = url
        self.units = units

    def query(self):

        api_key = "daa0571a94dc72cbed431b170ad71c6f"

        # Read the CSV file into a DataFrame using Polars
        df = pl.read_csv(self.file)

        # Filter the DataFrame to include only rows where the state name starts with the given letter
        filtered_df = df.filter(pl.col("State").str.starts_with(self.letter))

        # If the filtered DataFrame is empty, print a message and return None values
        if filtered_df.is_empty():
            print(f"No data available for states starting with the letter '{self.letter.upper()}'. Please try another letter.")
            return None, None
        
        # Create an instance of WeatherDataFetcher to retrieve temperature data
        data_fetcher = WeatherDataFetcher(api_key)

        # Add a new 'Temperature' column to the filtered DataFrame by fetching the current temperature for each capital
        temperature = filtered_df.with_columns([
            pl.struct(pl.all()).map_elements(
                lambda row: data_fetcher.get_current_temperature(
                    self.url, 
                    row["Capital"], 
                    row["State"], 
                    row["Country"], 
                    self.units,
                ), 
                return_dtype=pl.Int64
            ).alias("Temperature") # Name the new column 'Temperature'
        ])

        # Calculate the average temperature from the 'Temperature' column
        average_temperature = round(temperature["Temperature"].mean())

        return temperature, average_temperature  # Return the updated DataFrame with the temperature data and the average temperature

