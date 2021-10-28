"""
CSE Choose your own Adventure
Team members: Esben Nielsen, Shashwat Tewari, Edmond Niu
Date: 3/22/2021
pygamePort_modules.py
Task Description:
Hosts classes for several different aspects of the pygame:
    InteractiveItem2 handles methods associated with items in the game that the player can pick up or consume
    BackpackCreator handles the methods associated with the backpack display and dropping objects
    renderGUI renders the GUI over the player and background
    pygameMovement handles the movement of the character following player keyboard presses
    makeNewAnimations creates the animations associated with character movement and performs methods to
        images that are passed into its methods
"""
#Import necessary modules
from PIL import Image
import PIL
import os.path
import matplotlib.pyplot as plt
import pygame
#Class to handle methods associated with picking up and consuming objects
class InteractiveItem2():
    def __init__(self, image, pos, consumable):
        self.image = image
        self.pos = pos
        self.consumable = consumable
    #Check for equality
    def equals(self, otherItem):
        if self.image == otherItem.getImage():
            return True
    #Search in backpack for an item
    def simpleSearch(self, backpackItems):
        self.backpackItems = backpackItems
        for i in range(len(backpackItems)):
            if self.equals(backpackItems[i]):
                return True
        return False
    #return image filename
    def getImage(self):
        return self.image
    #get position
    def getPos(self):
        return self.pos
    #get icon image
    def getIcon(self):
        for filename in os.listdir(os.getcwd()+'\\backpackIconFiles'):
            if self.image.lower().find(filename) > -1:
                return 'backpackIconFiles\\'+filename
    #check if the character's position coincides with the bounds of detection for the object
    def collisionDetect(self, spritex, spritey): #Use height and width of image (PIL) and spritex+50, spritey+50
        self.spritex = spritex
        self.spritey = spritey
        widthCharacter, heightCharacter = PIL.Image.open(os.path.join(os.getcwd(), 'trueAnimation', 'rightAnimation', 'right-pixil-frame-breathing-0.png')).size
        widthItem, heightItem = PIL.Image.open(self.image).size
        if self.pos[0] - 15 < spritex+widthCharacter/2 < self.pos[0]+widthItem+15 and self.pos[1] - 15 < spritey+heightCharacter/2 < self.pos[1]+heightItem+15:
            return True
    #Set the object position
    def setPos(self, pos):
        self.pos = pos
        return pos

    #change character statistics depending on the object picked up
    def effect(self, backpack, character, local_items_list, itemsList, n):
        self.backpack = backpack
        self.character = character
        self.itemsList = itemsList
        self.local_items_list = local_items_list
        self.n = n
        renderErrorText = False
        createArmorConsumable = pygame.USEREVENT + 0

        if self.image == 'src\RESIZED_syringe.png' or self.image == 'src\RESIZED_Bandage.png':
            #increment healh
            if character.getHealth() == 100:
                renderErrorText = True
            else:
                character.changeHealth(5)
        elif self.image == 'src\RESIZED_Bread50x50.png':
            #increment endurance
            if character.getEndurance() == 100:
                renderErrorText = True
            else:
                character.changeEndurance(5)
        elif self.image == 'src\RESIZED_Soda50x50.png':
            #Increment endurance
            if character.getEndurance() == 100:
                renderErrorText = True
            else:
                character.changeEndurance(2)
        elif self.image == 'src\RESIZED_Steak50x50.png':
            #Increment endurance
            if character.getEndurance() == 100:
                renderErrorText = True
            else:
                character.changeEndurance(7)
        #If the object is a laundry machine mask, check if the backpack has a suit of armor
        elif self.image == 'src\RESIZED_LaundryMachineMask.png':
            print(len(backpack.getItems()))
            for n in range(len(backpack.getItems())):
                print(n)
                if backpack.getItems()[n].getImage() == 'src\RESIZED_35x45Armor.png':
                    #Set an event in 1 second to create an armor
                    pygame.time.set_timer(createArmorConsumable, 1000, True)
                    del backpack.getItems()[n]
                    break
        #Increment armor if the character picks up an armor
        elif self.image == 'src\RESIZED_45x45Armor.png':
            character.changeArmor(10)
            self.local_items_list.pop(n)
            itemsList.pop(n)
        #Runs only if the item is pickupable
        elif itemsList[n]==True:
            #If the object is a harp, increment dps
            if self.image == 'src\RESIZED_Harp.png':
                character.changeDPS(10)
            backpack.addToPack(self)
            itemsList.pop(n)
            self.local_items_list.pop(n)
        return renderErrorText, itemsList, self.local_items_list
