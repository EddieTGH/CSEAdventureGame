"""
AG2021_1 CSE Choose Your Own Adventure
Group Members: Edmond, Shashwat, and Esben
Date: March 15, 2020
File task description: medbay.py creates the canvas that will house the background image and all of the interactive objects in the medbay room
that can be accessed by the main character. It creates a canvas that is populated with a pixel art background image and interactive objects.
It contains three interactive washing machines where you can place suits of armor. There are 6 in the room that can be consumed by picking
them up and washing them first. Access to the laundry room is limited, with the player being required to have a laundry_key in their backpack 
before entering
"""

from tkinter import *
from tkinter.ttk import * 
from PIL import Image
import os.path
import time
from item import InteractiveItem, PressurePlate
from commonmethods import CommonMethods

global local_character
global local_backpack
global local_base
global washing_machine_1
global washing_machine_2
global washing_machine_3
global active_machine  
#Class that creates the laundry room  
class LaundryRoom: 
    def __init__(self, character, backpack, base, master = None): 
        #master is the root
        self.master = master
        #Syncing up the backpack, character, and base objects for continuous updating of character statistics and base health 
        global local_character
        global local_backpack
        global local_base
        local_character = character
        local_backpack = backpack
        local_base = base

        # to take care of movement in x direction 
        self.x = 1
        # to take care of movement in y direction 
        self.y = 0
  
        #List of locations for washing machine labels that tell whether the machine is in use or not
        self.label_locs = [(0.23, 0.19), (0.23, 0.41), (0.23, 0.62)]
        

        #Opening images and resizing them using PIL
        self.im = Image.open('Character.png').resize((200, 150))
        self.flashlight_img = Image.open('Images/Flashlight.png').resize((40, 40))
        self.fork_img = Image.open('src/fork.png').resize((30,30))
        self.spoon = Image.open('src/spoon.png').resize((30,30))
        self.suit = Image.open('src/suit-of-armor.png').resize((70, 70))
        
        #Creating source directory for resized backgrounds
        self.directory = os.getcwd() # Use working directory if unspecified
        self.src_directory = os.path.join(self.directory, "src")
        try:
            os.mkdir(self.src_directory)
        except OSError:
            pass # if the directory already exists, proceed """

        #Creating filenames
        self.filename = os.path.join(self.src_directory, "RESIZED_Character.png")
        self.bg_filename = os.path.join(os.path.join(os.getcwd(), 'Original Backgrounds'), "RESIZED_Laundry_Room_background.png")
        self.locked_bg_filename = os.path.join(os.path.join(os.getcwd(), 'Original Backgrounds'), "RESIZED_Locked_Laundry_Room_background.png")
        self.flash_filename = os.path.join(self.src_directory, 'RESIZED_Flashlight.png')
        self.fork_filename = os.path.join(self.src_directory, 'RESIZED_Fork.png')
        self.spoon_filename = os.path.join(self.src_directory, "RESIZED_Spoon.png")
        #self.syringe_filename = os.path.join(self.src_directory, "RESIZED_syringe.png")
        self.suit_armor_filename = os.path.join(self.src_directory, 'RESIZED_Armor.png')

        #Saving images to src
        self.im.save(self.filename, 'png')
        self.flashlight_img.save(self.flash_filename, 'png')
        self.fork_img.save(self.fork_filename, 'png')
        self.spoon.save(self.spoon_filename, 'png')
        self.suit.save(self.suit_armor_filename, 'png')
        

        #Making photoImage objects for character and background
        self.unlocked_background_image = PhotoImage(file = self.bg_filename)
        self.locked_background_image = PhotoImage(file = self.locked_bg_filename)
        self.character = PhotoImage(file = self.filename)
        

        
        #Populating space with objects
        self.objects = []       #list of InteractiveItem objects
        self.object_images = [] #list of tkinter canvas images
        self.plates = []        #list of pressure plates corresponding to the three washing machines
        #adding InteractiveItem objects
        self.objects.append(InteractiveItem(365, 385, 110, 130, 'flashlight', 'src/RESIZED_Flashlight.png', 375, 120, 'backpackIconFiles/flashlight.png', 'pickupable', True, 'flashlight'))
        self.objects.append(InteractiveItem(190, 210, 190, 210, 'fork', 'src/RESIZED_Fork.png', 200, 200, 'backpackIconFiles/fork.png', 'pickupable', True, 'fork'))
        self.objects.append(InteractiveItem(290, 310, 110, 130, 'spoon', 'src/RESIZED_Spoon.png', 300, 120, 'backpackIconFiles/spoon.png', 'pickupable', True, 'spoon'))
        self.objects.append(InteractiveItem(320, 330, 217.5, 232.5, 'suit of armor', 'src/RESIZED_Armor_35x45.png', 325, 186, 'backpackIconFiles/armor.png', 'pickupable', True, 'suitofarmor1'))
        self.objects.append(InteractiveItem(345, 365, 217.5, 232.5, 'suit of armor', 'src/RESIZED_Armor_35x45.png', 355, 186, 'backpackIconFiles/armor.png', 'pickupable', True, 'suitofarmor2'))
        self.objects.append(InteractiveItem(380, 390, 217.5, 232.5, 'suit of armor', 'src/RESIZED_Armor_35x45.png', 386, 186, 'backpackIconFiles/armor.png', 'pickupable', True, 'suitofarmor3'))
        self.objects.append(InteractiveItem(320, 330, 352.5, 367.5, 'suit of armor', 'src/RESIZED_Armor_35x45.png', 325, 321, 'backpackIconFiles/armor.png', 'pickupable', True, 'suitofarmor4'))
        self.objects.append(InteractiveItem(345, 365, 352.5, 367.5, 'suit of armor', 'src/RESIZED_Armor_35x45.png', 355, 321, 'backpackIconFiles/armor.png', 'pickupable', True, 'suitofarmor5'))
        self.objects.append(InteractiveItem(380, 390, 352.5, 367.5, 'suit of armor', 'src/RESIZED_Armor_35x45.png', 386, 321, 'backpackIconFiles/armor.png', 'pickupable', True, 'suitofarmor6'))

        #Pressure plates
        self.plates.append(PressurePlate(105, 127.5, 132.5, 150, 116, 141, 'wash_1', True))
        self.plates.append(PressurePlate(105, 127.5, 240, 260, 116, 250, 'wash_2', True))
        self.plates.append(PressurePlate(105, 127.5, 345, 365, 116, 355, 'wash_3', True))
        #Locations of washing machines for putting the armors when they are done washing
        self.wash_locations = [(116, 141), (116, 250), (116, 355)]
        #Washing machine objects list
        self.machines = [WashMachine(False, None), WashMachine(False, None), WashMachine(False, None)]

        #Setting initial character coordinates
        self.character_coordX = 250                     
        self.character_coordY = 250
        print(str(self.character_coordX)+", "+str(self.character_coordY))

        #CommonMethods object declaration
        self.methods = CommonMethods(
            local_backpack, 
            local_character, 
            local_base, 
            self.objects, 
            self.object_images, 
            self.character_coordX, 
            self.character_coordY,
            self.x,
            self.y,
            (100, 400, 115, 380) 
            )

    #Function to render things more than once, every time we enter 
    def Render_Canvas(self, backpack, character, base, master = None):
        global local_backpack
        global local_character
        global local_base
        #Syncing up backpack, character, base
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
        #looking through backpack to see if character is carrying a laundry key
        unlocked = local_backpack.inPack('laundry key')
        #If the character is, populate the canvas with all the images, normally
        if unlocked != -1:
            #Background image
            self.bg_image = self.canvas.create_image(0, 0, image = self.unlocked_background_image, anchor = NW)
            #Room name on the double doors
            self.room_name = self.canvas.create_text(232, 446, fill = 'blue', text = "LAUN", font = ('Helvetica', 9, 'bold'), anchor = 'c')  
            self.room_name2 = self.canvas.create_text(260, 446, fill = 'blue', text = "DRY", font = ('Helvetica', 9, 'bold'), anchor = 'c')  
            #Populating canvas: placing suits of armor behind the character and all other objects in front
            for item in self.objects:
                if item.getVisibility() and item.getName().__contains__('suit of armor'):
                    self.object_images.append(self.canvas.create_image(item.getX(), 
                        item.getY(), 
                        image = item.getPhotoImage(), 
                        anchor = 'c', 
                        tags = (item.getTag())))
            #Character image
            self.image = self.canvas.create_image(250, 250, image=self.character, anchor='c')
            for item in self.objects:
                if item.getVisibility() and not item.getName().__contains__('suit of armor'):
                    self.object_images.append(self.canvas.create_image(item.getX(), 
                        item.getY(), 
                        image = item.getPhotoImage(), 
                        anchor = 'c', 
                        tags = (item.getTag())))
        else:
            #If the character is not carrying a laundry_key:
            #only create the faded-out background image, the room label, the character_image, and the alert label
            self.bg_image = self.canvas.create_image(0, 0, image = self.locked_background_image, anchor = NW)
            self.room_name = self.canvas.create_text(232, 446, fill = 'blue', text = "LAUN", font = ('Helvetica', 9, 'bold'), anchor = 'c')  
            self.room_name2 = self.canvas.create_text(260, 446, fill = 'blue', text = "DRY", font = ('Helvetica', 9, 'bold'), anchor = 'c')    
            self.image = self.canvas.create_image(250, 250, image=self.character, anchor='c')
            self.alert_label = Label(master, text = "You must have a laundry key to access this room")
            self.alert_label.place(relx = 0.5, rely = .35, anchor = CENTER)
            
        #Initializing Buttons so that they can be withdrawn later
        #Button used to pick up objects
        self.pickup_btn = Button(master, text = "pick up", state = DISABLED, command = lambda: self.pickUpObject(self.canvas))
        self.pickup_btn.place(relx = 0.7, rely = 0.9, relwidth = 0.25, relheight = 0.05)
        #Button used to consume objects
        self.consume_btn = Button(master, text = "consume", state = DISABLED, command = lambda: self.consumeObject())
        self.consume_btn.place(relx = 0.7, rely = 0.82, relwidth = 0.25, relheight = 0.05)
        #Button used to wash the armor
        self.wash_btn = Button(master, text = 'wash armor', state = DISABLED, command = lambda: self.washArmor())
        self.wash_btn.place(relx = 0.7, rely = 0.74, relwidth = 0.25, relheight = 0.05)
        #Labels on the three washing machines
        self.label1 = Label(master, text = "In use")
        self.label2 = Label(master, text = "In use")
        self.label3 = Label(master, text = "In use")

    def washArmor(self):
        global washing_machine_1
        global washing_machine_2
        global washing_machine_3
        global active_machine

        #if a suit of armor has been picked up by the player
        if local_backpack.inPack('suit of armor') != -1 and active_machine != -1:
            #removing the suit of armor from the pack
            removed = local_backpack.removeFromPack(local_backpack.inPack('suit of armor'))
            #getting location for stashing it while it is being washed
            new_loc = self.wash_locations[active_machine]
            #Creating new object that will be hidden within the canvas at the washing machine location
            self.objects.append(InteractiveItem(new_loc[0]-10, new_loc[0]+10, new_loc[1]-10, new_loc[1]+10,
                'suit of armor',
                'src/RESIZED_Armor_35x45.png', 
                new_loc[0], new_loc[1],
                'backpackIconFiles/armor.png',
                'pickupable',
                False,
                (removed.getTag()),
                0, 30))
            self.wash_btn.config(state = DISABLED)
            #Conditions for each of the three washing machines
            if active_machine == 0:
                #set 10 second timer
                washing_machine_1 = time.time() + 10
                #set label text
                self.label1.config(text = 'In Use: 10')
                #place the label
                self.label1.place(relx = self.label_locs[0][0], rely = self.label_locs[0][1])
                #set the washing machine to be running
                self.machines[0].setState(True)
                #set the index of the armor within the washing machine in the washMachine object
                self.machines[0].setIndex(len(self.objects) - 1)
            elif active_machine == 1:
                #See comments above
                washing_machine_2 = time.time() + 10
                self.label2.config(text = 'In Use: 10')
                self.label2.place(relx = self.label_locs[1][0], rely = self.label_locs[1][1])
                self.machines[1].setState(True)
                self.machines[1].setIndex(len(self.objects) - 1)
            elif active_machine == 2:
                #See comments above
                washing_machine_3 = time.time() + 10
                self.label3.config(text = 'In Use: 10')
                self.label3.place(relx = self.label_locs[2][0], rely = self.label_locs[2][1])
                self.machines[2].setState(True)
                self.machines[2].setIndex(len(self.objects) - 1)

    def updateLabels(self):
        global washing_machine_1
        global washing_machine_2
        global washing_machine_3

        #Make labels disappear if the washing machines are done
        try:
            #If the first washing machine timer has run out
            if time.time() > washing_machine_1:
                #delete the label and set the washing machine's state to being open
                self.label1.place_forget()
                self.machines[0].setState(False)
                #get the suit of armor object's index in the self.objects list
                armor_index = self.machines[0].getIndex()
                print("Suit of armor's index in self.objects: ", armor_index)
                #make that suit of armor visible
                self.objects[armor_index].toggleVisible()
                #Change the suit of armor's type to 'consumable'
                self.objects[armor_index].setType('consumable')
                #Re-add it back onto the canvas
                self.object_images.append(self.canvas.create_image(self.objects[armor_index].getX(), 
                    self.objects[armor_index].getY(), 
                    image = self.objects[armor_index].getPhotoImage(), 
                    anchor = 'c',
                    tags = (self.objects[armor_index].getTag())))
            else:
                #If the timer is not finished, configure the label with the remaining time
                self.label1.config(text = "In Use: " + str(int(washing_machine_1 - time.time())))
        except:
            pass
        try:
            #see comments above
            if time.time() > washing_machine_2:
                self.label2.place_forget()
                self.machines[1].setState(False)
                armor_index = self.machines[1].getIndex()
                print("Suit of armor's index in self.objects: ", armor_index)
                self.objects[armor_index].toggleVisible()
                self.objects[armor_index].setType('consumable')
                self.object_images.append(self.canvas.create_image(self.objects[armor_index].getX(), 
                    self.objects[armor_index].getY(), 
                    image = self.objects[armor_index].getPhotoImage(), 
                    anchor = 'c',
                    tags = (self.objects[armor_index].getTag())))
            else:
                self.label2.config(text = "In Use: " + str(int(washing_machine_2 - time.time())))
        except:
            pass
        try:
            #see comments above
            if time.time() > washing_machine_3:
                self.label3.place_forget()
                self.machines[2].setState(False)
                armor_index = self.machines[2].getIndex()
                print("Suit of armor's index in self.objects: ", armor_index)
                self.objects[armor_index].toggleVisible()
                self.objects[armor_index].setType('consumable')
                self.object_images.append(self.canvas.create_image(self.objects[armor_index].getX(), 
                    self.objects[armor_index].getY(), 
                    image = self.objects[armor_index].getPhotoImage(), 
                    anchor = 'c',
                    tags = (self.objects[armor_index].getTag())))
            else:
                self.label3.config(text = "In Use: " + str(int(washing_machine_3 - time.time())))
        except:
            pass

    #Method for checking the proximity of the character to washing machines in the room, marked by pressure plates
    def checkMachineProx(self):
        global active_machine
        #getting character's position
        character_x, character_y = (self.methods.__getattribute__('character_coordX'), self.methods.__getattribute__('character_coordY'))
        #checking the pressure plates
        n = 0
        for plate in self.plates:
            #Getting bounds of detection for the plates
            xBound, yBound = plate.getXBounds(), plate.getYBounds()
            #If the character is within the bounds and the plate is available and the backpack contains a suit of armor
            if character_x > xBound[0] and character_x < xBound[1] and character_y > yBound[0] and character_y < yBound[1] and plate.getAvailability() and local_backpack.inPack('suit of armor') != -1:
                #make the wash button available
                self.wash_btn.config(state = NORMAL)
                #set the washing machine that the character is standing on to the list index
                active_machine = n
                return n
            #increment n
            n += 1
        #if no washing machine is being triggered, set the active machine to -1
        active_machine = -1
        #disable the wash button
        self.wash_btn.config(state = DISABLED)

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
        self.methods.dropObject(dropped_object, local_backpack, self.canvas)

    def getCommonObject(self):
        return self.methods

    def deleteCommon(self):
        del self.methods


class WashMachine:
    def __init__(self, occupied, armor_index):
        self.occupied = occupied
        #This attribute describes the index in the self.objects list where the armor that is in the washing machine is located
        self.armor_index = armor_index
    #returns whether the washing machine is occupied or not
    def getState(self):
        return self.occupied
    #Toggle the occupied state of the washing machine
    def toggleState(self):
        if self.occupied:
            self.occupioed = False
        else:
            self.occupied = True

        return self.occupied
    #Set the occupied state of the washing machine
    def setState(self, state):
        self.occupied = state

        return self.occupied
    #get the index in the self.objects list where the armor is
    def getIndex(self):
        return self.armor_index
    #Set the index in the self.objects list where the armor is
    def setIndex(self, index):
        self.armor_index = index
        return self.armor_index