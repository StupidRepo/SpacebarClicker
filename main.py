import colorsys
import time

import pygame
import json
import random
import sys
from appdirs import user_data_dir
import os
from glob import glob

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

pygame.init()

scale = 1.4
resizeable = False

def makeText(text, color, font):
    return font.render(text, False, color)

screen_width, screen_height = round(1512/scale), round(1028/scale)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Spacebar Clicker: %s (%s)" % (version, "Loading game..."))

lastChecked = -1

muted = False

clicks = 0
cpc = 1
impossible = False
chanceToClick = 0.1

textSizeClicks = 52
textSizeDescription = 19
textSizeCPC = 19

lastText = ""

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
    global lastText
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

    if descriptionString != lastText and clicks > 10:
        lastText = descriptionString
        trolled = getSoundByName("newdescription", "special")
        if trolled is not None: trolled.play()
    descriptionString = descriptionString.replace("{clicks}", str(clicks)).replace("{cpc}", str(cpc)).replace("{chanceToClick}", str(chanceToClick * 100)).replace("{version}", version).replace("{space}", "space" if clicks == 1 else "spaces").replace("{intlimit}", str(sys.maxsize)).replace('{untilintlimit}', str(sys.maxsize - clicks))
    return descriptionString

sounds = None

def initSounds():
    global sounds
    thisSounds = {}
    for sound in glob("assets/audio/**/*.wav"):
        folderName = sound.split("/")[2]
        if folderName not in thisSounds:
            thisSounds[folderName] = []
        thisSounds[folderName].append({
            "name": os.path.basename(sound).replace(".wav", ""),
            "sound": pygame.mixer.Sound(sound)
        })
    for sound in glob("assets/audio/**/*.ogg"):
        folderName = sound.split("/")[2]
        if folderName not in thisSounds:
            thisSounds[folderName] = []
        thisSounds[folderName].append({
            "name": os.path.basename(sound).replace(".ogg", ""),
            "sound": pygame.mixer.Sound(sound)
        })
    sounds = thisSounds

initSounds()

def getSoundByName(name, folder):
    if sounds is not None:
        if not muted:
            for soundObject in sounds[folder]:
                if soundObject["name"] == name:
                    return soundObject["sound"]
    return None

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
                resetSaveGame(saveData["clicks"], saveData["cpc"])
                print("Save file reset.")
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
        resetSaveGame()
        print("Save file reset.")
        saveGame()
    except Exception as err:
        print("Unknown error. Please make an issue on the GitHub. Error: %s" % err)
        sys.exit(255)

running = True

loadSavedGame()

titleFont = 'assets/fonts/title.ttf'

descriptionText = makeText(getDescriptionText(), (255, 255, 255), pygame.font.Font(titleFont, textSizeDescription))

pygame.display.set_caption("Spacebar Clicker: %s (%s space%s)" % (version, clicks, '' if clicks == 1 else 's'))

muted = False

def bleep():
    if not muted:
        random.choice(sounds["clicks"])["sound"].play()

def ambient():
    random.choice(sounds["ambient"])["sound"].play()

def superclick():
    theSound = getSoundByName("superclick", "special")
    if theSound is not None:
        theSound.play()

def megaclick():
    theSound = getSoundByName("megaclick", "special")
    if theSound is not None:
        theSound.play()

percentFontClass = pygame.font.Font(titleFont, 17)
descFontClass = pygame.font.Font(titleFont, textSizeDescription)
cpcFontClass = pygame.font.Font(titleFont, textSizeCPC)
spaceFontClass = pygame.font.Font(titleFont, textSizeClicks)

initSounds()

AMBIENT_EVENT_TIME_MIN = 60*1000
AMBIENT_EVENT_TIME_MAX = 300*1000

SUPERCLICK_EVENT_TIME_MIN = 2*1000
SUPERCLICK_EVENT_TIME_MAX = 2*1000

AMBIENT_EVENT, AMBIENT_EVENT_TIME = pygame.USEREVENT + 1, random.randint(AMBIENT_EVENT_TIME_MIN, AMBIENT_EVENT_TIME_MAX)
SUPERCLICK_EVENT, SUPERCLICK_EVENT_TIME = pygame.USEREVENT + 2, random.randint(SUPERCLICK_EVENT_TIME_MIN, SUPERCLICK_EVENT_TIME_MAX)
pygame.time.set_timer(AMBIENT_EVENT, AMBIENT_EVENT_TIME, 1)
pygame.time.set_timer(SUPERCLICK_EVENT, SUPERCLICK_EVENT_TIME, 1)

superClicks = 0
maxSuperClicksUntilMegaClick = random.randint(20, 50)

secretMusicEnabled = False
secretMusic = getSoundByName("secretmusic", "special")

rainbowSpeed = 20

