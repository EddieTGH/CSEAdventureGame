"""
AG2021_1 CSE Choose Your Own Adventure
Group Members: Edmond, Shashwat, and Esben
Date: March 7, 2020
File task description: failsafe.py hosts the root window, handles the movement of the display from room to room, and hosts the Character
and Backpack classes. It also hosts the 'back to hallway' and 'Open Backpack' buttons on the graphical user interface and provides the 
functions associated with those buttons.  
"""
from pygamePort_test_file import *
#from medbay import MedBayRoom
from cafeteria import CafeteriaRoom
from commandcenter import CommandRoom
#from laundry import LaundryRoom
from bossroom import BossRoom
from weaponsroom import WeaponsRoom
#from backgroundCanvas import BackgroundRoom
from item import InteractiveItem
from tkinter import *
from tkinter.ttk import * 
from PIL import Image, ImageTk
import os.path
import time

#Base class for defining the base object that will be passed among python files
class Base:
    def __init__(self, initialHealth, timeInterval, damageInterval):
        self.health = initialHealth
        self.timeInterval = timeInterval
        self.start_time = time.time()
        self.last_checked = time.time()
        self.damageInterval = damageInterval

    def getHealth(self):
        return self.health

    #method for updating the base's health. Also calls function to update the baseHealth canvas on the screen
    def updateHealth(self):
        totalduration = (time.time() - self.last_checked) // self.timeInterval
        if totalduration > 0:
            self.last_checked = time.time()
            self.health -= totalduration * self.damageInterval
        updateBaseHealth()
        print(self.health)
#Backpack class for defining the backpack object that will be passed among python files
class Backpack():
    def __init__(self, size):
        self.size = size
        self.pack = []

    def getItems(self):
        return self.pack

    def getSize(self):
        return self.size

    #item is a string that correlates to the 'name' attribute of the InteractiveItem objects in the pack
    def inPack(self, item):
        names = []
        for thing in self.pack:
            names.append(thing.getName())
        try:
            return names.index(item)
        except:
            return -1

    def addToPack(self, item):
        self.pack.append(item)

    #accepts either integer or InteractiveItem values; removes object at the specified index
    def removeFromPack(self, item):
        if type(item) == int:   
            removed = self.pack.pop(item)
            return removed
        else:
            delete_index = self.pack.index(item)
            self.pack.pop(delete_index)
            
#Character class for defining the character for the root
class Character():
    def __init__(self, initialX, initialY, image, initialHealth, initialArmor, initialEndurance, initialDPS, maxHealth):
        self.X = initialX
        self.Y = initialY
        self.image = image
        self.health = initialHealth
        self.armor = initialArmor
        self.endurance = initialEndurance
        self.dps = initialDPS
        self.maxHealth = maxHealth

    def getHealth(self):
        return self.health

    def changeHealth(self, increment):
        self.health += increment
        if self.health > self.maxHealth:
            self.health = self.maxHealth
        elif self.health < 0:
            self.health = 0
        return self.health

    def getArmor(self):
        return self.armor

    def changeArmor(self, increment):
        self.armor += increment
        if self.armor < 0:
            self.armor = 0
        return self.armor

    def getEndurance(self):
        return self.endurance

    def changeEndurance(self, increment):
        maxEndurance = 100
        self.endurance += increment
        if self.endurance > maxEndurance:
            self.endurance = maxEndurance
        elif self.endurance < 0:
            self.endurance = 0
        return self.endurance

    def getDPS(self):
        return self.dps

    def changeDPS(self, increment):
        self.dps += increment
        return self.dps

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

    def getImage(self):
        return self.image 

    def setX(self, newX):
        self.X = newX
        return self.X

    def setY(self, newY):
        self.Y = newY
        return self.Y

    def changeX(self, increment):
        self.X += increment
        return self.X

    def changeY(self, increment):
        self.Y += increment
        return self.Y

    def updateStatCanvas(self):
        updateCharStats()
