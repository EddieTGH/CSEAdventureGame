"""
AG2021_1 CSE Choose Your Own Adventure
Group Members: Edmond, Shashwat, and Esben
Date: March 15, 2020
File task description: medbay.py creates the canvas that will house the background image and all of the interactive objects in the medbay room
that can be accessed by the main character. It creates a canvas that is populated with a pixel art background and with consumables 
that increase the character's performance in the boss room
"""

#two global variables
'''
boss attack time
button cooldown

'''

from tkinter import *
from tkinter.ttk import * 
from PIL import Image
import os.path
from item import InteractiveItem
from commonmethods import CommonMethods
import time

global local_character
global local_backpack
global local_base
global healthbar_canvas
global bossHealth
global bossDPS 
global future
global attackCooldown
global bossAttackCooldown
global futureAttack
global futureBossAttack
global charAttack
global bossAttack

class BossRoom: 
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
  
         
        
        '''
        #Opening images and resizing them using PIL
        self.im = Image.open('Character.png').resize((200, 150))
        self.im2 = Image.open('Original Backgrounds/bossroom.png').resize((500, 500))
        self.im3 = Image.open('Original Backgrounds/darkboss.png').resize((500, 500))
        self.flashlight_img = Image.open('Images/Flashlight.png').resize((40, 40))
        self.fork_img = Image.open('src/fork.png').resize((30,30))
        self.spoon = Image.open('src/spoon.png').resize((30,30))
        self.syringe = Image.open('src/syringe.png').resize((50, 50))
        self.boss = Image.open('src/bossBear2.png').resize((300, 225))
        '''

        #Creating source directory for resized backgrounds
        self.directory = os.getcwd() # Use working directory if unspecified
        self.src_directory = os.path.join(self.directory, "src")
        try:
            os.mkdir(self.src_directory)
        except OSError:
            pass # if the directory already exists, proceed """
        

        #Creating filenames
        self.filename = os.path.join(self.src_directory, "RESIZED_Character.png")
        self.bg_filename = os.path.join(os.path.join(os.getcwd(), 'Original Backgrounds'), "RESIZED_BossRoom_background.png")
        self.locked_bg_filename = os.path.join(os.path.join(os.getcwd(), 'Original Backgrounds'), "RESIZED_Locked_BossRoom-BG.png")
        self.flash_filename = os.path.join(self.src_directory, 'RESIZED_Flashlight.png')
        self.fork_filename = os.path.join(self.src_directory, 'RESIZED_Fork.png')
        self.spoon_filename = os.path.join(self.src_directory, "RESIZED_Spoon.png")
        self.syringe_filename = os.path.join(self.src_directory, "RESIZED_syringe.png")
        self.bandage_filename = os.path.join(self.src_directory, 'RESIZED_bandage50x30.png')
        self.bossBear_filename = os.path.join(self.src_directory, 'RESIZED_boss.png')

        '''
        #Saving images to src
        self.im.save(self.filename, 'png')
        self.im2.save(self.bg_filename, 'png')
        self.im3.save(self.locked_bg_filename, 'png')
        self.flashlight_img.save(self.flash_filename, 'png')
        self.fork_img.save(self.fork_filename, 'png')
        self.spoon.save(self.spoon_filename, 'png')
        self.syringe.save(self.syringe_filename, 'png')
        self.boss.save(self.bossBear_filename, 'png')
    '''
        

        #Making photoImage objects for character and background
        self.unlocked_background_image = PhotoImage(file = self.bg_filename)
        self.locked_background_image = PhotoImage(file = self.locked_bg_filename)
        self.character = PhotoImage(file = self.filename)
        

        
        #Populating space with objects
        self.objects = []       #list of InteractiveItem objects
        self.object_images = [] #list of tkinter canvas images
        #adding an InteractiveItem object
        #self.objects.append(InteractiveItem(410, 430, 130, 150, 'flashlight', 'src/RESIZED_Flashlight.png', 420, 140, 'backpackIconFiles/flashlight.png', 'pickupable', True, 'flashlight'))
        #self.objects.append(InteractiveItem(190, 210, 190, 210, 'fork', 'src/RESIZED_Fork.png', 200, 200, 'backpackIconFiles/fork.png', 'pickupable', True, 'fork'))
        #self.objects.append(InteractiveItem(90, 110, 90, 110, 'spoon', 'src/RESIZED_Spoon.png', 100, 100, 'backpackIconFiles/spoon.png', 'pickupable', True, 'spoon'))
        #self.objects.append(InteractiveItem(300, 342.5, 130, 150, 'syringe', 'src/RESIZED_syringe.png', 325, 90, 'backpackIconFiles/syringe.png', 'consumable', True, 'syringe', 5))
        #self.objects.append(InteractiveItem(155, 182.5, 130, 150, 'bandage', 'src/RESIZED_bandage50x30.png', 172, 88, 'backpackIconFiles/bandage.png', 'consumable', True, 'bandage',5))
        #self.objects.append(InteractiveItem(250, 270, 140, 160, 'laundry key', 'src/RESIZED_laundry_key50x50.png', 260, 150, 'backpackIconFiles/laundry_key.png', 'pickupable', True, 'laundry_key'))
        self.objects.append(InteractiveItem(250, 270, 140, 160, 'bossBear', 'src/RESIZED_boss.png', 440, 300, 'backpackIconFiles/laundry_key.png', 'pickupable', True, 'bossBear'))

        
        #populating self.object_images with canvas images; this also puts them on the canvas; uses tags for selective deleting later
        #for item in self.objects:
        #    self.object_images.append(self.canvas.create_image(item.getX(), item.getY(), image = item.getPhotoImage(), anchor = 'c', tags = (item.getName())))

        #Initializing Buttons so that they can be withdrawn later
        #self.pickup_btn = Button(master, text = "pick up", state = DISABLED, command = lambda: self.methods.pickUpObject())
        #self.consume_btn = Button(master, text = "consume", state = DISABLED, command = lambda:self.methods.consumeObject())
        self.attack_btn = Button(master, text = "Attack", state = DISABLED, command = lambda: self.attack())
        self.battle_btn = Button(master, text = "Begin Battle", state = DISABLED, command = lambda: self.beginBattle())

        #Setting initial character coordinates
        self.character_coordX = 80                       
        self.character_coordY = 270
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
        global canvasBoss
        #Syncing up backpack, character, and base
        local_backpack = backpack
        local_character = character
        local_base = base

        # canvas object to create room 
        self.canvas = Canvas(master, height = 500, width = 500)
        self.canvas.pack()
        canvasBoss = self.canvas

        #Setting initial character coordinates
        self.character_coordX = 100                     
        self.character_coordY = 300
        self.methods.setCoordinates((100, 300))
        print(str(self.character_coordX)+", "+str(self.character_coordY))
        #looking through backpack to see if character is carrying a laundry key
        unlocked = local_backpack.inPack('flashlight')
        #If the character is, populate the canvas with all the images, normally
        #if unlocked != -1:
        if True:
            #Making the background image, the room label, and the character image
            self.bg_image = self.canvas.create_image(0, 0, image = self.unlocked_background_image, anchor = NW)
            #self.room_name = self.canvas.create_text(247, 446, fill = 'red', text = "MED BAY", font = ('Helvetica', 10, 'bold'), anchor = 'c')
            self.image = self.canvas.create_image(70,320, image=self.character, anchor='c', tags = 'char')
            #Populating the canvas with the associated images of InteractiveItem objects in the self.objects list
            for item in self.objects:
                if item.getVisibility():
                    self.object_images.append(self.canvas.create_image(item.getX(), 
                        item.getY(), 
                        image = item.getPhotoImage(), 
                        anchor = 'c', 
                        tags = (item.getTag())))
            self.createBossBar()
        
        else:
            #If the character is not carrying a laundry_key:
            #only create the faded-out background image, the room label, the character_image, and the alert label
            self.bg_image = self.canvas.create_image(0, 0, image = self.locked_background_image, anchor = NW)
            #self.room_name = self.canvas.create_text(232, 446, fill = 'blue', text = "LAUN", font = ('Helvetica', 9, 'bold'), anchor = 'c')  
            #self.room_name2 = self.canvas.create_text(260, 446, fill = 'blue', text = "DRY", font = ('Helvetica', 9, 'bold'), anchor = 'c')    
            self.image = self.canvas.create_image(250, 250, image=self.character, anchor='c')
            self.alert_label = Label(master, text = "You must have a flashlight to start the bossfight.")
            self.alert_label.place(relx = 0.5, rely = .35, anchor = CENTER)

        #Initializing Buttons
        #self.pickup_btn = Button(master, text = "pick up", state = DISABLED, command = lambda: self.pickUpObject(self.canvas))
        #self.pickup_btn.place(relx = 0.7, rely = 0.9, relwidth = 0.25, relheight = 0.05)
        #self.consume_btn = Button(master, text = "consume", state = DISABLED, command = lambda: self.consumeObject())
        #self.consume_btn.place(relx = 0.7, rely = 0.75, relwidth = 0.25, relheight = 0.05)
        self.attack_btn = Button(master, text = "Attack", state = DISABLED, command = lambda: self.attack())
        self.attack_btn.place(relx = 0.7, rely = 0.9, relwidth = 0.25, relheight = 0.05)
        self.battle_btn = Button(master, text = "Begin Battle and Consume (1) Flashlight", state = NORMAL, command = lambda: self.beginBattle())
        self.battle_btn.place(relx = 0.5, rely = 0.95, relwidth = 0.5, relheight = 0.05)

        self.dead_label = Label(self.master, text = "YOU DIED", font = ('Helvetica', 25))
        self.battleBegin_label = Label(self.master, text="The Battle Has Begun!", font = ('Helvetica', 25))
        self.gameSuccess_label = Label(self.master, text = "YOU WON!", font = ('Helvetica', 25))
        self.endurance_label = sLabel(self.master, text = "You Have No Endurance Left. You Can't Attack Anymore!", font = ('Helvetica', 25))
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
    
    def attack(self):
        global local_character
        global futureAttack
        global charAttack
        DPS = local_character.getDPS()
        local_character.changeEndurance(-10)
        local_character.updateStatCanvas()
        charAttack = True
        self.attack_btn.config(state = DISABLED)
        self.master.update()

        self.commenceAttack()
        self.finishAttack()
        self.updateBaseHealth(DPS)
        
        self.master.update()
        futureAttack = time.time() + 5
        charAttack = False

    def gameOverMessage(self):
        self.attack_btn.config(state = DISABLED)
        self.battle_btn.config(state = DISABLED)
        self.dead_label.place(relx = 0.5, rely = 0.15, anchor = 'c')
        self.bg_image = self.canvas.create_image(0, 0, image = self.locked_background_image, anchor = NW)
        self.master.update()
        

    def gameSuccessMessage(self):
        self.attack_btn.config(state = DISABLED)
        self.battle_btn.config(state = DISABLED)
        self.gameSuccess_label.place(relx = 0.5, rely = 0.15, anchor = 'c')
        self.master.update()

    def noEnduranceMessage(self):
        self.attack_btn.config(state = DISABLED)
        self.battle_btn.config(state = DISABLED)
        self.endurance_label.place(relx = 0.5, rely = 0.15, anchor = 'c')
        self.master.update()

    def getAttacked(self):
        global local_character
        global bossAttack
        bossDPS = -20
        armorValue = local_character.getArmor()
        actualDamageTaken = -20 + ((armorValue / 100) * 20)
        local_character.changeArmor(-10)
        bossAttack = True
        self.receiveAttack1()
        self.receiveAttack2()
        local_character.changeHealth(actualDamageTaken)
        local_character.updateStatCanvas()
        self.master.update()
        bossAttack = False

    def receiveAttack1(self):
        global future1
        x=-23
        for i in range (0,12):
            self.canvas.move(self.object_images[0],x,0)
            self.master.update()
            time.sleep(0.05)
        #self.canvas.delete('char')
        #self.image = self.canvas.create_image(370,320, image=self.character, anchor='c', tags = 'char1')
        future1 = time.time() + 1
        print('commencedone')

    def receiveAttack2(self):
        global future1
        while True:
            x=23
            if time.time() > future1:
                for i in range (0,12):
                    self.canvas.move(self.object_images[0],x,0)
                    self.master.update()
                    time.sleep(0.05)
                print('attackdone')

                #self.canvas.delete('char')
                #self.image = self.canvas.create_image(70,320, image=self.character, anchor='c', tags = 'char')
                break


    def commenceAttack(self):
        global future
        x=23
        for i in range (0,12):
            self.canvas.move(self.image,x,0)
            self.master.update()
            time.sleep(0.05)
        #self.canvas.delete('char')
        #self.image = self.canvas.create_image(370,320, image=self.character, anchor='c', tags = 'char1')
        future = time.time() + 1
        print('commencedone')

    

    def finishAttack(self):
        global future
        while True:
            x=-23
            if time.time() > future:
                for i in range (0,12):
                    self.canvas.move(self.image,x,0)
                    self.master.update()
                    time.sleep(0.05)
                print('attackdone')

                #self.canvas.delete('char')
                #self.image = self.canvas.create_image(70,320, image=self.character, anchor='c', tags = 'char')
                break
        
        
        '''
        canvasBoss.move(self.image, 200, 300) 
        self.image = self.canvas.create_image(70,320, image=self.character, anchor='c') '''
        
        

        
    def disablebuttons(self):
        self.battle_btn.config(state = DISABLED)
        #self.attack_btn.config(state = NORMAL)
        print('they should be disabled')
        

    def beginBattle(self):
        #begins battle and uses up one flashlight
        global local_backpack
        global attackCooldown
        global bossHealth
        global bossAttackCooldown
        global futureAttack
        global futureBossAttack
        global local_character
        global charAttack
        global bossAttack
        
        self.disablebuttons()
        self.battleBegin_label.place(relx = 0.5, rely = 0.15, anchor = 'c')
        self.master.update()
        time.sleep(2)
        self.battleBegin_label.place_forget()
        self.master.update()
        #index = local_backpack.inPack('flashlight')
        #local_backpack.removeFromPack(index)

        time.sleep(1)
        attackCooldown = 5
        bossAttackCooldown = 3 
        futureAttack = time.time() + attackCooldown
        futureBossAttack = time.time() + bossAttackCooldown
        charAttack = False
        bossAttack = True
        while True:
            if time.time() > futureAttack and bossAttack == False and local_character.getEndurance()>0:
                print('this should make button avail')
                self.attack_btn.config(state = NORMAL)
                self.master.update()
            if time.time() > futureBossAttack and charAttack == False:
                self.attack_btn.config(state = DISABLED)
                self.master.update()
                self.getAttacked()
                futureBossAttack = time.time() + bossAttackCooldown
                print('this should have the boss attack')
            time.sleep(0.5)
            if local_character.getHealth() == 0:
                self.gameOverMessage()
                break
            if bossHealth == 0:
                self.gameSuccessMessage()
                break
            if local_character.getEndurance() == 0:
                self.noEnduranceMessage()
       
            #print('1 iteration done')


    def createBossBar(self):
        global healthbar_canvas
        global bossHealth
        bossHealth = 100  
        #Create and place canvas for the base's health bar
        healthbar_canvas = Canvas(self.master, height = 25, width = 170, relief = GROOVE)
        healthbar_canvas.place(relx=.65, rely=.79)
        #text as a label
        healthbar_canvas.create_text(23, 14, text="Boss\nHealth", justify = CENTER)
        #Adding 5 hearts to the base's health bar
        heart = PhotoImage(file = os.path.join(os.path.join(os.getcwd(), 'src'), 'health_bar_heart.png'))
        self.master.heart = heart 
        healthbar_canvas.create_image(52, 5, image=heart, anchor='nw', tags = ('heart1'))
        healthbar_canvas.create_image(75, 5, image=heart, anchor='nw', tags = ('heart2'))
        healthbar_canvas.create_image(100, 5, image=heart, anchor='nw', tags = ('heart3'))
        healthbar_canvas.create_image(125, 5, image=heart, anchor='nw', tags = ('heart4'))
        healthbar_canvas.create_image(150, 5, image=heart, anchor='nw', tags = ('heart5'))

    def updateBaseHealth(self, DPS):
        global healthbar_canvas
        global bossHealth
        bossHealth = bossHealth - DPS
        print(bossHealth)
        #retrieve health value
        #delete hearts from the bar according to the health level of the base
        if bossHealth <= 80 and bossHealth > 60:
            healthbar_canvas.delete('heart1')
        elif bossHealth <= 60 and bossHealth > 40:
            try:
                healthbar_canvas.delete("heart2")
            except:
                pass
        elif bossHealth <= 40 and bossHealth > 20:
            try:
                healthbar_canvas.delete("heart3")
            except:
                pass
        elif bossHealth <= 20 and bossHealth > 0:
            try:
                healthbar_canvas.delete("heart4")
            except:
                pass
        elif bossHealth <= 0:
            try:
                healthbar_canvas.delete("heart5")
                print('the boss is defeated')
            except:
                pass