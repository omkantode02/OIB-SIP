# file: weather_app.py
import tkinter as tk
from tkinter import messagebox, ttk
import requests


API_KEY = "6b4cd00b66662e29d12213de3ac3eb81"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city, unit):
    try:
        params = {"q": city, "appid": API_KEY, "units": unit}
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data.get("cod") != 200:
            messagebox.showerror("Error", "City not found or API error.")
            return None

        weather = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"].capitalize(),
            "wind": data["wind"]["speed"]
        }
        return weather
    except Exception as e:
        messagebox.showerror("Error", f"⚠️ {e}")
        return None

def show_weather():
    city = city_entry.get().strip()
    unit_choice = unit_var.get()

    unit = "metric" if unit_choice == "Celsius" else "imperial"

    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    weather = get_weather(city, unit)
    if weather:
        unit_symbol = "°C" if unit == "metric" else "°F"
        output = (
            f"Weather in {weather['city']} ({weather['country']}):\n\n"
            f"🌡 Temperature: {weather['temp']} {unit_symbol}\n"
            f"💧 Humidity: {weather['humidity']}%\n"
            f"☁️ Condition: {weather['condition']}\n"
            f"💨 Wind Speed: {weather['wind']} m/s"
        )
        result_label.config(text=output)


root = tk.Tk()
root.title("Advanced Weather App")
root.geometry("400x400")
root.configure(bg="lightblue")

title = tk.Label(root, text="Weather App", font=("Arial", 18, "bold"), bg="lightblue")
title.pack(pady=10)

frame = tk.Frame(root, bg="lightblue")
frame.pack(pady=10)

city_entry = tk.Entry(frame, font=("Arial", 14))
city_entry.grid(row=0, column=0, padx=5)

unit_var = tk.StringVar(value="Celsius")
unit_menu = ttk.Combobox(frame, textvariable=unit_var, values=["Celsius", "Fahrenheit"], state="readonly", width=10)
unit_menu.grid(row=0, column=1, padx=5)

search_btn = tk.Button(frame, text="Search", command=show_weather, bg="blue", fg="white", font=("Arial", 12, "bold"))
search_btn.grid(row=0, column=2, padx=5)

result_label = tk.Label(root, text="", font=("Arial", 12), bg="lightblue", justify="left")
result_label.pack(pady=20)

root.mainloop()
