import pyautogui
import requests
import json
import random
import os
import threading
from pprint import pprint as pp
from pynput.keyboard import Key, Listener
from overlay import *
from win32api import GetSystemMetrics



class Poe(object):

    def __init__(self):

        self.POESESSID = "no"
        self.cookies = dict(POESESSID=self.POESESSID)
        self.accountName = "no"
        self.charName = "no"
        self.baseDict = self.getChaosRecipeRequirements()
        self.stash = "https://www.pathofexile.com/character-window/get-stash-items?league=Metamorph&realm=pc&accountName={0}&tabs=0&tabIndex=0".format(self.accountName)
        self.characterWindow = "https://www.pathofexile.com/character-window/get-items?accountName={0}&character={1}".format(self.accountName,self.charName)
        #Initial location and offsets for inventory
        self.setLocationValues()

    
    def getFacts(self):
        
        hwnd = win32gui.FindWindow(None, "Path Of Exile")

        rect = win32gui.GetWindowRect(hwnd)

        win32api.SetCursorPos((rect[2],rect[0]))

        self.poeX = rect[0]
        self.Po = rect[1]
        self.width = rect[2] - self.x
        self.height = rect[3] - self.y

    def setLocationValues(self):
        originStashX = 0.015625
        originStashY = 0.1614
        offsetStash = 0.01171875

        originInventoryX = 0.67578125
        originInventoryY = 0.56944444
        offsetInventory = offsetStash * 2

        self.xInventory = GetSystemMetrics(0) * originInventoryX
        self.yInventory = GetSystemMetrics(1) * originInventoryY
        self.xStash = GetSystemMetrics(0) * originStashX
        self.yStash = GetSystemMetrics(1) * originStashY
        self.offsetStash = GetSystemMetrics(0) * offsetStash
        self.offsetInventory = GetSystemMetrics(0) * offsetInventory


    def getChaosRecipeRequirements(self):

        itemTypeList = ["gloves","body_armour","helmet","ring","belt","boots","amulet","one_hand_weapon"]

        with open("base_items.json","r") as fh:
            data = json.loads(fh.read())

        baseDict = {
            "gloves":[],
            "body_armour":[],
            "helmet":[],
            "ring":[],
            "belt":[],
            "boots":[],
            "amulet":[],
            "one_hand_weapon":[]
        }

        keyList = list(data)

        for key in keyList:
            for item in itemTypeList:
                if item in data[key]['tags']:
                    baseDict[item].append(data[key]['name'])

        return baseDict




    def getChaosRecipe(self):    

        recipeList = ["gloves","body_armour","helmet","ring","ring","belt","boots","amulet","one_hand_weapon","one_hand_weapon"]

        response = requests.get(self.stash,cookies=self.cookies)

        jsonData = response.json()

        itemList = list()
        for item in jsonData['items']:
            for recipeItem in recipeList:
                if item['typeLine'] in self.baseDict[recipeItem]:

                    #TODO add logic for item level and rarity check.
                    # if(int(item['ilvl']) >= 70 ):
                    itemList.append((item['x'],item['y'],item['name']))
                    recipeList.remove(recipeItem)


        stash = pyautogui.locateOnScreen('images/stash.png', confidence=0.9)


        recipeClick = ["gloves","body_armour","helmet","ring","ring","belt","boots","amulet","one_hand_weapon","one_hand_weapon"]

        # if not (len(recipeList) > 0):

        if stash is not None:

            for item in itemList:
                print(item[2] + " Picked up")
                    
                noiseX = random.random() * 5
                noiseY = random.random() * 5

                xLoc = (self.xStash  + (self.offsetStash *  item[0]) + noiseX)
                yLoc = (self.yStash  + (self.offsetStash *  item[1]) + noiseY)

                pyautogui.moveTo(xLoc,yLoc)
                self.ctrlClick()
        else:
            print("Stash not open")
        # else:
        #     print("no full recipe")

    def ctrlClick(self):
        pyautogui.keyDown('ctrl')
        pyautogui.click()
        pyautogui.keyUp('ctrl')

    """
    Gets all inventory items for a character excluding wisdom and portal scrolls 
    returns as a list of items in tuple
    """

    def getInventory(self):

        response = requests.get(self.characterWindow,cookies=self.cookies)

        invDict = response.json()
        

        myItems = []

        for item in invDict['items']:
            if item['inventoryId'] == "MainInventory" and not (item["typeLine"] == "Scroll of Wisdom" or item["typeLine"] == "Portal Scroll"):
                myItems.append(item)



        return myItems

    """
    This function dumps the inventory that is generated in getInventory. 
    """

    def dumpInventory(self):


        myItems = self.getInventory()


        for item in myItems:
            print(item['name']  + " Dumped.")
            noiseX = random.random() 
            noiseY = random.random() 

            xLoc = (self.xInventory + (self.offsetInventory * item["x"]) + noiseX)
            yLoc = (self.yInventory + (self.offsetInventory * item["y"]) + noiseY)

            pyautogui.moveTo(xLoc,yLoc)
            self.ctrlClick()




if __name__ == '__main__':
    
    #Create the  
    poe = Poe()

    def on_press(key):

        if key == Key.f9:
            poe.getChaosRecipe()

        if key == Key.f10:
            poe.dumpInventory()

        if key == Key.f11:
            os._exit(1)

    #Starts the keyboard listener for function keys.
    listener = Listener(
           on_press=on_press)
    listener.start()

    #Start application, then start overlay.
    app = QApplication(sys.argv)
    overlay = Overlay()
    sys.exit(app.exec_())