#Global variables for buttons on home page
global canvas
global medbay_btn
global cafeteria_btn
global commandCenter_btn
global laundry_btn 
global bossroom_btn
global weaponsRoom_btn
#Globals for singleton backpack, character, and base objects
global k
global local_backpack
global local_character
global local_base
#Globals for stat canvases on all screens
global healthbar_canvas
global character_stat_canvas
#Globals for text in the character_stat_canvas
global health_text
global armor_text
global endurance_text
global dps_text
#Icons for health, armor, dps, and endurance
global heart
global shield
global stamina
global sword
#Globals for all the room objects and the backpack window
global backpack_window
global med_bay_room
global cafeteria_room
global command_center
global laundry_room
global boss_room
global weapons_room
global medBayRoom
global itemsListMedBay
global itemsListCafeteria
global itemsListLaundry
global itemsListBoss


#root initialization; resizable option set to 0 so that the game window remains the same size
root = Tk()
root.resizable(0,0)

#creating one backpack object and character object
itemsListMedBay = [True, True, True, True, True, True]
itemsListCafeteria = [True, True, True, True]
itemsListLaundry = [True, True, True, True, True, True, True]
itemsListBoss = []
local_backpack = Backpack(9)
local_base = Base(100, 10, 1)
local_character = Character(0.5, 0.5, 'Character.png', 50, 10, 30, 5, 100)

#med_bay_room = MedBayRoom(local_character, local_backpack, local_base, root)
#cafeteria_room = CafeteriaRoom(local_character, local_backpack, local_base, root)
#command_center = CommandRoom(local_character, local_backpack, local_base, root)
#laundry_room = LaundryRoom(local_character, local_backpack, local_base, root)
boss_room = BossRoom(local_character, local_backpack, local_base, root)
#weapons_room = WeaponsRoom(local_character, local_backpack, local_base, root)'''
medBayRoom = medBayRoom_pygame(itemsListMedBay)
cafeteriaRoom =cafeteriaRoom_pygame(itemsListCafeteria)
laundryRoom = laundryRoom_pygame(itemsListLaundry)
bossRoom = bossRoom_pygame(itemsListBoss)

heart = PhotoImage(file = os.path.join(os.path.join(os.getcwd(), 'src'), 'health_bar_heart.png'))
shield = PhotoImage(file = os.path.join(os.path.join(os.getcwd(), 'src'), 'RESIZED_character_bar_shield.png'))
stamina = PhotoImage(file = os.path.join(os.path.join(os.getcwd(), 'src'), 'RESIZED_character_lightning.png'))
sword = PhotoImage(file = os.path.join(os.path.join(os.getcwd(), 'src'), 'RESIZED_character_sword.png'))

def updateBaseHealth():
    global local_base
    global healthbar_canvas
    #retrieve health value
    health = local_base.getHealth()
    #delete hearts from the bar according to the health level of the base
    if health <= 80 and health > 60:
        healthbar_canvas.delete('heart1')
    elif health <= 60 and health > 40:
        try:
            healthbar_canvas.delete("heart2")
        except:
            pass
    elif health <= 40 and health > 20:
        try:
            healthbar_canvas.delete("heart3")
        except:
            pass
    elif health <= 20 and health > 0:
        try:
            healthbar_canvas.delete("heart4")
        except:
            pass
    elif health <= 0:
        try:
            healthbar_canvas.delete("heart5")
        except:
            pass

def updateCharStats():
    global local_character
    global character_stat_canvas
    global health_text
    global armor_text
    global endurance_text
    global dps_text
    #Update the labels with the correct character stats using the globals
    character_stat_canvas.itemconfig(health_text, text = str(local_character.getHealth()) + "/" + str(local_character.__getattribute__('maxHealth')))
    character_stat_canvas.itemconfig(armor_text, text = str(local_character.getArmor()))
    character_stat_canvas.itemconfig(endurance_text, text = str(local_character.getEndurance()))
    character_stat_canvas.itemconfig(dps_text, text = str(local_character.getDPS()))

