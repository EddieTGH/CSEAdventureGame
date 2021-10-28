"""
CSE Choose your own Adventure
Team members: Esben Nielsen, Shashwat Tewari, Edmond Niu
Date: 3/22/2021
pygamePort_test_file.py
Task Description:
Hosts the classes for all 7 of the rooms that we have implemented including the hallway.
Handles the interaction between the player and the pick-up-able objects in the room as
well as the consumable objects in the room. Handles the character, backpack, and base methods
"""


import pygame
from pygamePort_modules import *
#from main import * 
from PIL import Image
import os.path
#from bossroom import BossRoom
#from medbay import MedBayRoom
#from cafeteria import CafeteriaRoom
#from commandcenter import CommandRoom
#from laundry import LaundryRoom
#from bossroom import BossRoom
#from weaponsroom import WeaponsRoom
#from backgroundCanvas import BackgroundRoom
#from item import InteractiveItem
import time

#global variables for the character, backpack, and base
global local_character
global local_backpack
global local_base
#global medBayRoom
#Global variables for the mirrored lists determining whether items are interactable for each of the rooms
global itemsListMedBay
global itemsListCafeteria
global itemsListLaundry
global itemsListBoss
global itemsListCommandCenter
global itemsListWeaponsRoom



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
        #updateBaseHealth()
        #print(self.health)
#Backpack class for defining the backpack object that will be passed among python files

class Backpack():
    def __init__(self, size):
        self.size = size
        self.pack = []

    def getItems(self):
        return self.pack

    def getSize(self):
        return self.size

    #item is a string that correlates to the 'name' attribute of the InteractiveItem2 objects in the pack
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
            
#Character class for defining the character
class Character():
    def __init__(self, initialHealth, initialArmor, initialEndurance, dps, maxHealth, maxArmor):
        self.health = initialHealth
        self.armor = initialArmor
        self.endurance = initialEndurance
        self.dps = dps
        self.maxHealth = maxHealth
        self.maxArmor = maxArmor
        self.maxDPS = 50
        self.maxEndurance = 100
    #return health
    def getHealth(self):
        return self.health
    #change health within bounds of 0 and maxHealth
    def changeHealth(self, increment):
        self.health += increment
        if self.health > self.maxHealth:
            self.health = self.maxHealth
        elif self.health < 0:
            self.health = 0
        return self.health
    #Return armor
    def getArmor(self):
        return self.armor
    #return maximum level of armor
    def getMaxArmor(self):
        return self.maxArmor
    #change armor between bounds of 0 amd maxArmor
    def changeArmor(self, increment):
        self.armor += increment
        if self.armor < 0:
            self.armor = 0
        elif self.armor > self.maxArmor:
            self.armor = self.maxArmor
        return self.armor
    #Return endurance
    def getEndurance(self):
        return self.endurance
    #change endurance between bounds of 0 and 100
    def changeEndurance(self, increment):
        maxEndurance = 100
        self.endurance += increment
        if self.endurance > maxEndurance:
            self.endurance = maxEndurance
        elif self.endurance < 0:
            self.endurance = 0
        return self.endurance
    #Return damage per strike
    def getDPS(self):
        return self.dps
    #change dps within bounds of 0 and the maxDPS parameter
    def changeDPS(self, increment):
        self.dps += increment
        if self.dps > self.maxDPS:
            self.dps = self.maxDPS
        elif self.dps < 0:
            self.dps = 0
        return self.dps

#Item lists that mirror the local items lists to determine whether objects are interactable
itemsListMedBay = [True, True, True, True, True, True]
itemsListCafeteria = [True, True, True, True]
itemsListLaundry = [True, True, True, True, True, True, True]
itemsListBoss = []
itemsListCommandCenter = [True, True, True, True, True, True]
itemsListWeaponsRoom = [True, True, True, True, True, True, True]
#backpack, base, and character objects
local_backpack = Backpack(9)
local_base = Base(100, 2, 1)
local_character = Character(50, 10, 30, 5, 100, 100)

