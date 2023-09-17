import requests #for HTTP requests
from dotenv import load_dotenv #to load environment variables from a .env file
import os #to access environment variable


class Weather:
    #Defining the constructor for the Weather class
    def __init__(self,city):
        #Loading environment variables from a .env file
        load_dotenv()
        #Checing if the city argument is empty
        if not city:
            raise ValueError("City cannot be empty") #Raising a ValueError if the city argument is empty
        self.api_key=os.getenv("API_KEY") #Getting the OpenWeatherMap API key from the environment variables
        #Checking if the API key is missing
        if not self.api_key:
            raise ValueError("API key not found in .env file.") #Raising a ValueError if the API key is missing
        self.city=city
        #Calling the get_user_operation to prompt the user for an operation
        self.get_user_operation() 

    #Defining a method to get weather data from the OpenWeatherMap API
    def get_weather_data(self):
        #Creating the API URL 
        url=f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}"
        try:
            response=requests.get(url) #Making an HTTP get request to the API
            response.raise_for_status() #Raising an exception if the response has an HTTP error status code
        #Catching HTTP errors
        except requests.exceptions.HTTPError as error:
            #Checking if the API is available
            if error.response.status_code==503:
                print("Server is currently unavailable. Please try again later.")
            else:
                print("HTTP error:",error) #Print an HTTP error message
        #Catching other exceptions
        except Exception as e:
            print("Error:",e)
        else:
            #Converting the API response to JSON format
            weather_data=response.json()
            #Returning the weather data
            return weather_data #Returning the weather data

    #Defining a method to get a specific weather parameter from the weather data
    def get_parameter(self,parameter):
        #Getting the weather data
        weather_data=self.get_weather_data()
        #Checking if the parameter is "temperature"
        if parameter=="temperature":
            temperature=weather_data["main"]["temp"] #Getting the temperature value from the weather data
            #Return a formatted string with the temperature value
            return f"The temperature in {self.city} is {temperature} degrees celcius."
        #Checking if the parameter is "humidity"
        if parameter=="humidity":
            humidity=weather_data["main"]["humidity"]
            return f"The humidity in {self.city} is {humidity}%."
        #Checking if the parameter is "wind_speed"
        if parameter=="wind_speed":
            wind_speed=weather_data["wind"]["speed"]
            return f"The wind speed in {self.city} is {wind_speed}m/s."
        
    #Defining a method to prompt the user for an operation
    def get_user_operation(self):
        #Asks the user what operation they want to carry out
        user_input="" #Initializing the user_input variable
        print("What operation do you want to carry out? ")
        print("1. Get temperature")
        print("2. Get humidity")
        print("3. Get wind speed")
        print("'q'. Quit\n")

        #Looping until the user's input is valid or the user quits
        while user_input!="q":
            user_input=input("Enter your choice (1-3): ")
            #Checking if the input is valid
            if user_input in ["1","2","3","q"]:
                break
            else:
                print("Invalid input. Please enter a number between 1 and 3.")
        #Calling the get_parameter with the corresponding parameter anfd printing the result
        if user_input=="1":
            print(self.get_parameter("temperature"))
        elif user_input=="2":
            print(self.get_parameter("humidity"))
        elif user_input=="3":
            print(self.get_parameter("wind_speed"))
        else:
            #Quitting the program if the user enters "q"
            quit()


def main():
    #Getting the city name input from the user and capitalizing the first letter
    city=input("Enter the city name: ").capitalize()
    #Creating a Weather object with the city name as the argument
    weather=Weather(city)

if __name__=="__main__":
    main()