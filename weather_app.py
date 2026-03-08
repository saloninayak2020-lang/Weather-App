import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime

# Your API key
API_KEY = "insert your own OpenWeatherMap API key here."

def get_weather():
    city = city_entry.get().strip()

    if city == "":
        messagebox.showinfo("Input Error", "Please enter a city name.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            city_name = data["name"]
            country = data["sys"]["country"]
            temperature = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            weather = data["weather"][0]["description"]
            icon_code = data["weather"][0]["icon"]

            # Current time
            time_now = datetime.now().strftime("%H:%M:%S")

            # Update background color depending on weather
            weather_lower = weather.lower()
            if "rain" in weather_lower:
                window.config(bg="lightgray")
            elif "cloud" in weather_lower:
                window.config(bg="silver")
            elif "clear" in weather_lower:
                window.config(bg="skyblue")
            elif "snow" in weather_lower:
                window.config(bg="white")
            else:
                window.config(bg="lightblue")

            # Display result text
            result_text = (
                f"Weather in {city_name}, {country}\n\n"
                f"Temperature: {temperature} °C\n"
                f"Feels Like: {feels_like} °C\n"
                f"Humidity: {humidity}%\n"
                f"Condition: {weather}\n\n"
                f"Last Updated: {time_now}"
            )
            result_label.config(text=result_text, bg=window["bg"])

            # Display weather icon
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_response = requests.get(icon_url)
            icon_image = Image.open(BytesIO(icon_response.content))
            icon_photo = ImageTk.PhotoImage(icon_image)
            icon_label.config(image=icon_photo, bg=window["bg"])
            icon_label.image = icon_photo

        else:
            messagebox.showinfo("Error", "City not found. Please try again.")

    except:
        messagebox.showinfo("Error", "Error connecting to weather service.")

# Create window
window = tk.Tk()
window.title("Weather App")
window.geometry("380x320")
window.resizable(False, False)
window.config(bg="lightblue")

# Title
title_label = tk.Label(window, text="Professional Weather App", font=("Arial", 16, "bold"), bg="lightblue")
title_label.pack(pady=10)

# City label
city_label = tk.Label(window, text="Enter City Name:", font=("Arial", 12), bg="lightblue")
city_label.pack()

# Input box
city_entry = tk.Entry(window, width=25, font=("Arial", 12))
city_entry.pack(pady=5)

# Button
get_button = tk.Button(window, text="Get Weather", command=get_weather, font=("Arial", 12))
get_button.pack(pady=10)

# Weather icon
icon_label = tk.Label(window, bg="lightblue")
icon_label.pack()

# Result label
result_label = tk.Label(window, text="", justify="center", font=("Arial", 10), bg="lightblue")
result_label.pack(pady=10)

# Run app
window.mainloop()