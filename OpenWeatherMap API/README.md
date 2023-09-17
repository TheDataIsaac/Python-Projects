## OpenWeatherMap Weather App
This Python application uses the OpenWeatherMap API to get current weather data for a specified city. The user is prompted to choose an operation - get temperature, get humidity, or get wind speed - and the corresponding information is returned. The code uses the requests library to make HTTP requests to the API and the dotenv library to load an API key from a .env file.

### Prerequisites
- Python 3.x
- OpenWeatherMap API key (free or paid)
- requests library (can be installed using pip)
- dotenv library (can be installed using pip)

### Usage
Run the program using python main.py.
Enter the name of a city when prompted.
Choose an operation by entering a number (1, 2, or 3) when prompted:
Get temperature
Get humidity
Get wind speed
The program will return the corresponding information for the specified city.

#### License
This code is licensed under the MIT License. See LICENSE for more information.