def createWidgets():
    global canvas
    global root

    global medbay_btn
    global cafeteria_btn
    global commandCenter_btn
    global laundry_btn 
    global bossroom_btn
    global weaponsRoom_btn

    #re-initializing canvas for buttons on home page
    canvas = Canvas(root, height = 500, width = 500)
    canvas.pack()

    bg_image = PhotoImage(file = os.path.join(os.path.join(os.getcwd(), 'Original Backgrounds'), "RESIZED_Hallway_500x500.png"))
    root.bg_image = bg_image
    background = canvas.create_image(250, 250, image = bg_image, anchor = 'c', tag = ('bg_image'))

    #button that brings screen to medbay
    medbay_btn = Button(canvas, text = "to med bay", command = lambda: openMedBay())
    #medbay_btn.place(relx = 0.166666, rely = 0.1, relwidth = 0.333333, relheight = 0.2, anchor = 'c')
    medbay_btn_window = canvas.create_window(145, 80, anchor = CENTER, window = medbay_btn)
    #button that brings screen to the cafeteria
    cafeteria_btn = Button(canvas, text = "to cafeteria", command = lambda: openCafeteria())
    #cafeteria_btn.place(relx = 0.5, rely = 0.1, relwidth = 0.333333, relheight = 0.2, anchor = 'c')
    cafeteria_btn_window = canvas.create_window(360, 80, anchor = CENTER, window = cafeteria_btn)
    #button that brings screen to the command center
    commandCenter_btn = Button(canvas, text = "to command center", command = lambda: openCommand())
    #commandCenter_btn.place(relx = 0.833333, rely = 0.1, relwidth = 0.333333, relheight = 0.2, anchor = 'c')
    command_window = canvas.create_window(400, 250, anchor = CENTER, window = commandCenter_btn)
    #button that brings screen to the laundry room
    laundry_btn = Button(canvas, text = "to laundry room", command = lambda: openLaundry())
    #laundry_btn.place(relx = 0.166666, rely = 0.3, relwidth = 0.333333, relheight = 0.2, anchor = 'c')
    laundry_window = canvas.create_window(145, 415, anchor = CENTER, window = laundry_btn)
    #button that brings screen to the boss room
    bossroom_btn = Button(canvas, text = "to boss room", command = lambda: openBoss())
    #bossroom_btn.place(relx = 0.5, rely = 0.3, relwidth = 0.333333, relheight = 0.2, anchor = 'c')
    boss_window = canvas.create_window(82, 250, anchor = CENTER, window = bossroom_btn)
    #button that brings screen to the weapons room
    weaponsRoom_btn = Button(canvas, text = 'to weapons room', command = lambda: openWeapons())
    #weaponsRoom_btn.place(relx = 0.833333, rely = 0.3, relwidth = 0.333333, relheight = 0.2, anchor = 'c')
    weapons_window = canvas.create_window(360, 415, anchor = CENTER, window = weaponsRoom_btn)
#calling create widgets function for home page
createWidgets()

#   Creates the universal GUI elements for every room
#   Elements:
#       Backpack Button, Hallway button, 'pick up' button, 'consume' button, Base Health canvas, Character Stats Canvas, and keybinds for movement
def createGUI(room, root):
    global healthbar_canvas
    global character_stat_canvas
    global health_text
    global armor_text
    global endurance_text
    global dps_text
    global heart
    global shield
    global stamina
    global sword
    #buttons for navigating back to the navigation page and for opening the backpack
    hallway_btn = Button(root, text = 'To Hallway', command = lambda: backToMain()).place(relx = 0.04, rely = 0.03)
    backpack_btn = Button(root, text = "Open Backpack", command = lambda: openBackpack(room)).place(relx = 0.78, rely = 0.03)
    
    #Create and place canvas for the base's health bar
    healthbar_canvas = Canvas(root, height = 25, width = 170, relief = GROOVE)
    healthbar_canvas.place(relx=.019, rely=.89)
    #text as a label
    healthbar_canvas.create_text(23, 14, text="Base\nHealth", justify = CENTER)
    #Adding 5 hearts to the base's health bar
    healthbar_canvas.create_image(52, 5, image=heart, anchor='nw', tags = ('heart1'))
    healthbar_canvas.create_image(75, 5, image=heart, anchor='nw', tags = ('heart2'))
    healthbar_canvas.create_image(100, 5, image=heart, anchor='nw', tags = ('heart3'))
    healthbar_canvas.create_image(125, 5, image=heart, anchor='nw', tags = ('heart4'))
    healthbar_canvas.create_image(150, 5, image=heart, anchor='nw', tags = ('heart5'))
    #Creating character statistics canvas and placing it
    character_stat_canvas = Canvas(root, height = 25, width = 220)
    character_stat_canvas.place(relx = 0.5, rely = 0.05, anchor = 'c')

    #Placing texts showing armor level, health level, endurance level, and damage per second level
    armor_text = character_stat_canvas.create_text(115, 14, text = str(local_character.getArmor()))

    health_text = character_stat_canvas.create_text(49, 14, text = str(local_character.getHealth()) + "/" + str(local_character.__getattribute__('maxHealth')))

    endurance_text = character_stat_canvas.create_text(160, 14, text = str(local_character.getEndurance()))

    dps_text = character_stat_canvas.create_text(210, 14, text = str(local_character.getDPS()))
    #Create icons for health, armor, endurance, and dps
    character_stat_canvas.create_image(95, 14, image = shield, anchor = 'c', tags = ('character_armor'))
    character_stat_canvas.create_image(142, 12, image = stamina, anchor = 'c', tags = ('character_stamina'))
    character_stat_canvas.create_image(17, 14, image = heart, anchor = 'c', tags = ('character_hp'))
    character_stat_canvas.create_image(190, 14, image = sword, anchor = 'c', tags = ('character_sword'))

    #key binds for movement within the medbay room
    root.bind("<KeyPress-Left>", lambda e: room.left(e)) 
    root.bind("<KeyPress-Right>", lambda e: room.right(e)) 
    root.bind("<KeyPress-Up>", lambda e: room.up(e)) 
    root.bind("<KeyPress-Down>", lambda e: room.down(e))
    #Update the base's health and the character stat bar
    updateBaseHealth()
    updateCharStats()

