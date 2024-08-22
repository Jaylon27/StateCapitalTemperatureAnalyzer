# StateCapitalTemperatureAnalyzer

- **Web App**: [Access the Dashboard App](https://app-d4h36xqh4cp46.azurewebsites.net/)
- **Command-Line Tool**: [Docker Image for Command-Line Tool](https://hub.docker.com/r/jjones380/weatherprojectimages)

## Summary

This project is designed to analyze weather data for capital cities in the United States. It includes two primary components:

1. **Command-Line Tool**: A Python script that fetches weather data for states based on their initial letter and calculates the average temperature of capitals in those states.
2. **Dashboard App**: A Dash application that visualizes the temperature data on a web dashboard. Users can input a letter to filter the states and see a bar chart along with summary statistics.

## Technologies Used

### Python
- **`polars`**: Used for data manipulation and querying.
- **`requests`**: Used to make HTTP requests to the Open Weather API.
- **`plotly(dash)`**: Used to create the interactive web dashboard.
- **`pytest`**: Utilized for testing the application's functionality.

### Docker
- Docker is used to containerize both the command-line tool and the dashboard application, making it easier to deploy and manage dependencies.

### Azure
- **Azure Container Registry (ACR)**: Used to store Docker images.
- **Azure App Service**: Hosts the Dash application.
- **Azure Bicep Templates**: Used for infrastructure deployment, including creating resources and setting up role assignments.

## Deployment

### Infrastructure Deployment

The infrastructure is deployed using Azure Bicep templates. The following resources are created:

- **Azure Container Registry**: For storing Docker images.
- **App Service Plan**: For hosting the Dash application.
- **Web App**: Configured to use Docker for deployment.
- **Role Assignment**: Grants the Web App access to the ACR.

### GitHub Actions

Two GitHub Actions workflows automate the process:

1. **Build and Push Docker Image to ACR**

2. **Deploy Infrastructure**

## Testing

The project includes unit tests using `pytest` to ensure the reliability of the code:

  - Tests validate the functionality of data fetching and processing in the `PolarsQuery` class.
  - Tests for valid inputs, handling of invalid inputs, and scenarios where no data is returned.
  - Tests verify the accuracy of data retrieval from the weather API and error handling.
  - Mock HTTP requests are used to simulate API responses and failures.

## Usage

### Command-Line Tool

The command-line tool is designed to fetch and analyze weather data for U.S. capital cities based on the initial letter of the state name.

**Running the Tool**:
   - Pull Command: docker pull jjones380/weatherprojectimages:latest
   - Run Command: docker run --rm jjones380/weatherprojectimages:latest python3 /app/main.py `<letter>`

   **Example:** docker run --rm jjones380/weatherprojectimages:latest python3 /app/main.py M

### Web Dashboard App

The Dash web app provides an interactive interface for exploring the weather data.

#### Accessing the App:

- Visit the web app using the provided link at the top of this README.
- Enter a single letter (A-Z) in the search box to filter the data by state initial.

#### Features:

- **Bar Chart:** Displays the temperature of capital cities.
- **Summary Statistics:** Provides the number of states, average temperature, and the highest and lowest temperatures.


