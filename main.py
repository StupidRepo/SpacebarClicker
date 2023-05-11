import pygame
import json
import random
import sys
from appdirs import user_data_dir
import os

try:
    with open("version.txt", "r") as versionFile:
        version = versionFile.read()
        versionFile.close()
except FileNotFoundError:
    version = "Unknown"
baseLocation = user_data_dir("Spacebar Clicker", "Bradlee Barnes")
saveLocation = f"{baseLocation}/saveFile.json"
descriptionsLocation = "assets/core/descriptions.json"

if not os.path.exists(baseLocation):
    os.makedirs(baseLocation)

# Initialize pygame
pygame.init()

# Create the window
screen_width, screen_height = 1512, 1028
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Spacebar Clicker: %s (%s)" % (version, "Not Ready"))

lastChecked = -1

clicks = 0
cpc = 1
impossible = False
chanceToClick = 0.1

textSizeClicks = 52
textSizeDescription = 17
textSizeCPC = 15

try:
    with open(descriptionsLocation, "r") as descriptionsFile:
        descriptions = json.loads(descriptionsFile.read())
        descriptionsFile.close()
except FileNotFoundError:
    descriptions = [{
        "clicks": 0,
        "text": "An error has occured. Please re-download the game."
    }]


def getDescriptionText():
    descriptionString = ""
    if clicks >= sys.maxsize:
        return "You have reached the integer limit, which means you have officially beaten the game. It'll still work, but things may get buggy."
    for description in descriptions:
        if clicks >= description["clicks"]:
            descriptionString = description["text"]
            if 'impossible' in description:
                global impossible
                impossible = True
        if clicks <= description["clicks"]:
            break

    descriptionString = descriptionString.replace("{clicks}", str(clicks)).replace("{cpc}", str(cpc)).replace("{chanceToClick}", str(chanceToClick * 100)).replace("{version}", version).replace("{space}", "space" if clicks == 1 else "spaces").replace("{intlimit}", str(sys.maxsize)).replace('{untilintlimit}', str(sys.maxsize - clicks))
    return descriptionString

def makeText(text, color, font):
    return font.render(text, True, color)

def saveGame():
    with open(saveLocation, "w") as saveFile:
        saveFile.write("""{
    "clicks": %s,
    "cpc": %s
}""" % (clicks, cpc))
        saveFile.close()

def resetSaveGame():
    os.remove(saveLocation)

def loadSavedGame():
    global clicks, cpc
    try:
        with open(saveLocation, "r") as saveFile:
            print("Save file found. Loading...")
            saveData = json.loads(saveFile.read())
            clicks = saveData["clicks"]
            cpc = saveData["cpc"]
            saveFile.close()
            print("Save file loaded.")
    except FileNotFoundError:
        print("No save file found. Creating one...")
        saveGame()
        print("Save file created.")

running = True

loadSavedGame()

titleFont = 'assets/fonts/title.ttf'

descriptionText = makeText(getDescriptionText(), (255, 255, 255), pygame.font.Font(titleFont, textSizeDescription))

pygame.display.set_caption("Spacebar Clicker: %s (%s space%s)" % (version, clicks, '' if clicks == 1 else 's'))

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Saving game...")
            saveGame()
            print("Game saved. Exiting!")
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                print("Resetting game...")
                resetSaveGame()
                print("Game reset. Crashing!")
                running = False
                exec(type((lambda: 0).__code__)(0, 1, 0, 0, 0, b'', (), (), (), '', '', 1, b''))

            if event.key == pygame.K_SPACE:
                if impossible:
                    if random.random() < chanceToClick:
                        chanceToClick += 0.005
                        clicks += cpc
                else:
                    clicks += cpc
                pygame.display.set_caption("Spacebar Clicker: %s (%s space%s)" % (version, clicks, '' if clicks == 1 else 's'))
                descriptionText = makeText(getDescriptionText(), (255, 255, 255), pygame.font.Font(titleFont, textSizeDescription))

    cpcText = makeText(f"{cpc} spaces per click{f' (with a {chanceToClick * 100}% chance of a successful click)' if impossible else ''}", (255, 255, 255),
                               pygame.font.Font(titleFont, textSizeCPC))

    spaceText = makeText(f"{clicks} space{'' if clicks == 1 else 's'}", (255, 255, 255), pygame.font.Font(titleFont, textSizeClicks))

    screen.blit(spaceText, ((screen_width - spaceText.get_width()) // 2, textSizeClicks // 2))
    screen.blit(descriptionText, ((screen_width - descriptionText.get_width()) // 2, (textSizeDescription + textSizeClicks) + (textSizeClicks // 4) + 4))
    screen.blit(cpcText, ((screen_width - cpcText.get_width()) // 2, (textSizeDescription + textSizeClicks) + (textSizeClicks // 4) + 4 + textSizeDescription + 4))
    pygame.display.update()

# Clean up
pygame.quit()