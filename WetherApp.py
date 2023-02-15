import requests
import json
import tkinter as tk
import datetime
from geopy.geocoders import Nominatim
from PIL import Image, ImageTk
import os


def get_weather(url, city, api_key):
    params = {"q": city, "appid": api_key}
    response = requests.get(url=url, params=params)
    return response.json()


def get_current_weather_string(data):
    if data['cod'] == 200:
        kelvin = 273  # value of kelvin

        temp = int(data['main']['temp'] - kelvin)  # converting default kelvin value to Celcius
        feels_like_temp = int(data['main']['feels_like'] - kelvin)
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed'] * 3.6
        sunrise = data['sys']['sunrise']
        sunset = data['sys']['sunset']
        timezone = data['timezone']
        cloudy = data['clouds']['all']
        description = data['weather'][0]['description']
        city_name = data['name']

        sunrise_time = time_format_for_location(sunrise + timezone)
        sunset_time = time_format_for_location(sunset + timezone)

        return f"\nWeather of: {city_name}\nTemperature (Celsius): {temp}°\nFeels like in (Celsius): {feels_like_temp}°\nPressure: {pressure} hPa\nHumidity: {humidity}%\nSunrise at {sunrise_time} and Sunset at {sunset_time}\nCloud: {cloudy}%\nInfo: {description}"
    else:
        return "Error getting weather"


def get_forecast_weather(data, text_field):
    if data['cod'] == '200':
        for entry in data['list']:
            kelvin = 273  # value of kelvin

            date = entry['dt_txt']
            temp = int(entry['main']['temp'] - kelvin)  # converting default kelvin value to Celcius
            feels_like_temp = int(entry['main']['feels_like'] - kelvin)
            pressure = entry['main']['pressure']
            humidity = entry['main']['humidity']
            cloudy = entry['clouds']['all']
            description = entry['weather'][0]['description']

            final = f"\nThe forecast for: {date}\nTemperature (Celsius): {temp}°\nFeels like in (Celsius): {feels_like_temp}°\nPressure: {pressure} hPa\nHumidity: {humidity}%\nCloud: {cloudy}%\nInfo: {description}\n\n"
            insert_icon_after_text(text_field, entry, final)


def get_weather_icon(data):
    return data['weather'][0]['icon']


def generate_gui(url, api_key, city_value, current_weather_field, forecast_field):
    current_weather_field.delete("1.0", "end")
    forecast_field.delete("1.0", "end")

    current_data = get_weather(f"{url}/weather", city_value.get(), api_key)
    forecast_data = get_weather(f"{url}/forecast", city_value.get(), api_key)

    insert_icon_after_text(current_weather_field, current_data, get_current_weather_string(current_data))
    get_forecast_weather(forecast_data, forecast_field)


def insert_icon_after_text(text_field, data, text):
    text_field.insert(tk.END, text)
    icon = ImageTk.PhotoImage(Image.open(f"icons/{get_weather_icon(data)}.png"))
    icon_label = tk.Label(text_field, image=icon)
    icon_label.dontloseit = icon
    text_field.window_create(tk.END, window=icon_label)
    text_field.pack()


def intialize_gui(url, api_key):
    root = tk.Tk()
    root.title("Weather App")

    root.geometry("500x500")  # size of the window by default

    city_value = tk.StringVar()

    tk.Label(root, text='Enter City Name', font='Arial 12 bold').pack(pady=10)  # to generate label heading

    tk.Entry(root, textvariable=city_value, width=24, font='Arial 12 bold').pack()

    tk.Button(root, command=lambda: generate_gui(url, api_key, city_value, current_weather_field, forecast_field),
              text="Check Weather",
              font="Arial 10",
              bg='lightblue', fg='black',
              activebackground="teal", padx=5, pady=5).pack(pady=20)

    tk.Label(root, text="The Weather is:", font='arial 12 bold').pack(pady=10)

    current_weather_field = tk.Text(root, width=46, height=10)
    forecast_field = tk.Text(root, width=46, height=60)

    root.mainloop()


def time_format_for_location(utc_with_tz):
    local_time = datetime.datetime.utcfromtimestamp(utc_with_tz)
    return local_time.time()


def main():
    api_key = "[INSERT_YOUR_API_KEY_HERE]"
    url = "https://api.openweathermap.org/data/2.5"
    intialize_gui(url, api_key)


if __name__ == "__main__":
    main()
