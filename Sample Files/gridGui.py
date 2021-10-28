import tkinter as tk 
root = tk.Tk()

HEIGHT = 300
WIDTH = 500

canvas = tk.Canvas(root, height=HEIGHT, width = WIDTH)
canvas.pack()

frame = tk.Frame(root, bg = "#80ccff")
frame.place(relx=0.1, rely = 0.1, relheight = 0.8, relwidth = 0.8)

b1 = tk.Button(frame, text="Button1", bg="gray", fg="red")
b1.grid(row=0, column=0, ipadx = 10, ipady = 10, padx = 20, pady = 20) #top left with 10px padding on all sides and 20px "margins"

label = tk.Label(frame, text = "This is a label", bg = "#ffe066")
label.grid(row = 1, column = 1)

entry = tk.Entry(frame, bg='#85e085')
entry.grid(row = 1, column = 2)


root.mainloop()