#Class to define the Medbay Room
class medBayRoom_pygame:
    #constructor
    def __init__(self, itemsList):
        self.itemsList=itemsList
        #initializing interactive items for consuming or picking up
        self.syr = InteractiveItem2('src\RESIZED_syringe.png', (300, 65), self.itemsList[0])
        self.ban = InteractiveItem2('src\RESIZED_Bandage.png', (147, 73), self.itemsList[1])
        self.flashlight = InteractiveItem2('src\RESIZED_Flashlight.png', (170, 250), self.itemsList[2])
        self.laundryKey = InteractiveItem2('src\RESIZED_laundry_key.png', (200, 200), self.itemsList[3])
        self.spoon1 = InteractiveItem2('src\RESIZED_Spoon.png', (260, 250), self.itemsList[4])
        self.fork = InteractiveItem2('src\RESIZED_Fork.png', (290, 300), self.itemsList[5])
        #Local items list that contains the items in the room
        self.local_item_list = [self.flashlight, self.laundryKey, self.spoon1, self.fork, self.syr, self.ban]
    #Renders the game onto the pygame window
    def renderGame(self, character, backpack, base):
        #Synchronize objects
        local_backpack = backpack
        local_character = character
        local_base = base
        #Variable to tell whether to display error text or not
        self.renderErrorText = False
        #start pygame
        pygame.init()
        #make character movement object
        characterMovementObj = pygameMovement()

        #set fps and pygame clock
        FPS=120
        fpsClock=pygame.time.Clock()
        #set window width and height
        width=500
        height=500
        DISPLAYSURF=pygame.display.set_mode((width,height),0,32)
        pygame.display.set_caption('MedBay')
        #Load the background, the transparent background, and the character
        background=pygame.image.load('src/RESIZED_MedBay_Background_ACTUAL.png')
        truebg=pygame.image.load('trueBGImg.png')
        sprite=pygame.image.load('newCharacter.png')

        

        spritex=195
        spritey=332.5

        while True:
            #Display the transparent background and the background
            DISPLAYSURF.blit(truebg, (0,0))
            DISPLAYSURF.blit(background, (0,0))
            #Check if need to render error text
            if self.renderErrorText:
                font = pygame.font.SysFont(None, 15)
                maxHealthError = font.render('Max health. Adding more won\'t do anything.', True, (0, 0, 0))
                DISPLAYSURF.blit(maxHealthError, (100,20))
            #Render overlay GUI
            renderGUI.renderGUI(self, local_character, DISPLAYSURF, local_base)

            #Render all of the objects on the screen
            for n in range(len(self.local_item_list)):
                if self.itemsList[n]:
                    DISPLAYSURF.blit(pygame.image.load(self.local_item_list[n].getImage()), self.local_item_list[n].getPos())
            '''for item in local_item_list: #Rendering the items
                if not item.simpleSearch(local_backpack.getItems()):
                    DISPLAYSURF.blit(pygame.image.load(item.getImage()), item.getPos())'''
            DISPLAYSURF.blit(sprite,(spritex,spritey))
            #Iterate through the events, checking them for key presses; call functions accordingly
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE):
                        #pygame.quit()
                        #Move back to the main hallway
                        mainRoom.renderGame(local_character, local_backpack, local_base)
                        return self.local_item_list, local_character, local_backpack
                    if (event.key == pygame.K_y):
                        #Open the backpack window
                        backpackCreator.backpackFunction(self, local_backpack, DISPLAYSURF, self.local_item_list , self.itemsList, spritex, spritey, True)
                    if (event.key == pygame.K_e):
                        #check for collisions with an interactive object and pick it up if so
                        n = 0
                        while n < len(self.local_item_list):
                            if self.local_item_list[n].collisionDetect(spritex, spritey):
                                self.renderErrorText, self.itemsList, self.local_item_list = self.local_item_list[n].effect(local_backpack, local_character, self.local_item_list, self.itemsList, n)
                            n+=1
                #print the location of the mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Mouse: {}, {}. Sprite: {}, {}".format(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], spritex, spritey))
            #update spritex, spritey
            sprite, spritex, spritey = characterMovementObj.movesLikeJagger(pygame.time.get_ticks(), pygame.key.get_pressed(), spritex, spritey)
            
            #print(local_character.getHealth())
            pygame.display.update()
            fpsClock.tick(FPS)


