from polars_query import  PolarsQuery
import time
import argparse

def main():
    # Create an ArgumentParser object to handle command-line arguments
    parser = argparse.ArgumentParser(description="Fetch average temperature for states starting with a given letter.")
    parser.add_argument('letter', type=str, help="The letter to filter states by.") # This argument is a string and represents the letter used to filter states

    # Parse the command-line arguments
    args = parser.parse_args()

    start_time = time.time()

    try:
        # Initialize an instance of PolarsQuery
        query = PolarsQuery(
            letter = args.letter, 
            file="capitals.csv", 
            url="http://api.openweathermap.org/data/2.5/weather", 
            units = "imperial" #Fahrenheit
        )

         # Execute the query to retrieve the filtered DataFrame and average temperature
        result = query.query()

        filtered_df = result[0] # Extract the filtered DataFrame from the result tuple 
        average_temperature =result[1] # Extract the average temperature from the result tuple

        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(filtered_df) if filtered_df is not None else None
        print("Average Temperature :", average_temperature)
        print(f"Program execution time: {elapsed_time:.4f} seconds")

    except ValueError as e:
        print(e)

if __name__ == '__main__':
    main()