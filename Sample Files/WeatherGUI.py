import tkinter as tk        #tkinter
from tkinter import Tk,font    #change font props
import requests             #Accessing APIs
import json                 #JSON response processing
from PIL import Image, ImageTk

#Test Button
def getWeather(city):
    api_key = "952e07264cb401dc776daf3668fc19fb"
    units = 'imperial'
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid={}".format(city, units, api_key)
    response = requests.get(url)
    weather = response.json()

    label['text'] = format_response(weather)
    icon_name = weather['weather'][0]['icon']
    open_image(icon_name)

def format_response(weather):
    try:
        name = weather['name']                      #name of city
        desc = weather['weather'][0]['description'] #weather description
        temp = weather['main']['temp']              #temperature
        feels_like = weather['main']['feels_like']
        humid = weather['main']['humidity']
        wind_speed = weather['wind']['speed']

        ds = u'\N{DEGREE SIGN}'                     #Degree symbol
        label_text = 'City: {}\nWeather: {}\nTemperature({}F): {}\nFeels Like ({}F): {}\nHumidity: {}%\nWind Speed: {} mph'.format(
            name, desc, ds, temp, ds, feels_like, humid, wind_speed)
        return label_text
    except:
        label_text = "There is no data retrieved"
        return label_text

def open_image(icon):
    size = int(lowerframe.winfo_height()*0.25)  #return height of lower frame

    #open icon and resize and convert to tk image
    img = ImageTk.PhotoImage(Image.open('./img/{}.png'.format(icon)).resize((size, size)))

    #Remove any icons currently present
    weather_icon.delete('all')

    #Create new image on the canvas
    weather_icon.create_image(0, 0, anchor = 'nw', image=img)
    weather_icon.image=img

#Building GUI

root = tk.Tk()
font.families()

HEIGHT = 700
WIDTH = 800

#top frame for input and button
#lower frame for text from weather API

#Canvas
canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
canvas.pack()

#Add background image
bg_image = tk.PhotoImage(file="Sample Files/landscape2.png")
bg_label = tk.Label(root, image = bg_image)
bg_label.place(relwidth = 1, relheight = 1)

#add upper frame
topframe = tk.Frame(root, bg = '#80ccff', bd = 5)
topframe.place(relx = 0.5, rely = 0.1, relwidth = 0.75, relheight = 0.1, anchor = 'n')

#Add widgets
#Entry
entry = tk.Entry(topframe, font = ('Verdana', 18))
entry.place(relwidth = 0.65, relheight = 1)

#Button
button = tk.Button(topframe, fg = "#3477eb", text = "Get Weather", font = ('MS Sans Serif', 18, 'bold'), command = lambda: getWeather(entry.get()))
button.place(relx = 0.7, relwidth = 0.3, relheight = 1)

#Add lower frame
lowerframe = tk.Frame(root, bg = '#80b7ff', bd = 7)
lowerframe.place(relx = 0.5, rely = 0.25, relwidth = 0.75, relheight = 0.6, anchor = 'n')

#Adding label
bg_color = 'white'
label = tk.Label(lowerframe, bg = bg_color, font = ('Consolas', 18, 'bold italic'), anchor = 'nw', justify = 'left', bd = 5)
label.place(relwidth = 1, relheight = 1)            #Fill entire frame

#Adding Canvas for weather icon
weather_icon = tk.Canvas(label, bg = bg_color, bd = 0, highlightthickness=0)
weather_icon.place(relx = 0.75, rely = 0, relwidth = 1, relheight = 0.5)

root.mainloop()