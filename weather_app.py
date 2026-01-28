import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO



API_KEY = "914be16d1d73f2f6b057eb38b7b69a91"
is_celsius = True

BG_COLOR = "#87CEEB"
BTN_COLOR = "#19BA51"
TEXT_COLOR = "#C11E1E"

#functions 

def clear_placeholder(event):
    if city_entry.get() == "Enter city name":
        city_entry.delete(0, tk.END)

def toggle_unit():
    global is_celsius
    is_celsius = not is_celsius
    get_weather()

def get_weather():
    city = city_entry.get().strip()

    if city == "" or city == "Enter city name":
        location_label.config(text="Please enter a city name")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            location_label.config(text="City not found")
            temp_label.config(text="")
            desc_label.config(text="")
            humidity_label.config(text="")
            wind_label.config(text="")
            icon_label.config(image="")
            return

        #data
        city_name = data["name"]
        temp_k = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        description = data["weather"][0]["description"].capitalize()
        icon_code = data["weather"][0]["icon"]

       
        if is_celsius:
            temp = temp_k - 273.15
            unit = "°C"
        else:
            temp = (temp_k - 273.15) * 9/5 + 32
            unit = "°F"

       
        location_label.config(text=f"City: {city_name}")
        temp_label.config(text=f"Temperature: {temp:.2f} {unit}")
        desc_label.config(text=f"Weather: {description}")
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_label.config(text=f"Wind Speed: {wind} m/s")

       
        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_image = Image.open(BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_image)

        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo

    except Exception as e:
        location_label.config(text="Error fetching data")

#GUI

root = tk.Tk()
root.title("Weather App by Nikhil singh")
root.geometry("320x520")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

title_label = tk.Label(
    root,
    text="Weather App ",
    font=("calibri", 18, "bold","italic", "underline"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
title_label.pack(pady=20)

city_entry = tk.Entry(
    root,
    font=("Arial", 12),
    justify="center"
)
city_entry.pack(pady=10)
city_entry.insert(0, "Enter city name")
city_entry.bind("<FocusIn>", clear_placeholder)

get_weather_btn = tk.Button(
    root,
    text="Get Weather",
    font=("Arial", 12),
    bg=BTN_COLOR,
    fg="white",
    command=get_weather
)
get_weather_btn.pack(pady=8)

toggle_btn = tk.Button(
    root,
    text="Toggle °C / °F",
    font=("Arial", 10),
    bg=BTN_COLOR,
    fg="white",
    command=toggle_unit
)
toggle_btn.pack(pady=5)

icon_label = tk.Label(root, bg=BG_COLOR)
icon_label.pack(pady=5)

location_label = tk.Label(root, font=("Arial", 12), bg=BG_COLOR)
location_label.pack(pady=5)

temp_label = tk.Label(root, font=("Arial", 12), bg=BG_COLOR)
temp_label.pack(pady=5)

desc_label = tk.Label(root, font=("Arial", 12), bg=BG_COLOR)
desc_label.pack(pady=5)

humidity_label = tk.Label(root, font=("Arial", 12), bg=BG_COLOR)
humidity_label.pack(pady=5)

wind_label = tk.Label(root, font=("Arial", 12), bg=BG_COLOR)
wind_label.pack(pady=5)

root.mainloop()

