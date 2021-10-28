from tkinter import *
from tkinter.ttk import * 
from PIL import Image
import os.path
import matplotlib.pyplot as plt
import pygame

"""
AG2021_1 CSE Choose Your Own Adventure
Group Members: Edmond, Shashwat, and Esben
Date: March 7, 2020
File task description: item.py is the python file that hosts the classes InteractiveItem and PressurePlate, which handle interactive object methods and washing machine pressure
plates, respectively. 
InteractiveItem contains all the attributes of the object, including things like the image that is used for the canvas and for the backpack, the ranges of detection, the 
geographic position where the object is placed on the canvas, the type of object 'pickupable' or 'consumable'
PressurePlate contains the attributes of a pressure plate, only currently used in the laundry room to detect if the player is standing near a washing machine
"""

class InteractiveItem():
    def __init__(self, startX, endX, startY, endY, itemName, itemImage, posX, posY, iconFilename, object_type, visible, tag, health_effect = 0, armor_effect = 0, dps_effect = 0, endurance_effect = 0):
        self.startX = startX
        self.endX = endX
        self.startY = startY
        self.endY = endY
        self.name = itemName
        self.image_filename = itemImage
        self.icon_filename = iconFilename
        self.image_height = len(plt.imread(self.image_filename).copy())
        self.image_width = len(plt.imread(self.image_filename).copy()[0])

        self.Photoimage = PhotoImage(file = self.image_filename)  #PhotoImage object
        self.icon_Photoimage = PhotoImage(file = self.icon_filename)
        self.X = posX
        self.Y = posY
        self.fulldirectory = os.path.join(os.getcwd(), self.image_filename)
        self.type = object_type
        self.health_effect = health_effect
        self.armor_effect = armor_effect
        self.dps_effect = dps_effect
        self.endurance_effect = endurance_effect
        self.visible = visible
        self.tag = tag

    def getTag(self):
        return self.tag

    #when the canvas is rendered, the object will only show up if this attribute is true
    def toggleVisible(self):
        if self.visible:
            self.visible = False
        else:
            self.visible = True
        return self.visible

    def getVisibility(self):
        return self.visible
    #returns X bounds of detection
    def getXBounds(self):
        return (self.startX, self.endX)
    #returns Y bounds of detection
    def getYBounds(self):
        return (self.startY, self.endY)

    #the name of the object shown on the buttons when the character is hovered over it
    def getName(self):
        return self.name
    #returns the PhotoImage used to place the object on the canvas visibly
    def getPhotoImage(self):
        return self.Photoimage
    #returns the file path for the object's image
    def getImageFilename(self):
        return self.image_filename
    #returns the PIL image
    def getPILImage(self):
        image = Image.open(self.fulldirectory)
        return image
    #returns the file path of the backpack icon used
    def getIconFilename(self):
        return self.icon_filename
    #returns the PhotoImage object containing the backpack icon
    def getIconImage(self):
        return self.icon_Photoimage
    #returns the object's X position on the canvas
    def getX(self):
        return self.X
    #returns the object's Y position on the canvas
    def getY(self):
        return self.Y
    #returns the object's type: 'pickupable' or 'consumable', which determines how the character can interact with it
    def getType(self):
        return self.type
    #Used to change the type of object without making a new one
    def setType(self, type):
        self.type = type
        return self.type
    #Returns the character statistic effects that consuming this object would have. 
    #For 'pickupables', all are 0
    def getEffects(self):
        return (self.health_effect, self.armor_effect, self.endurance_effect, self.dps_effect)

class PressurePlate:
    def __init__(self, startX, endX, startY, endY, x, y, name, available):
        #Bounds of detection
        self.startX = startX
        self.endX = endX
        self.startY = startY
        self.endY = endY
        #Position on the canvas
        self.X = x
        self.Y = y
        #name
        self.name = name
        #Whether the pressure plate can be activated or not
        self.available = available

    def getName(self):
        return self.name

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

    def getXBounds(self):
        return (self.startX, self.endX)

    def getYBounds(self):
        return (self.startY, self.endY)

    def getAvailability(self):
        return self.available