class cafeteriaRoom_pygame:
    #constructor
    def __init__(self, itemsList):
        self.itemsList=itemsList
        #interactive items
        self.flashlight = InteractiveItem2('src\RESIZED_Flashlight.png', (350, 240), self.itemsList[0])
        self.bread = InteractiveItem2('src\RESIZED_Bread50x50.png', (130, 120), self.itemsList[1])
        self.soda = InteractiveItem2('src\RESIZED_Soda50x50.png', (240, 120), self.itemsList[2])
        self.steak = InteractiveItem2('src\RESIZED_Steak50x50.png', (355, 120), self.itemsList[3])
        
        #local item list
        self.local_item_list = [self.flashlight, self.bread, self.soda, self.steak]
    #Renders the game
    def renderGame(self, character, backpack, base):
        local_backpack = backpack
        local_character = character
        local_base = base
        self.renderErrorText = False
        pygame.init()
        characterMovementObj = pygameMovement()

        FPS=120
        fpsClock=pygame.time.Clock()

        width=500
        height=500
        DISPLAYSURF=pygame.display.set_mode((width,height),0,32)
        pygame.display.set_caption('Cafeteria')

        #Load cafeteria background
        background=pygame.image.load('Original Backgrounds\RESIZED_CafeteriaRoom_background.png')
        lockedbackground = pygame.image.load('Original Backgrounds\RESIZED_Locked_CafeteriaRoom-BG.png')
        truebg=pygame.image.load('trueBGImg.png')
        sprite=pygame.image.load('newCharacter.png')

        

        spritex=195
        spritey=332.5
        #while loop
        while True:
            #render everything, including background, interactive items, error text if necessary
            DISPLAYSURF.blit(truebg, (0,0))
            DISPLAYSURF.blit(background, (0,0))
            renderGUI.renderGUI(self, local_character, DISPLAYSURF, local_base)
            if self.renderErrorText:
                font = pygame.font.SysFont(None, 15)
                maxEdError = font.render('Max endurance. Adding more won\'t do anything.', True, (0, 0, 0))
                DISPLAYSURF.blit(maxEdError, (100,20))
            for n in range(len(self.local_item_list)):
                if self.itemsList[n]:
                    DISPLAYSURF.blit(pygame.image.load(self.local_item_list[n].getImage()), self.local_item_list[n].getPos())
            '''for item in local_item_list: #Rendering the items
                if not item.simpleSearch(local_backpack.getItems()):
                    DISPLAYSURF.blit(pygame.image.load(item.getImage()), item.getPos())'''
            DISPLAYSURF.blit(sprite,(spritex,spritey))
            #Checking key presses for any triggers; see comments above for explanation on what each of these does
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE):
                        mainRoom.renderGame(local_character, local_backpack, local_base)
                        return self.local_item_list, local_character, local_backpack
                    if (event.key == pygame.K_y):
                        backpackCreator.backpackFunction(self, local_backpack, DISPLAYSURF, self.local_item_list, self.itemsList, spritex, spritey, True)
                    if (event.key == pygame.K_e):
                        n = 0
                        while n < len(self.local_item_list):
                            if self.local_item_list[n].collisionDetect(spritex, spritey):
                                self.renderErrorText, self.itemsList, self.local_item_list = self.local_item_list[n].effect(local_backpack, local_character, self.local_item_list, self.itemsList, n)
                            n += 1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Mouse: {}, {}. Sprite: {}, {}".format(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], spritex, spritey))
            #updating character position
            sprite, spritex, spritey = characterMovementObj.movesLikeJagger(pygame.time.get_ticks(), pygame.key.get_pressed(), spritex, spritey)
            
            #print(local_character.getHealth())
            pygame.display.update()
            fpsClock.tick(FPS)


