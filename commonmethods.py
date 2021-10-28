from tkinter import *
from tkinter.ttk import * 
from PIL import Image
import os.path
from item import InteractiveItem
import random

"""
AG2021_1 CSE Choose Your Own Adventure
Group Members: Edmond, Shashwat, and Esben
Date: March 7, 2020
File task description: commonmethods.py serves as the host for the class CommonMethods, which contains methods that are commonly used by all the rooms in the game
to perform various functions such as picking up objects, consuming objects, making buttons visible, and character movement
Objects of this class are created in the separate room classes, one object per room
"""

global local_backpack
global local_character
global local_base
class CommonMethods:
    def __init__(self, backpack, character, base, objects, object_images, character_coordX, character_coordY, x, y, limits):
        #syncing up the backpack, base, and character objects
        global local_backpack
        global local_character
        global local_base
        local_backpack = backpack
        local_character = character
        local_base = base

        #list of interactive objects on the canvas
        self.objects = objects
        #list of Tkinter Canvas Images on the canvas
        self.object_images = object_images
        #self.pickup_btn = pickup_btn
        #self.canvas = canvas
        #character's initial coordinates
        self.character_coordX = character_coordX
        self.character_coordY = character_coordY
        #variables to hold movement increments
        self.x = x
        self.y = y
        #Character movement bounds describing the location of the walls of the room
        self.lower_x = limits[0]
        self.higher_x = limits[1]
        self.lower_y = limits[2]
        self.higher_y = limits[3]
        #self.character_image = image

    #Method for picking up an object on the canvas and placing it in the backpack
    def pickUpObject(self, canvas, pickup_btn, consume_btn):
        global local_backpack
        global local_character
        #Get the index in the self.objects list where the character is close to
        object_index = self.checkProximity(pickup_btn, consume_btn)
        #Add the object to the backpack
        local_backpack.addToPack(self.objects[object_index])
        #destroying the object from the canvas
        removed_tag = self.objects[object_index].getTag()
        canvas.delete(self.objects[object_index].getTag())
        #removing object from the list of objects in the medbay room
        self.objects.pop(object_index) 
        self.object_images.pop(object_index)
        print(object_index)
        #Hiding the pick-up button
        self.hideButton(pickup_btn, consume_btn)
        return removed_tag

    #Method for consuming objects
    def consumeObject(self, pickup_btn, consume_btn, canvas):
        global local_backpack
        global local_character
        #Get the index of the object in self.objects that the character is in close proximity to
        object_index = self.checkProximity(pickup_btn, consume_btn)
        #Retrieve the effects to character statistics that this object has
        effects = self.objects[object_index].getEffects()
        #apply effects to the character's statistics
        local_character.changeHealth(effects[0])
        local_character.changeArmor(effects[1])
        local_character.changeEndurance(effects[2])
        local_character.changeDPS(effects[3])
        local_character.updateStatCanvas()

    #Exposing the pickup button
    def exposeButton(self, n, pickup_btn):
        pickup_btn.config(state = NORMAL)
        pickup_btn.config(text = "pick up " + self.objects[n].getName())

    #Exposing the consume button
    def exposeConsumeButton(self, n, consume_btn):
        consume_btn.config(state = NORMAL)
        consume_btn.config(text = "consume " + self.objects[n].getName())

    #hiding both consume and pickup buttons
    def hideButton(self, pickup_btn, consume_btn):
        pickup_btn.config(state = DISABLED, text = 'pick up')
        consume_btn.config(state = DISABLED, text = 'consume')
        
    #method to handle character movement on the canvas
    def movement(self, canvas, character_image, pickup_btn, consume_btn): 
        global local_base
        global local_character
        # This is where the move() method is called 
        # This increments the character's position on the canvas by x, y
        canvas.move(character_image, self.x, self.y) 
        print(str(self.character_coordX)+", "+str(self.character_coordY))
        #check the proximity of the character again
        self.checkProximity(pickup_btn, consume_btn)
        #Update the health bar
        local_base.updateHealth()
        #Update the character's statistics
        local_character.updateStatCanvas()
      
    # for motion in negative x direction 
    def left(self, event, canvas, image, pickup_btn, consume_btn): 
        if self.character_coordX > self.lower_x:
            self.x = -2.5
            self.y = 0
            #Updating absolute character coordinates
            self.character_coordX += -2.5
            self.movement(canvas, image, pickup_btn, consume_btn)
        
      
    # for motion in positive x direction 
    def right(self, event, canvas, image, pickup_btn, consume_btn): 
        if self.character_coordX < self.higher_x:
            self.x = 2.5
            self.y = 0
            #Updating absolute character coordinates
            self.character_coordX += 2.5
            self.movement(canvas, image, pickup_btn, consume_btn)
      
    # for motion in positive y direction 
    def up(self, event, canvas, image, pickup_btn, consume_btn): 
        if self.character_coordY > self.lower_y:
            self.x = 0
            self.y = -2.5
            #Updating absolute character coordinates
            self.character_coordY += -2.5
            self.movement(canvas, image, pickup_btn, consume_btn)
        
    # for motion in negative y direction 
    def down(self, event, canvas, image, pickup_btn, consume_btn): 
        if self.character_coordY < self.higher_y:
            self.x = 0
            self.y = 2.5
            #Updating absolute character coordinates
            self.character_coordY += 2.5
            self.movement(canvas, image, pickup_btn, consume_btn)

    #Method for returning the character, backpack, and base objects to the main file when the room is being exited
    def sendObjects(self):
        global local_backpack, local_character, local_base
        return local_character, local_backpack, local_base

    #Method for checking the proximity of the character to any interactive objects on the canvas
    def checkProximity(self, pickup_btn, consume_btn):
        #Iterate through the objects in the room
        found = False
        for n in range(len(self.objects)):
            #Get the range of x and y values where the character is able to pick up the object
            xrange = self.objects[n].getXBounds()
            yrange = self.objects[n].getYBounds()
            print(self.objects[n].getName(), xrange, yrange)
            #If the character's coordinates are within both the x and y coordinate ranges, allow them to pick up the item
            if self.character_coordX >= xrange[0] and self.character_coordX <= xrange[1] and self.character_coordY >= yrange[0] and self.character_coordY <= yrange[1] and self.objects[n].getVisibility():
                if self.objects[n].getType() == 'pickupable' and len(local_backpack.getItems()) < local_backpack.getSize():
                    self.exposeButton(n, pickup_btn)
                    return n
                elif self.objects[n].getType() == 'consumable' and len(local_backpack.getItems()) < local_backpack.getSize():
                    self.exposeConsumeButton(n, consume_btn)
                    return n
            else:
                self.hideButton(pickup_btn, consume_btn)

    # method to handle the dropping of objects into a room from the backpack
    # caller can specify position if they want to, otherwise it's random
    def dropObject(self, removed_object, backpack, canvas, newX = None, newY = None):
        global local_backpack
        local_backpack = backpack
        #If no coordinates were specified, generate random ones within the possible movement area for the character
        if newX == None:
            newX = random.randint(self.lower_x + 30, self.higher_x - 30)
        if newY == None:
            newY = random.randint(self.lower_y + 30, self.higher_y - 30)
        #Set the bounds of detection for the new object
        xTop = newX + 10
        xBottom = newX - 10
        yTop = newY + 10
        yBottom = newY - 10

        #basically duplicating removed_object but with a new location in the room grid
        new_object = InteractiveItem(xBottom, 
            xTop, 
            yBottom,
            yTop,
            removed_object.getName(),
            removed_object.getImageFilename(),
            newX,
            newY,
            removed_object.getIconFilename(), 
            removed_object.getType(), 
            True,
            (removed_object.getTag()), 
            removed_object.getEffects()[0],
            removed_object.getEffects()[1],
            removed_object.getEffects()[2],
            removed_object.getEffects()[3]
        )
        #self.objects contains a list of all the InteractiveItem objects in a room; add the new object to the list
        self.objects.append(new_object)
        #adding this new object to the canvas
        self.object_images.append(canvas.create_image(new_object.getX(), new_object.getY(), image = new_object.getPhotoImage(), anchor = 'c', tags = (new_object.getTag())))

    #Setting the coordinates of the character at the entering of the player into the room, since the coordinates of the character from when they left the room have been preserved,
    #even though the character always starts at 250, 250
    def setCoordinates(self, pos):
        self.character_coordX, self.character_coordY = pos