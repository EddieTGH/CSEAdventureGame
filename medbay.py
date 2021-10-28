"""
AG2021_1 CSE Choose Your Own Adventure
Group Members: Edmond, Shashwat, and Esben
Date: March 15, 2020
File task description: medbay.py creates the canvas that will house the background image and all of the interactive objects in the medbay room
that can be accessed by the main character. It creates a canvas that is populated with a pixel art background and with consumables 
that increase the character's performance in the boss room
"""


from tkinter import *
from tkinter.ttk import * 
from PIL import Image
import os.path
from item import InteractiveItem
from commonmethods import CommonMethods

global local_character
global local_backpack
global local_base
class MedBayRoom: 
    def __init__(self, character, backpack, base, master = None): 
        self.master = master 
        global local_character
        global local_backpack
        global local_base
        local_character = character
        local_backpack = backpack
        local_base = base

        # to take care movement in x direction 
        self.x = 1
        # to take care movement in y direction 
        self.y = 0
  
         
        

        #Opening images and resizing them using PIL
        self.im = Image.open('Character.png').resize((200, 150))
        self.im2 = Image.open('Original Backgrounds/medbay-drawing-pixilart.png').resize((500, 500))
        self.flashlight_img = Image.open('Images/Flashlight.png').resize((40, 40))
        self.fork_img = Image.open('src/fork.png').resize((30,30))
        self.spoon = Image.open('src/spoon.png').resize((30,30))
        self.syringe = Image.open('src/syringe.png').resize((50, 50))
        
        #Creating source directory for resized backgrounds
        self.directory = os.getcwd() # Use working directory if unspecified
        self.src_directory = os.path.join(self.directory, "src")
        try:
            os.mkdir(self.src_directory)
        except OSError:
            pass # if the directory already exists, proceed """

        #Creating filenames
        self.filename = os.path.join(self.src_directory, "RESIZED_Character.png")
        self.bg_filename = os.path.join(self.src_directory, "RESIZED_MedBay_Background_ACTUAL.png")
        self.flash_filename = os.path.join(self.src_directory, 'RESIZED_Flashlight.png')
        self.fork_filename = os.path.join(self.src_directory, 'RESIZED_Fork.png')
        self.spoon_filename = os.path.join(self.src_directory, "RESIZED_Spoon.png")
        self.syringe_filename = os.path.join(self.src_directory, "RESIZED_syringe.png")
        self.bandage_filename = os.path.join(self.src_directory, 'RESIZED_bandage50x30.png')

        #Saving images to src
        self.im.save(self.filename, 'png')
        self.im2.save(self.bg_filename, 'png')
        self.flashlight_img.save(self.flash_filename, 'png')
        self.fork_img.save(self.fork_filename, 'png')
        self.spoon.save(self.spoon_filename, 'png')
        self.syringe.save(self.syringe_filename, 'png')

        

        #Making photoImage objects for character and background
        self.background_image = PhotoImage(file = self.bg_filename)
        self.character = PhotoImage(file = self.filename)
        

        
        #Populating space with objects
        self.objects = []       #list of InteractiveItem objects
        self.object_images = [] #list of tkinter canvas images
        #adding an InteractiveItem object
        self.objects.append(InteractiveItem(390, 430, 130, 150, 'flashlight', 'src/RESIZED_Flashlight.png', 420, 140, 'backpackIconFiles/flashlight.png', 'pickupable', True, 'flashlight'))
        self.objects.append(InteractiveItem(190, 210, 190, 210, 'fork', 'src/RESIZED_Fork.png', 200, 200, 'backpackIconFiles/fork.png', 'pickupable', True, 'fork'))
        self.objects.append(InteractiveItem(90, 110, 90, 110, 'spoon', 'src/RESIZED_Spoon.png', 100, 100, 'backpackIconFiles/spoon.png', 'pickupable', True, 'spoon'))
        self.objects.append(InteractiveItem(300, 342.5, 130, 150, 'syringe', 'src/RESIZED_syringe.png', 325, 90, 'backpackIconFiles/syringe.png', 'consumable', True, 'syringe', 5))
        self.objects.append(InteractiveItem(155, 182.5, 130, 150, 'bandage', 'src/RESIZED_bandage50x30.png', 172, 88, 'backpackIconFiles/bandage.png', 'consumable', True, 'bandage',5))
        self.objects.append(InteractiveItem(250, 270, 140, 160, 'laundry key', 'src/RESIZED_laundry_key50x50.png', 260, 150, 'backpackIconFiles/laundry_key.png', 'pickupable', True, 'laundry_key'))
        #populating self.object_images with canvas images; this also puts them on the canvas; uses tags for selective deleting later
        #for item in self.objects:
        #    self.object_images.append(self.canvas.create_image(item.getX(), item.getY(), image = item.getPhotoImage(), anchor = 'c', tags = (item.getName())))

        #Initializing Buttons so that they can be withdrawn later
        self.pickup_btn = Button(master, text = "pick up", state = DISABLED, command = lambda: self.methods.pickUpObject())
        self.consume_btn = Button(master, text = "consume", state = DISABLED, command = lambda:self.methods.consumeObject())

        #Setting initial character coordinates
        self.character_coordX = 250                     
        self.character_coordY = 250
        print(str(self.character_coordX)+", "+str(self.character_coordY))

        #Common methods declaration
        self.methods = CommonMethods(
            local_backpack, 
            local_character, 
            local_base, 
            self.objects, 
            self.object_images, 
            #self.pickup_btn,
            #"""self.canvas, """,
            self.character_coordX, 
            self.character_coordY,
            self.x,
            self.y,
            (100, 400, 115, 380) 
            #self.image
            )

    #Function to initialize things more than once, every time we enter 
    def Render_Canvas(self, backpack, character, base, master = None):
        global objects_initialized
        global local_backpack
        global local_character
        global local_base
        #Syncing up backpack, character, and base
        local_backpack = backpack
        local_character = character
        local_base = base

        # canvas object to create room 
        self.canvas = Canvas(master, height = 500, width = 500)
        self.canvas.pack()

        #Setting initial character coordinates
        self.character_coordX = 250                     
        self.character_coordY = 250
        self.methods.setCoordinates((250, 250))
        print(str(self.character_coordX)+", "+str(self.character_coordY))
        #Making the background image, the room label, and the character image
        self.bg_image = self.canvas.create_image(0, 0, image = self.background_image, anchor = NW)
        self.room_name = self.canvas.create_text(247, 446, fill = 'red', text = "MED BAY", font = ('Helvetica', 10, 'bold'), anchor = 'c')
        self.image = self.canvas.create_image(250, 250, image=self.character, anchor='c')
        #Populating the canvas with the associated images of InteractiveItem objects in the self.objects list
        for item in self.objects:
            if item.getVisibility():
                self.object_images.append(self.canvas.create_image(item.getX(), 
                    item.getY(), 
                    image = item.getPhotoImage(), 
                    anchor = 'c', 
                    tags = (item.getTag())))

        #Initializing Buttons
        self.pickup_btn = Button(master, text = "pick up", state = DISABLED, command = lambda: self.pickUpObject(self.canvas))
        self.pickup_btn.place(relx = 0.7, rely = 0.9, relwidth = 0.25, relheight = 0.05)
        self.consume_btn = Button(master, text = "consume", state = DISABLED, command = lambda: self.consumeObject())
        self.consume_btn.place(relx = 0.7, rely = 0.75, relwidth = 0.25, relheight = 0.05)

    #The following methods serve as bridges between the main file and the commonMethods object, as the path the program takes must grab various objects along the way that can
    #only be accessed in this file
    def pickUpObject(self, canvas):
        self.methods.pickUpObject(canvas, self.pickup_btn, self.consume_btn)

    def consumeObject(self):
        self.methods.consumeObject(self.pickup_btn, self.consume_btn, self.canvas)

    def right(self, e):
        self.methods.right(e, self.canvas, self.image, self.pickup_btn, self.consume_btn)

    def left(self, e):
        self.methods.left(e, self.canvas, self.image, self.pickup_btn, self.consume_btn)

    def up(self, e):
        self.methods.up(e, self.canvas, self.image, self.pickup_btn, self.consume_btn)

    def down(self, e):
        self.methods.down(e, self.canvas, self.image, self.pickup_btn, self.consume_btn)

    def dropObject(self, dropped_object, backpack):
        global local_backpack
        local_backpack = backpack
        self.methods.dropObject(dropped_object, backpack, self.canvas)

    def getCommonObject(self):
        return self.methods

    def deleteCommon(self):
        del self.methods