#Class to create the overlay with the backpack items in it
class backpackCreator:
    def backpackFunction(self, local_backpack, DISPLAYSURF, local_items_list, bool_list, spritex, spritey, drop):
        self.local_backpack = local_backpack
        self.DISPLAYSURF=DISPLAYSURF
        self.local_items_list = local_items_list
        self.bool_list = bool_list
        self.spritex = spritex
        self.spritey = spritey
        self.drop = drop
        #function to drop an object that is clicked ons
        def dropObject(local_items_list, bool_list, spritex, spritey):
            x = 0
            y = 0
            #zones of detection
            zones = [(85, 125, 35, 75),
                    (135, 175, 35, 75),
                    (185, 225, 35, 75),
                    
                    (85, 125, 95, 135),
                    (135, 175, 95, 135),
                    (185, 225, 95, 135),
                    
                    (85, 125, 155, 195),
                    (135, 175, 155, 195),
                    (195, 225, 155, 195)]
            #Drop the item whose icon you are hovering
            character_loc = (spritex, spritey)
            x, y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            for n in range(len(zones)):
                if zones[n][0] <= x <= zones[n][1] and zones[n][2] <= y <= zones[n][3]:
                    bool_list.append(True)
                    local_items_list.append(local_backpack.getItems()[n])
                    del local_backpack.getItems()[n]

        #Create a new display for the backpack
        exit = False
        while not exit:
            DISPLAYSURF.blit(pygame.image.load('trueBGImg.png'), (0,0))
            for i in range(len(local_backpack.getItems())):
                if 0 <= i <= 2: 
                    DISPLAYSURF.blit(pygame.image.load(local_backpack.getItems()[i].getIcon()),(80+50*i,30))        
                if 2 < i <= 5:
                    DISPLAYSURF.blit(pygame.image.load(local_backpack.getItems()[i].getIcon()),(80+50*(i-3),90))
                if 5 < i <= 8:
                    DISPLAYSURF.blit(pygame.image.load(local_backpack.getItems()[i].getIcon()),(80+50*(i-6),150))
            for ev in pygame.event.get():
                #exit if y is pressed, drop an object if mouse is clicked
                if ev.type==pygame.KEYDOWN:
                    if (ev.key == pygame.K_y):
                        exit = True
                if ev.type==pygame.MOUSEBUTTONDOWN:
                    if self.drop:
                        dropObject(self.local_items_list, self.bool_list, self.spritex, self.spritey)
            pygame.display.update()
        
       
#Render the graphical user interface over the background and the game
class renderGUI:
    #Render HP, endurance, and DPS
    def renderGUI(self, character, DISPLAYSURF, local_base):
        self.local_base = local_base
        local_character = character
        self.DISPLAYSURF = DISPLAYSURF
        sprite = pygame.image.load('newCharacter.png')
        heart = pygame.image.load('src\health_bar_heart.png')
        shield = pygame.image.load('src\RESIZED_character_bar_shield.png')
        stamina = pygame.image.load('src\RESIZED_character_lightning.png')
        dps = pygame.image.load('src\RESIZED_character_sword.png')
        #Display the stamina, shield, and dps symbols
        DISPLAYSURF.blit(stamina, (322, 447))
        DISPLAYSURF.blit(shield, (370, 451))
        DISPLAYSURF.blit(dps, (420, 450))
        for i in range(int(round(local_character.getHealth()/20))):
            DISPLAYSURF.blit(heart, (4+36.25*i, 455))
        font = pygame.font.SysFont(None, 15)
        #Render the text for the character statistics canvas
        lifeText = font.render('Life: {}%'.format(local_character.getHealth()), True, (0,0,0))
        DISPLAYSURF.blit(lifeText, (4, 437))
        staminaText = font.render("{}".format(local_character.getEndurance()), True, (0,0,0))
        DISPLAYSURF.blit(staminaText, (355, 460))
        shieldText = font.render("{}".format(local_character.getArmor()), True, (0,0,0))
        DISPLAYSURF.blit(shieldText, (405, 460))
        dpsText = font.render("{}".format(local_character.getDPS()), True, (0,0,0))
        DISPLAYSURF.blit(dpsText, (455, 460))
        local_base.updateHealth()
        baseHpText = font.render("Base {}%".format(local_base.getHealth()), True, (0,0,0))
        if local_base.getHealth() <= 0:
            #Error message for player trying to escape the boss
            DISPLAYSURF.fill((0,0,0))
            font = pygame.font.SysFont(None, 30)
            gameOverText = font.render('THE BASE HAS COMPLETELY FROZEN.', True, (255, 255, 255))
            DISPLAYSURF.blit(gameOverText, (50,220))
            pygame.display.update()
            pygame.time.delay(3000)
            pygame.quit()
            #return local_character, local_backpack
        DISPLAYSURF.blit(baseHpText, (4, 15))  
        for i in range(int(round(local_base.getHealth()/20))):
            DISPLAYSURF.blit(heart, (4+36.25*i, 30))   
        

