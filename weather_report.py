# All the libraries needed for this program to work
import os
import requests
import google.generativeai as genai
from tkinter import *
from dotenv import load_dotenv

load_dotenv()

# Gets the keys from a .env file
geminiKey = os.getenv("GEMINI_API_KEY")
weatherStackKey = os.getenv("WEATHERSTACK_API_KEY")

# Weather Stack
def get_weather(location):
    params = {
        'access_key': weatherStackKey,
        'query': location,
        'units': 'f'
    }

    # Makes the API request
    response = requests.get("http://api.weatherstack.com/current", params=params)
    data = response.json()

    if "error" in data:
        return f"Error: {data['error']['info']}"
    
    else:
        location = data['location']['name']
        temperature = data['current']['temperature']
        condition = data['current']['weather_descriptions'][0]
        return f"Weather in {location}: {condition}, {temperature}°F"


def weatherReport():

    # tKinter window
    root = Tk()
    root.geometry('800x600')

    # Text bar
    textBar = Entry(root, width=50)
    textBar.grid(row=0, column=0)

    # 
    def aIReport():

        # Gets the user's input
        city = textBar.get()
        weatherInfo = get_weather(city)

        # Gets the API key
        genai.configure(api_key=geminiKey)
        # Gemini model type
        model = genai.GenerativeModel("gemini-1.5-flash")
        # Stores the response of the AI in a variable. And also has a very specific prompt
        response = model.generate_content(f"Give summary with some flavor text to \"{weatherInfo}\". I don't need options. IF and only IF the word \"ERROR\" is shows, say \"There seemed to be a typo or unauthorized request. Please try again.\", DO NOT and I repeat, DO NOT talk about an error if the word \"Error\" does not show up")

        # This clears the previous weather report
        geminiResposne = Label(root, text="")

        # Displays the current weather in the City entered
        geminiResposne.config(text=response.text)
        geminiResposne.grid(row=0, column=2)
    
    # A button to submit the city
    button = Button(root, text="Enter", command=aIReport).grid(row=0, column=1)
   

    root.mainloop()

weatherReport()