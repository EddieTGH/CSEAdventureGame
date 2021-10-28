from tkinter import *
import tkinter as tk 
from PIL import Image, ImageTk
import os.path

""" class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='640x360+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        try:
            geom=self.master.winfo_geometry()
        except:
            print('No methods named winfo_geometry for toplevel objects')
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom """

root = tk.Tk()
#home_app = FullScreenApp(root)
root.title("Tkinter Home Page")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
#resolution = (screen_width, screen_height)
#root.geometry(str(screen_width) + 'x' + str(screen_height))
root.attributes('-fullscreen', True)
#root.bind("<Escape>", root.attributes('-fullscreen', False))
#root.bind("<F11>", root.attributes('-fullscreen', True))

def returnToMain():  
    root.deiconify()


class MyTkWindow():
    def __init__(self):
        pass
    def initialize(self):
        #Creating window
        self.root = tk.Toplevel()
        self.root.title('Separate Window')

        #setting fullscreen state to true to fill entire screen
        self.fullscreen_state = True
        self.root.attributes('-fullscreen', self.fullscreen_state)
        self.root.bind("<F11>", self.toggle_fullscreen)

        #Determing screen width and height for resolution
        self.resolution = (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        #Creating resized background image
        self.resized_background = Image.open('Images/Medbay_Background.png').resize(self.resolution)

        #Creating source directory for resized backgrounds
        self.directory = os.getcwd() # Use working directory if unspecified
        self.src_directory = os.path.join(self.directory, "src")
        try:
            os.mkdir(self.src_directory)
        except OSError:
            pass # if the directory already exists, proceed

        #Saving resized background to src folder
        self.resized_image_filename = os.path.join(self.src_directory, "RESIZED_Medbay_Background.png")
        self.resized_background.save(self.resized_image_filename, 'png')

        #Opening image for use as background image
        self.bg_image = tk.PhotoImage(file = "src/RESIZED_Medbay_Background.png")
        self.bg_label = tk.Label(self.root, image = self.bg_image)
        self.bg_label.place(relwidth = 1, relheight = 1)
        #Button for returning to homescreen
        self.end_btn = tk.Button(self.root, text = "End Window", command = self.end)
        self.end_btn.place(relx = 0.5, rely = 0.75, relheight = 0.2, relwidth = 0.2, anchor = 'c')
    
    def toggle_fullscreen(self):
        if self.fullscreen_state:
            self.root.geometry('640x360')
            self.fullscreen_state = False
            self.root.attributes('-fullscreen', self.fullscreen_state)
        else:
            self.fullscreen_state = True
            self.root.attributes('-fullscreen', self.fullscreen_state)
    def start(self):
        self.root.mainloop()

    def end(self):
        self.root.destroy()
        returnToMain()


def quit_game():
    root.destroy()


other_window = MyTkWindow()

def startSeparate():
    other_window.initialize()
    root.withdraw()
    other_window.start()

exit_btn = tk.Button(root, text = "Exit Game", command = quit_game)
exit_btn.place(relx = 0.05, rely = 0.05, anchor = 'c', relwidth = 0.05, relheight = 0.05)

btn = tk.Button(root, text = "Start separate window", command = startSeparate)
btn.pack()

root.mainloop()