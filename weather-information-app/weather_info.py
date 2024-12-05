import tkinter as tk
from tkinter import messagebox
import requests

# Function to fetch weather data
def get_weather():
    city = entry_city.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name")
        return

    API_KEY = "b0628d33ea5dec6ddaf724704cb881bc"  # Replace with your API key
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    
    # Send the request to OpenWeatherMap API
    response = requests.get(BASE_URL, params={'q': city, 'appid': API_KEY, 'units': 'metric'})
    
    if response.status_code == 200:
        data = response.json()
        city_name = data['name']
        country = data['sys']['country']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        weather_description = data['weather'][0]['description']

        # Display the results
        label_result.config(
            text=f"Weather in {city_name}, {country}:\n"
                 f"Temperature: {temperature}°C\n"
                 f"Humidity: {humidity}%\n"
                 f"Condition: {weather_description.capitalize()}"
        )
    else:
        messagebox.showerror("City Not Found", "City not found. Please check the city name.")

# Create the main window
root = tk.Tk()
root.title("Weather Information App")
root.geometry("400x300")
root.config(bg="#f0f0f0")

# Create widgets
label_city = tk.Label(root, text="Enter City Name:", font=("Arial", 14), bg="#f0f0f0")
label_city.pack(pady=10)

entry_city = tk.Entry(root, font=("Arial", 12), width=20)
entry_city.pack(pady=10)

btn_get_weather = tk.Button(root, text="Get Weather", font=("Arial", 12), bg="#4CAF50", fg="white", command=get_weather)
btn_get_weather.pack(pady=10)

label_result = tk.Label(root, text="", font=("Arial", 12), bg="#f0f0f0", justify="left")
label_result.pack(pady=20)

# Run the application
root.mainloop()