class bossRoom_pygame:
    #constructor
    def __init__(self, itemsList):
        self.itemsList=itemsList
    #renders the pygame game
    def renderGame(self, character, backpack, base):
        local_backpack = backpack
        local_character = character
        local_base = base
        startGame = False
        pygame.init()
        #characterMovementObj = pygameMovement()
        #Class to keep track of the boss's health and damage per strike
        class Boss:
            def __init__(self, initialHealth, dps):
                self.health = initialHealth
                self.dps = dps

            def getDamaged(self, increment):
                self.health -= increment
                if self.health < 0:
                    self.health = 0

                return self.health

            def getHealth(self):
                return self.health

            def getDPS(self):
                return self.dps
        #Set an event in the future where the character will be able to attack
        charAttackPossible = pygame.USEREVENT + 1
        #Set an event in the future where the boss will be able to attack
        bossAttackPossible = pygame.USEREVENT + 2
        #Setting timers
        pygame.time.set_timer(charAttackPossible, 5000)
        pygame.time.set_timer(bossAttackPossible, 5000)
        
        FPS=120
        fpsClock=pygame.time.Clock()

        width=500
        height=500
        DISPLAYSURF=pygame.display.set_mode((width,height),0,32)
        pygame.display.set_caption('Boss Room')

        #Loading boss background
        background=pygame.image.load('Original Backgrounds\RESIZED_BossRoom_background.png')
        lockedbackground = pygame.image.load('Original Backgrounds\RESIZED_Locked_BossRoom-BG.png')
        truebg=pygame.image.load('trueBGImg.png')
        sprite=pygame.image.load('newCharacter.png')
        bossImage=pygame.image.load('src\RESIZED_boss.png')

        #Checking the backpack to see if a flashlight is present; start the fight if yes
        flashlight = InteractiveItem2('src\RESIZED_Flashlight.png', (0, 0), False)
        for n in range(len(local_backpack.getItems())):
            print("backpackSize:{}, n:{}".format(len(local_backpack.getItems()), n))
            if flashlight.equals(local_backpack.getItems()[n]):
                startGame=True
                
        #bread = InteractiveItem2('src\RESIZED_Bread50x50.png', (140, 130), self.itemsList[1])
        #soda = InteractiveItem2('src\RESIZED_Soda50x50.png', (250, 130), self.itemsList[2])
        #steak = InteractiveItem2('src\RESIZED_Steak50x50.png', (365, 130), self.itemsList[3])
        
        #local_item_list = [flashlight, bread, soda, steak]
        #Boss object
        boss = Boss(100, 10)
        #Booleans pertinent to the state of the boss fight so that the character and boss know when to attack and when to not attack
        battle_ongoing = False
        gameOver = False
        attackCooldown = 3
        bossAttackCooldown = 3 
        charAttack = True
        bossAttack = False

        charAttackDue = True
        bossAttackDue = True

        char_forwards = True
        char_backwards = False

        boss_forwards = True
        boss_backwards = False
        #Positions of boss and character 
        final_x = 300
        start_x = 100

        final_x_boss = 100
        start_x_boss = 300

        spritex=100
        spritey=332.5

        bossx = 285
        bossy = 260
        #Start music
        if startGame:
            pygame.mixer.music.load('bossMusic.mp3')
            pygame.mixer.music.play()
        #while loop to start rendering and updating display
        while True:
            DISPLAYSURF.blit(truebg, (0,0))
            #checking for the startGame boolean; if True, render the normal background, otherwise, render the grayed out background
            if startGame:
                DISPLAYSURF.blit(background, (0,0))
            else:
                DISPLAYSURF.blit(lockedbackground, (0,0))
            renderGUI.renderGUI(self, local_character, DISPLAYSURF, local_base)
            #Render boss hp
            if startGame:
                font = pygame.font.SysFont(None, 20)
                bossLifeText = font.render('Boss Hp: {}%'.format(boss.getHealth()), True, (0,0,0))
                DISPLAYSURF.blit(bossLifeText, (300, 100))

            #If the player has pressed the b key and the character and boss's health are not 0; allow the character and boss to attack
            if battle_ongoing and not (local_character.getHealth()==0) and not boss.getHealth()==0 and startGame:
                if local_character.getEndurance() > 0:
                    spritex, spritey, charAttack, charAttackDue, char_forwards, char_backwards, local_character, boss = self.characterAttack(spritex, spritey, charAttack, bossAttack, charAttackDue, 
                        final_x, start_x, char_forwards, char_backwards, local_character, boss)
                bossx, bossy, bossAttack, bossAttackDue, boss_forwards, boss_backwards, local_character, boss = self.bossAtt(bossx, bossy, charAttack, bossAttack, bossAttackDue, 
                        final_x_boss, start_x_boss, boss_forwards, boss_backwards, local_character, boss)
            #death
            if local_character.getHealth() == 0:
                pygame.mixer.music.stop
                pygame.mixer.music.load('deathSound.mp3')
                pygame.mixer.music.play()
                DISPLAYSURF.fill((0,0,0))
                font = pygame.font.SysFont(None, 30)
                gameOverText = font.render('YOU DIED.', True, (255, 255, 255))
                DISPLAYSURF.blit(gameOverText, (200,220))
                pygame.display.update()
                pygame.time.wait(3000)
                pygame.quit()
            if local_character.getEndurance() == 0:
                font = pygame.font.SysFont(None, 15)
                zeroEdError = font.render('You are too tired to attack. Good luck trying to beat the boss now.', True, (0, 0, 0))
                DISPLAYSURF.blit(zeroEdError, (100,20))
            
            
        
            DISPLAYSURF.blit(sprite,(spritex,spritey))
            #Only render the boss's image if the startGame variable is True
            if startGame:
                DISPLAYSURF.blit(bossImage, (bossx, bossy))
            #survive and victory
            if boss.getHealth() == 0:
                if startGame:
                    pygame.mixer.music.stop
                    pygame.mixer.music.load('victorySound.mp3')
                    pygame.mixer.music.play()
                DISPLAYSURF.fill((0,0,0))
                font = pygame.font.SysFont(None, 30)
                gameOverText = font.render('VICTORY!', True, (255, 255, 255))
                gameOverText2 = font.render('We hope you enjoyed...', True, (255, 255, 255))
                gameOverText3 = font.render('MELT THE ICE AWAY!', True, (255,255,255))
                DISPLAYSURF.blit(gameOverText, (200,220))
                DISPLAYSURF.blit(gameOverText2, (150,250))


                pygame.display.update()
                if startGame:
                    pygame.time.wait(5000)
                DISPLAYSURF.blit(gameOverText3, (150, 280))
                pygame.display.update()
                startGame = False
                #pygame.time.wait(3000)
                #pygame.quit()
            #iterating through events; checking for triggers
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE) and startGame:
                        #Error message for player trying to escape the boss
                        DISPLAYSURF.fill((0,0,0))
                        font = pygame.font.SysFont(None, 30)
                        gameOverText = font.render('YOU CANNOT ESCAPE FROM THE BOSS.', True, (255, 255, 255))
                        DISPLAYSURF.blit(gameOverText, (50,220))
                        pygame.display.update()
                        pygame.time.delay(3000)
                        #return local_character, local_backpack
                    elif (event.key == pygame.K_ESCAPE) and not startGame:
                        #go back to main room if player presses escape and the game is not started
                        mainRoom.renderGame(local_character, local_backpack, local_base)
                        return local_character, local_backpack
                    if (event.key == pygame.K_y):
                        pass
                    '''if (event.key == pygame.K_e):
                        for n in range(len(local_item_list)):
                            if local_item_list[n].collisionDetect(spritex, spritey):
                                self.itemsList = local_item_list[n].effect(local_backpack, local_character, self.itemsList, n)'''
                    #Key to start the battle
                    if (event.key == pygame.K_b and startGame):
                        print("Making battle_ongoing True")
                        battle_ongoing = True
                #Checking for events that make the boss attack possible
                if (event.type == bossAttackPossible):
                    bossAttackDue = True
                #Checking for events that make the character attack possible
                if (event.type == charAttackPossible):
                    charAttackDue = True


                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Mouse: {}, {}. Sprite: {}, {}".format(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], spritex, spritey))
            
            #sprite, spritex, spritey = characterMovementObj.movesLikeJagger(pygame.time.get_ticks(), pygame.key.get_pressed(), spritex, spritey)
            
            #print(local_character.getHealth())
            
            pygame.display.update()
            fpsClock.tick(FPS)
    #Function for moving the character over to the boss and attacking
    def characterAttack(self, spritex, spritey, charAttack, bossAttack, charAttackDue, final_x, start_x, char_forwards, char_backwards, local_character, boss):
        #if the boss is not attacking and a character attack is due and the character's endurance is not 0
        if not bossAttack and charAttackDue and local_character.getEndurance() > 0:
            #Set char attack to true
            charAttack = True
            #If character has not reached the final position and they are supposed to be moving forwards
            if spritex < final_x and char_forwards:
                #Increment position forwards
                spritex += 2
            #If the character is at the final x
            elif spritex == final_x and char_forwards:
                #Render damage to the boss
                boss.getDamaged(local_character.getDPS())
                """ local_character.changeArmor(local_character.getDPS())"""
                char_forwards = False
                char_backwards = True
                #Start moving backwards
                spritex -= 2
            #If the character is moving backwards and has not reached the start
            elif spritex < final_x and char_backwards:
                #Decrement the position
                spritex -= 2
            #If the character has reached the start, end the attack and allow the boss to attack
            if spritex < start_x and char_backwards:
                print("Ending attack")
                print(boss.health)
                char_forwards = True
                char_backwards = False
                charAttack = False
                charAttackDue = False
                local_character.changeEndurance(-10)
        #Return variables
        return spritex, spritey, charAttack, charAttackDue, char_forwards, char_backwards, local_character, boss
    #Function for moving the boss over to the character and attacking
    def bossAtt(self, bossx, bossy, charAttack, bossAttack, bossAttackDue, final_x_boss, start_x_boss, boss_forwards, boss_backwards, local_character, boss):
        #Format is very similar to characterAttack
        #See comments above for explanation
        #Inequalities are reversed since the boss moves oppositely
        if not charAttack and bossAttackDue and boss.getHealth() > 0:
            bossAttack = True
            if bossx > final_x_boss and boss_forwards:
                bossx -= 1
            elif bossx == final_x_boss and boss_forwards:
                dps = -1 * int(boss.getDPS() * (1-(local_character.getArmor() / local_character.getMaxArmor())))
                print("Boss's dps: ", dps)
                local_character.changeHealth(dps)
                armor_decrement = -1 * int(0.1 * local_character.getArmor())
                if local_character.getArmor() < 10:
                    armor_decrement = -1
                local_character.changeArmor(armor_decrement)
                #local_character.changeEndurance(dps)
                boss_forwards = False
                boss_backwards = True
                bossx += 1
            if bossx < start_x_boss and boss_backwards:
                bossx += 1
            if bossx == start_x_boss and boss_backwards:
                bossAttack = False
                boss_forwards = True
                boss_backwards = False
                bossAttackDue = False
            
        return bossx, bossy, bossAttack, bossAttackDue, boss_forwards, boss_backwards, local_character, boss