class pygameMovement:
    def __init__(self, frameIncrementerBreathing = 0, frameIncrementerRunning = 0, oldFrameTimeBreathing = 0, oldFrameTimeRunning = 0, right = True):
        #Store the frame variables to keep track of where the animation is
        self.frameIncrementerBreathing = frameIncrementerBreathing
        self.frameIncrementerRunning = frameIncrementerRunning
        self.oldFrameTimeBreathing = oldFrameTimeBreathing
        self.oldFrameTimeRunning = oldFrameTimeRunning
        self.right = right

    def movesLikeJagger(self, time, keys_list, spritex, spritey):
        self.keys_list = keys_list
        self.spritex = spritex
        self.spritey = spritey
        image = ""
        #If the arrow keys are pressed, update the sprite's position
        if keys_list[pygame.K_LEFT] and spritex>82.5:
            spritex -= 2.5
            self.right = False
        elif keys_list[pygame.K_RIGHT] and spritex<377.5:
            spritex += 2.5
            self.right = True

        if keys_list[pygame.K_UP] and spritey>52.5:
            spritey -= 2.5
        elif keys_list[pygame.K_DOWN] and spritey<332.5:
            spritey += 2.5
        
        #If no arrow keys are being pressed, change the sprite every 400ms
        if not (keys_list[pygame.K_LEFT] or keys_list[pygame.K_RIGHT] or keys_list[pygame.K_UP] or keys_list[pygame.K_DOWN]):
            #Check if the character is facing left or right, and render the sprite based on that
            if self.right and (int(time/100)) % 4 == 0 and (self.oldFrameTimeBreathing < (int(time/100))):
                self.frameIncrementerBreathing=(self.frameIncrementerBreathing+1)%4
                self.oldFrameTimeBreathing = (int(time/100))
                image = pygame.image.load('trueAnimation/rightAnimation/right-pixil-frame-breathing-{}.png'.format(self.frameIncrementerBreathing))
            elif self.right:
                image = pygame.image.load('trueAnimation/rightAnimation/right-pixil-frame-breathing-{}.png'.format(self.frameIncrementerBreathing))
            
            if not self.right and (int(time/100)) % 4 == 0 and (self.oldFrameTimeBreathing < (int(time/100))):
                self.frameIncrementerBreathing=(self.frameIncrementerBreathing+1)%4
                self.oldFrameTimeBreathing = (int(time/100))
                image = pygame.image.load('trueAnimation/leftAnimation/left-right-pixil-frame-breathing-{}.png'.format(self.frameIncrementerBreathing))
            elif not self.right:
                image = pygame.image.load('trueAnimation/leftAnimation/left-right-pixil-frame-breathing-{}.png'.format(self.frameIncrementerBreathing))
        else:
            #If arrow keys are being pressed, change the sprite every 100ms

            #Check if the character is facing left or right, and render the sprite based on that
            if (keys_list[pygame.K_RIGHT] or self.right) and (int(time/50)) % 2 == 0 and (self.oldFrameTimeRunning < (int(time/50))):
                self.frameIncrementerRunning=(self.frameIncrementerRunning+1)%9
                self.oldFrameTimeRunning = int(time/50)
                image = pygame.image.load('trueAnimation/rightAnimation/right-pixil-frame-running-{}.png'.format(self.frameIncrementerRunning))
            elif keys_list[pygame.K_RIGHT] or self.right:
                image = pygame.image.load('trueAnimation/rightAnimation/right-pixil-frame-running-{}.png'.format(self.frameIncrementerRunning))
            if (keys_list[pygame.K_LEFT] or not self.right) and (int(time/50)) % 2 == 0 and (self.oldFrameTimeRunning < (int(time/50))):
                self.frameIncrementerRunning=(self.frameIncrementerRunning+1)%9
                self.oldFrameTimeRunning = int(time/50)
                image = pygame.image.load('trueAnimation/leftAnimation/left-right-pixil-frame-running-{}.png'.format(self.frameIncrementerRunning))
            elif keys_list[pygame.K_LEFT] or not self.right:
                image = pygame.image.load('trueAnimation/leftAnimation/left-right-pixil-frame-running-{}.png'.format(self.frameIncrementerRunning))
        
        #return the current sprite and position
        return image, spritex, spritey