#function that brings the screen back to the main navigation window
def backToMain():
    global canvas
    global root
    global local_backpack
    print("Back in the main file: ", local_backpack.getItems())
    #destroying all widgets in the root and remaking them
    for child in root.winfo_children():
        child.destroy()
    #Remake the hallway
    root.iconify()
    

#Function that brings screen to medbay
def openMedBay():
    global cafeteriaRoom
    global itemsListMedBay
    global local_character
    global local_backpack
    global local_base
    '''
    global root
    global canvas
    global local_backpack
    global local_base
    global local_character
    global med_bay_room
    #destroy buttons in the canvas
    for child in canvas.winfo_children():
        child.destroy()
    #destroy canvas
    canvas.destroy()
    #create a MedBayRoom object which creates a canvas with unique background and interactive objects in it
    med_bay_room.Render_Canvas(local_backpack, local_character, local_base, root)
    createGUI(med_bay_room, root)

    #cycle this function
    root.mainloop()
    #sync up the universal objects
    (local_backpack, local_character, local_base) = med_bay_room.getCommonObject().sendObjects()
    '''
    root.wm_state('withdrawn')
    itemsListMedBay, local_character, local_backpack = medBayRoom.renderGame(local_character, local_backpack, local_base)
    root.wm_state('normal')
    print(local_backpack.getItems())

#Function that brings screen to the command center
def openCommand():
    global root
    global medbay_btn
    global cafeteria_btn
    global canvas
    cafeteria_btn['state'] = DISABLED
    medbay_btn.destroy()
    medbay_btn = Button(canvas, text = 'to hallway', command = lambda: backToMain()).pack()
    room = CommandRoom(root)
    root.bind("<KeyPress-Left>", lambda e: room.left(e)) 
    root.bind("<KeyPress-Right>", lambda e: room.right(e)) 
    root.bind("<KeyPress-Up>", lambda e: room.up(e)) 
    root.bind("<KeyPress-Down>", lambda e: room.down(e))

    root.mainloop()
    cafeteria_btn['state'] = NORMAL
    medbay_btn.destroy()
    del room
    

#Function that brings screen to the cafeteria
def openCafeteria():
    global cafeteriaRoom
    global itemsListCafeteria
    global local_character
    global local_backpack
    global local_base
    '''global root
    global canvas
    global local_backpack
    global local_base
    global local_character
    global cafeteria_room

    #destroy buttons in the canvas
    for child in canvas.winfo_children():
        child.destroy()
    #destroy canvas
    canvas.destroy()
    #create a MedBayRoom object which creates a canvas with unique background and interactive objects in it
    cafeteria_room.Render_Canvas(local_backpack, local_character, local_base, root)
    createGUI(cafeteria_room, root)

    \'''
    #key binds for movement within the boss room
    root.bind("<KeyPress-Left>", lambda e: room.left(e)) 
    root.bind("<KeyPress-Right>", lambda e: room.right(e)) 
    root.bind("<KeyPress-Up>", lambda e: room.up(e)) 
    root.bind("<KeyPress-Down>", lambda e: room.down(e)) \'''

    #cycle this function
    root.mainloop()
    #sync up the universal objects
    (local_backpack, local_character, local_base) = cafeteria_room.getCommonObject().sendObjects()'''
    
    root.wm_state('withdrawn')
    itemsListCafeteria, local_character, local_backpack = cafeteriaRoom.renderGame(local_character, local_backpack, local_base)
    root.wm_state('normal')
    print(local_backpack.getItems())
    