#Class to build the laundry room
class laundryRoom_pygame:
    def __init__(self, itemsList):
        self.itemsList=itemsList
        #Interactive items
        self.flashlight = InteractiveItem2('src\RESIZED_Flashlight.png', (350, 240), self.itemsList[0])
        self.armor = InteractiveItem2('src\RESIZED_35x45Armor.png', (309,165), self.itemsList[4])
        self.laundryMachine = InteractiveItem2('src\RESIZED_LaundryMachineMask.png', (102,118), self.itemsList[5])
        
        self.local_item_list = [self.flashlight, self.armor, self.laundryMachine]
    def renderGame(self, character, backpack, base):
        local_backpack = backpack
        local_character = character
        local_base = base
        #error text boolean for rendering
        self.renderErrorText = False
        pygame.init()
        createArmorConsumable = pygame.USEREVENT + 0
        characterMovementObj = pygameMovement()

        FPS=120
        fpsClock=pygame.time.Clock()

        width=500
        height=500
        DISPLAYSURF=pygame.display.set_mode((width,height),0,32)
        pygame.display.set_caption('Laundry Room')
        #Render the laundry room background
        background=pygame.image.load('Original Backgrounds\RESIZED_Laundry_Room_background.png')
        lockedbackground = pygame.image.load('Original Backgrounds\RESIZED_Locked_Laundry_Room_background.png')
        truebg=pygame.image.load('trueBGImg.png')
        sprite=pygame.image.load('newCharacter.png')
        

        spritex=195
        spritey=332.5

        while True:
            #Render the transparent background and the normal background
            DISPLAYSURF.blit(truebg, (0,0))
            DISPLAYSURF.blit(background, (0,0))
            renderGUI.renderGUI(self, local_character, DISPLAYSURF, local_base)
            #Put the interactive items on the display
            for n in range(len(self.local_item_list)):
                if self.itemsList[n]:
                    DISPLAYSURF.blit(pygame.image.load(self.local_item_list[n].getImage()), self.local_item_list[n].getPos())
            '''for item in local_item_list: #Rendering the items
                if not item.simpleSearch(local_backpack.getItems()):
                    DISPLAYSURF.blit(pygame.image.load(item.getImage()), item.getPos())'''
            DISPLAYSURF.blit(sprite,(spritex,spritey))
            #Iterate through events and check for key presses that are keybinds
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE):
                        #Return to hallway
                        mainRoom.renderGame(local_character, local_backpack, local_base)
                        return self.local_item_list, local_character, local_backpack
                    if (event.key == pygame.K_y):
                        #open backpack
                        backpackCreator.backpackFunction(self, local_backpack, DISPLAYSURF, self.local_item_list, self.itemsList, spritex, spritey, True)
                    if (event.key == pygame.K_e):
                        #Check for object collisions and pick up if so
                        print(len(self.local_item_list))
                        n = 0
                        while n < len(self.local_item_list):
                            if self.local_item_list[n].collisionDetect(spritex, spritey):
                                self.renderErrorText, self.itemsList, self.local_item_list = self.local_item_list[n].effect(local_backpack, local_character, self.local_item_list, self.itemsList, n)
                            n += 1
                #If the event is a create Armor event:
                #Create a new suit of armor and place it in the local_item_list and on the self.itemsList
                if event.type == createArmorConsumable:
                    self.local_item_list.append(InteractiveItem2('src\RESIZED_45x45Armor.png', (318, 165), True))
                    self.itemsList.append(True)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Mouse: {}, {}. Sprite: {}, {}".format(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], spritex, spritey))
            #update character position
            sprite, spritex, spritey = characterMovementObj.movesLikeJagger(pygame.time.get_ticks(), pygame.key.get_pressed(), spritex, spritey)
            
            #print(local_character.getHealth())
            pygame.display.update()
            fpsClock.tick(FPS)
