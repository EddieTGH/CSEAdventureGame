from tkinter import *
from tkinter.ttk import * 
from PIL import Image
import os.path


global local_character
global local_backpack
global window

class WeaponsRoom: 
    def __init__(self, master = None): 
        self.master = master 
          
        self.local_character = ''
        self.local_backpack = ''
        
        # to take care movement in x direction 
        self.x = 1
        # to take care movement in y direction 
        self.y = 0
  
        # canvas object to create shape 
        self.canvas = Canvas(master, height = 500, width = 500) 


        self.canvas.pack()


        self.im = Image.open('Character.png').resize((200, 150))
        self.im2 = Image.open('Cafeteria.png').resize((500, 500))
        #Creating source directory for resized backgrounds
        self.directory = os.getcwd() # Use working directory if unspecified
        self.src_directory = os.path.join(self.directory, "src")
        try:
            os.mkdir(self.src_directory)
        except OSError:
            pass # if the directory already exists, proceed

        self.filename = os.path.join(self.src_directory, "RESIZED_Character.png")
        self.bg_filename = os.path.join(self.src_directory, "RESIZED_Cafeteria_Background.png")
        self.im.save(self.filename, 'png')
        self.im2.save(self.bg_filename, 'png')
        
        self.background_image = PhotoImage(file = self.bg_filename)

        self.character = PhotoImage(file = self.filename)
        self.bg_image = self.canvas.create_image(0, 0, image = self.background_image, anchor = NW)
        self.image = self.canvas.create_image(250, 250, image=self.character, anchor='c')

        self.exit_btn = Button(self.canvas, text = "Exit to main")

        self.character_coordX = 0                     
        self.character_coordY = 0 
        print(str(self.character_coordX)+", "+str(self.character_coordY))
      
    def movement(self): 
  
        # This is where the move() method is called 
        # This moves the rectangle to x, y coordinates 
        self.canvas.move(self.image, self.x, self.y) 
        print(str(self.character_coordX)+", "+str(self.character_coordY))
      
    # for motion in negative x direction 
    def left(self, event): 
        if self.character_coordX > -215:
            self.x = -2.5
            self.y = 0
            self.character_coordX += -2.5
            self.movement()
        
      
    # for motion in positive x direction 
    def right(self, event): 
        if self.character_coordX < 220:
            self.x = 2.5
            self.y = 0
            self.character_coordX += 2.5
            self.movement()
      
    # for motion in positive y direction 
    def up(self, event): 
        if self.character_coordY < 200:
            self.x = 0
            self.y = -2.5
            self.character_coordY += 2.5
            self.movement()
        
    # for motion in negative y direction 
    def down(self, event): 
        if self.character_coordY > -200:
            self.x = 0
            self.y = 2.5
            self.character_coordY += -2.5
            self.movement()

    def receiveObjects(self, character, backpack):
        self.local_character = character
        self.local_backpack = backpack