#Function that brings screen to laundry room
def openLaundry():
    #global root
    #global canvas

    global laundryRoom
    global itemsListLaundry
    global local_character
    global local_backpack
    global local_base
    '''global laundry_room

    #destroy buttons in the canvas
    for child in canvas.winfo_children():
        child.destroy()
    #destroy canvas
    canvas.destroy()
    #create a MedBayRoom object which creates a canvas with unique background and interactive objects in it
    laundry_room.Render_Canvas(local_backpack, local_character, local_base, root)
    createGUI(laundry_room, root)
    #Since several aspects of the laundry room need to be updated at once, these are nested functions designed to bind one key to multiple updating functions
    def machine_check_l(e):
        global laundry_room
        laundry_room.left(e)
        laundry_room.checkMachineProx()
        laundry_room.updateLabels()
    def machine_check_r(e):
        global laundry_room
        laundry_room.right(e)
        laundry_room.checkMachineProx()
        laundry_room.updateLabels()
    def machine_check_u(e):
        global laundry_room
        laundry_room.up(e)
        laundry_room.checkMachineProx()
        laundry_room.updateLabels()
    def machine_check_d(e):
        global laundry_room
        laundry_room.down(e)
        laundry_room.checkMachineProx()
        laundry_room.updateLabels()

    #key binds for movement within the laundry room
    root.bind("<KeyPress-Left>", lambda e: machine_check_l(e)) 
    root.bind("<KeyPress-Right>", lambda e: machine_check_r(e)) 
    root.bind("<KeyPress-Up>", lambda e: machine_check_u(e)) 
    root.bind("<KeyPress-Down>", lambda e: machine_check_d(e))

    #cycle this function
    root.mainloop()
    (local_backpack, local_character, local_base) = laundry_room.getCommonObject().sendObjects()'''
    root.wm_state('withdrawn')
    itemsListLaundry, local_character, local_backpack = laundryRoom.renderGame(local_character, local_backpack, local_base)
    root.wm_state('normal')
    print(local_backpack.getItems())

#Function that brings screen to the boss room
def openBoss2():
    global bossRoom
    global itemsListBoss
    global local_character
    global local_backpack
    global local_base

    '''
    global root
    global canvas
    global local_backpack
    global local_base
    global local_character
    global boss_room

    #destroy buttons in the canvas
    for child in canvas.winfo_children():
        child.destroy()
    #destroy canvas
    canvas.destroy()
    #create a MedBayRoom object which creates a canvas with unique background and interactive objects in it
    boss_room.Render_Canvas(local_backpack, local_character, local_base, root)
    createGUI(boss_room, root)


    #cycle this function
    root.mainloop()
    #sync up the universal objects
    (local_backpack, local_character, local_base) = boss_room.getCommonObject().sendObjects()

'''
    root.wm_state('withdrawn')
    itemsListBoss, local_character, local_backpack = bossRoom.renderGame(local_character, local_backpack, local_base)
    root.wm_state('normal')
    print(local_backpack.getItems())


#Function that brings screen to the boss room
def openBoss():
    global root
    global canvas
    global local_backpack
    global local_base
    global local_character
    global boss_room

    #destroy buttons in the canvas
    for child in canvas.winfo_children():
        child.destroy()
    #destroy canvas
    canvas.destroy()
    #create a MedBayRoom object which creates a canvas with unique background and interactive objects in it
    boss_room.Render_Canvas(local_backpack, local_character, local_base, root)
    createGUI(boss_room, root)


    #cycle this function
    root.mainloop()
    #sync up the universal objects
    (local_backpack, local_character, local_base) = boss_room.getCommonObject().sendObjects()

'''
    root.wm_state('withdrawn')
    itemsListBoss, local_character, local_backpack = bossRoom.renderGame(local_character, local_backpack, local_base)
    root.wm_state('normal')
    print(local_backpack.getItems()) '''

