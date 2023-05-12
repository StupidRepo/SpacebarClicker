import pygame
import json
import random
import sys
from appdirs import user_data_dir
import os
# import pyautogui

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

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

scale = 1.35

# Create the window
screen_width, screen_height = round(1512/scale), round(1028/scale)
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

class Icon(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

    def draw(self, screenLol):
        screenLol.blit(self.image, self.rect)

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

dataToSave = """{
    "clicks": %s,
    "cpc": %s,
    "version": "%s"
}"""

def saveGame():
    with open(saveLocation, "w") as saveFile:
        saveFile.write(dataToSave % (clicks, cpc, version))
        saveFile.close()

def resetSaveGame(ourSpaces=None, ourCPC=None):
    os.remove(saveLocation)
    if ourSpaces is not None and ourCPC is not None:
        print("Resetting save file with spaces and cpc...")
        with open(saveLocation, "w") as saveFile:
            saveFile.write(dataToSave % (ourSpaces, ourCPC, version))
            saveFile.close()

def loadSavedGame():
    global clicks, cpc
    try:
        with open(saveLocation, "r") as saveFile:
            print("Save file found. Loading...")
            saveData = json.loads(saveFile.read())
            if saveData["version"] != version:
                print("Save file outdated! Saving spaces and cpc and resetting...")
                # if pyautogui.confirm("Your save file is outdated! You may experience issues with the game. Do you want to reset your save file?", "Outdated Save File", ["Yes", "No"]) == "Yes":
                resetSaveGame(saveData["clicks"], saveData["cpc"])
                print("Save file reset.")
                return sys.exit(1)
            clicks = saveData["clicks"]
            cpc = saveData["cpc"]
            saveFile.close()
            print("Save file loaded.")
    except FileNotFoundError:
        print("No save file found. Creating one...")
        saveGame()
        print("Save file created.")
    except KeyError:
        print("Save file is corrupted or outdated. Resetting...")
        # pyautogui.alert("Your save file is corrupted or outdated, and the game cannot find a value that should be present in your save file. It will now be reset.", "Corrupted/Outdated Save File")
        resetSaveGame()
        print("Save file reset.")
        return sys.exit(1)

running = True

loadSavedGame()

titleFont = 'assets/fonts/title.ttf'

descriptionText = makeText(getDescriptionText(), (255, 255, 255), pygame.font.Font(titleFont, textSizeDescription))

pygame.display.set_caption("Spacebar Clicker: %s (%s space%s)" % (version, clicks, '' if clicks == 1 else 's'))

clickSfxs = [pygame.mixer.Sound("assets/audio/gain1.wav"), pygame.mixer.Sound("assets/audio/gain2.wav"), pygame.mixer.Sound("assets/audio/gain3.wav"), pygame.mixer.Sound("assets/audio/gain4.wav"), pygame.mixer.Sound("assets/audio/gain5.wav")]

muted = False

def bleep():
    if not muted:
        random.choice(clickSfxs).play()

while running:
    screen.fill((155, 155, 155))
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

            if event.key == pygame.K_m:
                muted = not muted

            if event.key == pygame.K_SPACE:
                if impossible:
                    if random.random() < chanceToClick:
                        chanceToClick += 0.005
                        clicks += cpc
                        bleep()
                else:
                    clicks += cpc
                    bleep()
                pygame.display.set_caption("Spacebar Clicker: %s (%s space%s)" % (version, clicks, '' if clicks == 1 else 's'))
                descriptionText = makeText(getDescriptionText(), (255, 255, 255), pygame.font.Font(titleFont, textSizeDescription))

    cpcText = makeText(f"{cpc} spaces per click{f' (with a {chanceToClick * 100}% chance of a successful click)' if impossible else ''}", (255, 255, 255),
                               pygame.font.Font(titleFont, textSizeCPC))

    spaceText = makeText(f"{clicks} space{'' if clicks == 1 else 's'}", (255, 255, 255), pygame.font.Font(titleFont, textSizeClicks))

    Icon("assets/textures/mute.png" if muted else "assets/textures/unmute.png").draw(screen)

    screen.blit(spaceText, ((screen_width - spaceText.get_width()) // 2, 0))
    screen.blit(descriptionText, ((screen_width - descriptionText.get_width()) // 2, (textSizeDescription + textSizeClicks) + (textSizeClicks // 4) - textSizeClicks // 4))
    screen.blit(cpcText, ((screen_width - cpcText.get_width()) // 2, (textSizeDescription + textSizeClicks) + (textSizeClicks // 4) + 4 + textSizeDescription - textSizeClicks // 4))
    pygame.display.update()

# Clean up
pygame.quit()