#Class for rendering command center
class commandCenter_pygame:
    def __init__(self, itemsList):
        self.itemsList=itemsList
        #Interactive items
        self.flashlight = InteractiveItem2('src\RESIZED_Flashlight.png', (350, 240), self.itemsList[0])
        self.spoon = InteractiveItem2('src\RESIZED_Spoon.png', (90,300), self.itemsList[1])
        #bread = InteractiveItem2('src\RESIZED_Bread50x50.png', (140, 130), self.itemsList[1])
        #soda = InteractiveItem2('src\RESIZED_Soda50x50.png', (250, 130), self.itemsList[2])
        #steak = InteractiveItem2('src\RESIZED_Steak50x50.png', (365, 130), self.itemsList[3])
        
        self.local_item_list = [self.flashlight, self.spoon]
    def renderGame(self, character, backpack, base):
        local_backpack = backpack
        local_character = character
        local_base = base
        self.renderErrorText = False
        pygame.init()
        characterMovementObj = pygameMovement()

        FPS=120
        fpsClock=pygame.time.Clock()

        width=500
        height=500
        DISPLAYSURF=pygame.display.set_mode((width,height),0,32)
        pygame.display.set_caption('Command Center')
        #Render the command center background
        background=pygame.image.load('Original Backgrounds\RESIZED_commandCenter.png')
        #lockedbackground = pygame.image.load('Original Backgrounds\RESIZED_Locked_CafeteriaRoom-BG.png')
        truebg=pygame.image.load('trueBGImg.png')
        sprite=pygame.image.load('newCharacter.png')
        

        spritex=195
        spritey=332.5

        while True:
            #Render the background and the character and the interactive items
            DISPLAYSURF.blit(truebg, (0,0))
            DISPLAYSURF.blit(background, (0,0))
            renderGUI.renderGUI(self, local_character, DISPLAYSURF, local_base)

            for n in range(len(self.local_item_list)):
                if self.itemsList[n]:
                    DISPLAYSURF.blit(pygame.image.load(self.local_item_list[n].getImage()), self.local_item_list[n].getPos())
            '''for item in self.local_item_list: #Rendering the items
                if not item.simpleSearch(local_backpack.getItems()):
                    DISPLAYSURF.blit(pygame.image.load(item.getImage()), item.getPos())'''
            DISPLAYSURF.blit(sprite,(spritex,spritey))
            #Iterate through events, checking for keybinds
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE):
                        #Return to main
                        mainRoom.renderGame(local_character, local_backpack, local_base)
                        return self.local_item_list, local_character, local_backpack
                    if (event.key == pygame.K_y):
                        #Open backpack
                        backpackCreator.backpackFunction(self, local_backpack, DISPLAYSURF, self.local_item_list, self.itemsList, spritex, spritey, True)
                    if (event.key == pygame.K_e):
                        #Pick up item
                        n = 0
                        while n < len(self.local_item_list):
                            if self.local_item_list[n].collisionDetect(spritex, spritey):
                                self.renderErrorText, self.itemsList, self.local_item_list = self.local_item_list[n].effect(local_backpack, local_character, self.local_item_list, self.itemsList, n)
                            n += 1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Mouse: {}, {}. Sprite: {}, {}".format(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], spritex, spritey))
            #Update character position
            sprite, spritex, spritey = characterMovementObj.movesLikeJagger(pygame.time.get_ticks(), pygame.key.get_pressed(), spritex, spritey)
            
            #print(local_character.getHealth())
            pygame.display.update()
            fpsClock.tick(FPS)

