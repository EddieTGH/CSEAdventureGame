import tkinter as tk
import requests
import json

#Building a basic GUI
api_key = "952e07264cb401dc776daf3668fc19fb"
root = tk.Tk()

#Setting height and width
HEIGHT = 300
WIDTH = 200

canvas = tk.Canvas(root, height=HEIGHT, width = WIDTH)
canvas.pack()

frame = tk.Frame(root, bg = "#80ccff")
frame.place(relx=0.1, rely = 0.1, relheight = 0.8, relwidth = 0.8)

b1 = tk.Button(frame, text="Button1", bg="gray", fg="red")
b1.pack(side="left", fill='none', expand = 'false')

label = tk.Label(frame, text = "This is a label", bg = "#ffe066")
label.pack(side="left")

entry = tk.Entry(frame, bg='#85e085')
entry.pack(side='left', fill = 'x')


root.mainloop()