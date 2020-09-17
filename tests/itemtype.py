import json
import requests

accountName = "jack13371"

charName = "yuhyeetdab"

POESESSID = "b568458170f3e4ad35602f462b414362"

cookies = dict(POESESSID=POESESSID)

characterWindow = "https://www.pathofexile.com/character-window/get-items?accountName={0}&character={1}".format(accountName,charName)

stash = "https://www.pathofexile.com/character-window/get-stash-items?league=Standard&realm=pc&accountName={0}&tabs=0&tabIndex=0".format(accountName,charName)



def getChaosRecipeRequirements():

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



def getChaosRecipe(baseDict):    

    recipeList = ["gloves","body_armour","helmet","ring","ring","belt","boots","amulet","one_hand_weapon","one_hand_weapon"]

    recipeDict = {
        "gloves":[],
        "body_armour":[],
        "helmet":[],
        "ring":[],
        "belt":[],
        "boots":[],
        "amulet":[],
        "one_hand_weapon":[]
    }


    response = requests.get(characterWindow,cookies=cookies)

    jsonData = response.json()

    for item in jsonData['items']:
        for recipeItem in recipeList:
            if item['typeLine'] in baseDict[recipeItem]:
                    recipeDict[recipeItem].append(item['name'])
                    recipeList.remove(recipeItem)

    print(recipeDict)
    


baseDict = getChaosRecipeRequirements()
getChaosRecipe(baseDict)