#Class for rendering the weapons room
class weaponsRoom_pygame:
    def __init__(self, itemsList):
        self.itemsList=itemsList
        #Interactive items
        self.flashlight = InteractiveItem2('src\RESIZED_Flashlight.png', (350, 240), self.itemsList[0])
        self.harp = InteractiveItem2('src\RESIZED_Harp.png', (200, 130), self.itemsList[1])
        #soda = InteractiveItem2('src\RESIZED_Soda50x50.png', (250, 130), self.itemsList[2])
        #steak = InteractiveItem2('src\RESIZED_Steak50x50.png', (365, 130), self.itemsList[3])
        
        self.local_item_list = [self.flashlight, self.harp]
    def renderGame(self, character, backpack, base):
        local_backpack = backpack
        local_character = character
        local_base = base
        self.renderErrorText = False
        pygame.init()
        characterMovementObj = pygameMovement()

        FPS=120
        fpsClock=pygame.time.Clock()

        width=500
        height=500
        DISPLAYSURF=pygame.display.set_mode((width,height),0,32)
        pygame.display.set_caption('Weapons Room')
        #Render weapons room background
        background=pygame.image.load('Original Backgrounds\RESIZED_weaponsRoom.png')
        #lockedbackground = pygame.image.load('Original Backgrounds\RESIZED_Locked_CafeteriaRoom-BG.png')
        truebg=pygame.image.load('trueBGImg.png')
        sprite=pygame.image.load('newCharacter.png')
        

        spritex=195
        spritey=332.5

        while True:
            #Render the background and character and interactive items
            DISPLAYSURF.blit(truebg, (0,0))
            DISPLAYSURF.blit(background, (0,0))
            renderGUI.renderGUI(self, local_character, DISPLAYSURF, local_base)

            for n in range(len(self.local_item_list)):
                if self.itemsList[n]:
                    DISPLAYSURF.blit(pygame.image.load(self.local_item_list[n].getImage()), self.local_item_list[n].getPos())
            '''for item in self.local_item_list: #Rendering the items
                if not item.simpleSearch(local_backpack.getItems()):
                    DISPLAYSURF.blit(pygame.image.load(item.getImage()), item.getPos())'''
            DISPLAYSURF.blit(sprite,(spritex,spritey))
            #Check keys pressed for keybinds
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    #return to main
                    if (event.key == pygame.K_ESCAPE):
                        mainRoom.renderGame(local_character, local_backpack, local_base)
                        return self.local_item_list, local_character, local_backpack
                    if (event.key == pygame.K_y):
                        #Open backpack
                        backpackCreator.backpackFunction(self, local_backpack, DISPLAYSURF, self.local_item_list, self.itemsList, spritex, spritey, True)
                    if (event.key == pygame.K_e):
                        #Check collisions and pick up object if necessary
                        n = 0
                        while n < len(self.local_item_list):
                            if self.local_item_list[n].collisionDetect(spritex, spritey):
                                self.renderErrorText, self.itemsList, self.local_item_list = self.local_item_list[n].effect(local_backpack, local_character, self.local_item_list, self.itemsList, n)
                            n += 1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Mouse: {}, {}. Sprite: {}, {}".format(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], spritex, spritey))
            #Update character position
            sprite, spritex, spritey = characterMovementObj.movesLikeJagger(pygame.time.get_ticks(), pygame.key.get_pressed(), spritex, spritey)
            
            #print(local_character.getHealth())
            pygame.display.update()
            fpsClock.tick(FPS)


            