while running:
    barColour = colorsys.hsv_to_rgb((time.time() / rainbowSpeed) % 1, 1, 1)
    barColour = (round(barColour[0] * 255), round(barColour[1] * 255), round(barColour[2] * 255))

    megaClickFormula = round(10 * (cpc // 2) + max((clicks // 20), 10))
    screen.fill((155, 155, 155))

    pygame.draw.rect(screen, barColour, (screen.get_width() // 4 - ((screen.get_width() // 4) / 1), screen.get_height() - 50, (screen.get_width() // 1) * (superClicks / maxSuperClicksUntilMegaClick), 30), 0, 3, 3, 3, 3)
    pygame.draw.rect(screen, (255, 255, 255), (screen.get_width() // 4 - ((screen.get_width() // 4) / 1), screen.get_height() - 50, screen.get_width() // 1, 30), 3, 3, 3, 3, 3)

    superClicksText = makeText(f"Megaclick will give you +{megaClickFormula} clicks! ({round(superClicks/maxSuperClicksUntilMegaClick * 100, 2)}% - {superClicks}/{maxSuperClicksUntilMegaClick})", (255, 255, 255), percentFontClass)
    screen.blit(superClicksText, ((screen.get_width() - superClicksText.get_width()) // 2, screen.get_height() - 50 - 20))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Saving game...")
            saveGame()
            print("Game saved. Exiting!")
            running = False
        if event.type == AMBIENT_EVENT:
            ambient()
            if not impossible:
                clicks += 100 * cpc
            cpc += 1
            AMBIENT_EVENT_TIME = random.randint(AMBIENT_EVENT_TIME_MIN, AMBIENT_EVENT_TIME_MAX)
            pygame.time.set_timer(AMBIENT_EVENT, AMBIENT_EVENT_TIME, 1)
        if event.type == SUPERCLICK_EVENT:
            superClicks += 1
            superclick()
            clicks += 10 * cpc
            SUPERCLICK_EVENT_TIME = random.randint(SUPERCLICK_EVENT_TIME_MIN, SUPERCLICK_EVENT_TIME_MAX)
            pygame.time.set_timer(SUPERCLICK_EVENT, SUPERCLICK_EVENT_TIME, 1)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                muted = not muted

            if event.key == pygame.K_c:
                screen = pygame.display.set_mode((screen_width, screen_height),
                                                 flags=(pygame.RESIZABLE if resizeable else 0))

            if event.key == pygame.K_f:
                resizeable = not resizeable
                screen = pygame.display.set_mode((screen.get_width(), screen.get_height()),
                                                 flags=(pygame.RESIZABLE if resizeable else 0))

            if event.key == pygame.K_h:
                if pygame.key.get_pressed()[pygame.K_e] and pygame.key.get_pressed()[pygame.K_l] and pygame.key.get_pressed()[pygame.K_p]:
                    secretMusicEnabled = not secretMusicEnabled
                    if secretMusicEnabled:
                        secretMusic.play(-1)
                    else:
                        secretMusic.stop()

            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_BACKSPACE:
                if impossible:
                    if random.random() < chanceToClick:
                        chanceToClick += 0.005
                        clicks += cpc
                        bleep()
                else:
                    if random.random() < 0.05:
                        superClicks += 1
                    clicks += cpc
                    bleep()
                descriptionText = makeText(getDescriptionText(), (255, 255, 255), descFontClass)

    if superClicks > maxSuperClicksUntilMegaClick:
        superClicks = 0
        megaclick()
        clicks += megaClickFormula
        maxSuperClicksUntilMegaClick = random.randint(40, 80)

    clicks = min(clicks, sys.maxsize)
    pygame.display.set_caption(
        "Spacebar Clicker: %s (%s space%s)" % (version, clicks, '' if clicks == 1 else 's'))

    cpcText = makeText(f"{cpc} spaces per click{f' (with a {round(chanceToClick * 100, 1)}% chance of a successful click)' if impossible else ''}", (255, 255, 255), cpcFontClass)
    cpsText = makeText(f"{10 * cpc} spaces per {round(SUPERCLICK_EVENT_TIME / 1000, 3)} seconds", (255, 255, 255), cpcFontClass)
    spaceText = makeText(f"{clicks} space{'' if clicks == 1 else 's'}", (255, 255, 255), spaceFontClass)

    Icon("assets/textures/mute.png" if muted else "assets/textures/unmute.png").draw(screen)

    if pygame.key.get_pressed()[pygame.K_RSHIFT] and pygame.key.get_pressed()[pygame.K_LSHIFT] and pygame.key.get_pressed()[pygame.K_x]:
        resetSaveGame()
        running = False

    screen.blit(spaceText, ((screen.get_width() - spaceText.get_width()) // 2, 0))
    screen.blit(descriptionText, ((screen.get_width() - descriptionText.get_width()) // 2, (textSizeDescription + textSizeClicks) + (textSizeClicks // 4) + 4 + textSizeDescription - textSizeClicks - textSizeClicks // 8))
    screen.blit(cpcText, ((screen.get_width() - cpcText.get_width()) // 2, (textSizeDescription + textSizeClicks) + (textSizeClicks // 4) + 4 + textSizeDescription - textSizeClicks // 1.4))
    screen.blit(cpsText, ((screen.get_width() - cpsText.get_width()) // 2, (textSizeDescription + textSizeClicks) + (textSizeClicks // 4) + 4 + textSizeDescription - textSizeClicks // 1.4 + textSizeCPC))
    pygame.display.update()

pygame.quit()