#Function that brings screen to the weapons room
def openWeapons():
    global root
    global medbay_btn
    global cafeteria_btn
    global canvas
    cafeteria_btn['state'] = DISABLED
    medbay_btn.destroy()
    medbay_btn = Button(canvas, text = 'to hallway', command = lambda: backToMain()).pack()
    room = WeaponsRoom(root)
    root.bind("<KeyPress-Left>", lambda e: room.left(e)) 
    root.bind("<KeyPress-Right>", lambda e: room.right(e)) 
    root.bind("<KeyPress-Up>", lambda e: room.up(e)) 
    root.bind("<KeyPress-Down>", lambda e: room.down(e))

    root.mainloop()
    cafeteria_btn['state'] = NORMAL
    medbay_btn.destroy()
    del room

#function that opens the backpack Toplevel window
def openBackpack(room):
    #declare globals that will be used
    global local_backpack
    global backpack_window
    #Get the backpack, character, and base objects from the current active room
    #Tuple format: (backpack, character, base)
    temp = room.getCommonObject().sendObjects()
    local_backpack = temp[1]    #Sync up the backpack
    backpackContents = local_backpack.getItems()       #returns a list of InteractiveItem objects
    backpack_window = Canvas(root)      #Make a new canvas to display the items in the backpack
    backpack_window.place(relwidth = 0.8, relheight = 0.8, relx = 0.5, rely = .5, anchor = 'c')

    checkButtonList = []

    def makeWindow():
        global backpack_window
        #Destroy any previous instances of backpack_window
        backpack_window.destroy()
        #make a new backpack_window
        backpack_window = Canvas(root)
        backpack_window.place(relwidth = 0.8, relheight = 0.8, relx = 0.5, rely = .5, anchor = 'c')
        #Creating button to get rid of backpack canvas
        button = Button(root, text = 'Quit', command = backpack_window.destroy)
        button.configure(width = 10)
        #Creating a button on the backpack canvas
        button_window = backpack_window.create_window(10, 10, anchor = NW, window = button)
        #Button for dropping selected objects
        drop_btn = Button(root, text = "Drop Object(s)", command = lambda: processCheckButton())
        drop_btn.configure(width = 15)
        #Adding button to backpack canvas
        drop_btn_window = backpack_window.create_window(285, 365, anchor = NW, window = drop_btn)
        #positions of labels that will hold the item icons on the canvas
        positions = [
            (0.25, 0.25),
            (0.5, 0.25),
            (0.75, 0.25),
            (0.25, 0.5),
            (0.5, 0.5),
            (0.75, 0.5),
            (0.25, 0.75),
            (0.5, 0.75),
            (0.75, 0.75)
        ]
        #Make 9 Labels for holding objects
        for i in range (0,9):
            try:
                my_label = Label(backpack_window, 
                    text = str(backpackContents[i].getName()), image=backpackContents[i].getIconImage(), compound = 'top').place(relx = positions[i][0], rely = positions[i][1], anchor = 'c')
            except:
                pass
        #Positions of checkboxes corresponding to the various objects
        checkButtonPositions = [
            (0, 0),
            (0.25, 0),
            (0.5, 0),
            (0, 0.25),
            (0.25, 0.25),
            (0.5, 0.25),
            (0, 0.5),
            (0.25, 0.5),
            (0.5, 0.5)
        ]
        #make checkboxes
        for i in range(9):
            var = IntVar()
            var.set(0)
            c = Checkbutton(backpack_window, variable=var, onvalue=1, offvalue=0)
            c.place(relx = checkButtonPositions[i][0] + 0.23, rely = checkButtonPositions[i][1] + 0.1, anchor = NW)
            c.var = var
            checkButtonList.append((c, var))
        
    makeWindow()

    #iterate through checkboxes
    def processCheckButton():
        
        for i in range(9):
            #If the checkbox is checked
            if checkButtonList[i][1].get() == 1:
                #extract the object from the list of backpack objects that is going to be dropped
                dropped_object = backpackContents[i]
                #remove that object from the backpack
                local_backpack.removeFromPack(backpackContents[i])
                print('Object dropped from backpack')
                #destroy the window
                backpack_window.destroy()
                #remake it to update it
                makeWindow()
                #call the dropObject method that belongs to the currently active room to initiate changes to the attributes of the room
                room.dropObject(dropped_object, local_backpack)
root.mainloop()