#Create room objects
medBayRoom = medBayRoom_pygame(itemsListMedBay)
cafeteriaRoom =cafeteriaRoom_pygame(itemsListCafeteria)
laundryRoom = laundryRoom_pygame(itemsListLaundry)
bossRoom = bossRoom_pygame(itemsListBoss)
commandCenterRoom = commandCenter_pygame(itemsListCommandCenter)
weaponsRoom = weaponsRoom_pygame(itemsListWeaponsRoom)
#Handles the main hallway and the detection for entering rooms
class Main:
    def __init__(self):
        pass
    def renderGame(self, character, backpack, base):
        renderText1 = False
        renderText2 = False
        local_backpack = backpack
        local_character = character
        local_base = base

        pygame.init()
        characterMovementObj = pygameMovement()
        FPS=120
        fpsClock=pygame.time.Clock()

        width=500
        height=500
        DISPLAYSURF=pygame.display.set_mode((width,height),0,32)
        pygame.display.set_caption('Main')
        #Render hallway background
        background=pygame.image.load('Original Backgrounds/RESIZED_Hallway_500x500.png')
        truebg=pygame.image.load('trueBGImg.png')
        sprite=pygame.image.load('newCharacter.png')
        #Interactive items
        laundryKey = InteractiveItem2('src\RESIZED_laundry_key.png', (0, 0), False)
        spoon = InteractiveItem2('src\RESIZED_Spoon.png', (0, 0), False)
        self.local_item_list=[]
        itemsList=[]

        
        #tkBossRoom = BossRoom(local_character, local_backpack, local_base, root)
        #tkBossRoom.Render_Canvas(local_backpack, local_character, local_base, root)
        #root.bind("<Escape>", lambda: mainRoom.renderGame(local_character, local_backpack, local_base))
        #root.iconify()
        #bossroomRendered = True

        spritex=240
        spritey=160
        while True:
            numSpoons = 0
            DISPLAYSURF.blit(truebg, (0,0))
            DISPLAYSURF.blit(background, (0,0))
            #renderGUI.renderGUI(self, local_character, DISPLAYSURF)
            DISPLAYSURF.blit(sprite,(spritex,spritey))
            #If the character tried to enter the laundry room without a laundry key
            if renderText1 and not renderText2: 
                font = pygame.font.SysFont(None, 30)
                noKeyText = font.render('Try getting a laundry key first.', True, (0, 0, 255))
                DISPLAYSURF.blit(noKeyText, (50,220))
            #If the character tried to enter the cafeteria without two spoons
            elif renderText2 and not renderText1:
                font = pygame.font.SysFont(None, 30)
                noKeyText = font.render('You need at least 2 spoons.', True, (0, 0, 255))
                DISPLAYSURF.blit(noKeyText, (50,220))
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE):
                        #End the game
                        pygame.quit()
                        return None
                #return self.local_item_list, local_character, local_backpack
                    if (event.key == pygame.K_y):
                        #Open backpack
                        backpackCreator.backpackFunction(self, local_backpack, DISPLAYSURF, self.local_item_list, itemsList, spritex, spritey, False)
                    if (event.key == pygame.K_e) and 85< spritex <200 and spritey < 70:
                        #If player is at the medbay location and presses E, move to the medbay room
                        #itemsListMedBay, local_character, local_backpack = medBayRoom.renderGame(local_character, local_backpack, local_base)
                        itemsListMedBay, local_character, local_backpack = medBayRoom.renderGame(local_character, local_backpack, local_base)
                    elif (event.key == pygame.K_e) and 300 < spritex < 415 and spritey < 70:
                        #If the player is at the laundry room entrance and presses E, check for the laundry key
                        #and move to the laundry room if yes. if not, render the error text
                        if laundryKey.simpleSearch(local_backpack.getItems()):
                            itemsListLaundry, local_character, local_backpack = laundryRoom.renderGame(local_character, local_backpack, local_base)
                        else:
                            renderText1 = True
                            renderText2 = False
                    elif (event.key == pygame.K_e) and 80 < spritex <200 and spritey > 300:
                        #If the character is at the weapons room door and presses E, move to weapons room
                        itemsListWeaponsRoom, local_character, local_backpack = weaponsRoom.renderGame(local_character, local_backpack, local_base)
                    elif (event.key == pygame.K_e) and spritex<90 and 120 <spritey<250:
                        #If the player is at the boss room door and presses E, move to the boss room
                        local_character, local_backpack = bossRoom.renderGame(local_character,local_backpack, local_base)
                    elif (event.key == pygame.K_e) and 280 < spritex < 380 and spritey > 320:
                        #If the player is at the cafeteria door, check the backpack for spoons and if the character has them, let them enter the cafeteria
                        for item in local_backpack.getItems():
                            if spoon.equals(item):
                                numSpoons=numSpoons+1
                        if numSpoons >= 2:
                            itemsListCafeteria, local_character, local_backpack = cafeteriaRoom.renderGame(local_character, local_backpack, local_base)
                            renderText2 = False
                            renderText1 = False
                        else: 
                            renderText1=False
                            renderText2=True
                    elif (event.key == pygame.K_e) and spritex > 370 and 135 <spritey < 225:
                        #If the player is at the command center door and presses E, move to command center
                        itemsListCommandCenter, local_character, local_backpack = commandCenterRoom.renderGame(local_character, local_backpack, local_base)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Mouse: {}, {}. Sprite: {}, {}".format(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], spritex, spritey))
            #update character position
            sprite, spritex, spritey = characterMovementObj.movesLikeJagger(pygame.time.get_ticks(), pygame.key.get_pressed(), spritex, spritey)
            
            #print(local_character.getHealth())
            pygame.display.update()
            fpsClock.tick(FPS)

#Start main and render the game
mainRoom = Main()
mainRoom.renderGame(local_character, local_backpack, local_base)