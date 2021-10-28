import tkinter as tk 
root = tk.Tk()

HEIGHT = 300
WIDTH = 500

canvas = tk.Canvas(root, height=HEIGHT, width = WIDTH)
canvas.pack()

frame = tk.Frame(root, bg = "#80ccff")
frame.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.8)

button = tk.Button(frame, text = 'Button', bg = 'gray', fg = 'white')
button.place(relx = 0.0, rely = 0, relwidth = 0.25, relheight = 0.25)

label = tk.Label(frame, text = "Label 1", bg = 'gray', fg = 'white')
label.place(relx = 0.3, rely = 0, relwidth = 0.45, relheight = 0.25)

entry = tk.Entry(frame, bg = "#85e085")
entry.place(relx = 0.8, rely = 0, relwidth = 0.2, relheight = 0.25)

root.mainloop()