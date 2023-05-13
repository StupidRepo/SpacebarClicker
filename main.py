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

# Initialize pygame
pygame.init()

scale = 1.4
resizeable = False

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
textSizeDescription = 19
textSizeCPC = 19

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

sounds = {}

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

def getSoundByName(name, folder):
    if not muted:
        for soundObject in sounds[folder]:
            if soundObject["name"] == name:
                return soundObject["sound"]
    return None

def makeText(text, color, font):
    return font.render(text, False, color)

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

muted = False

def bleep():
    if not muted:
        random.choice(sounds["clicks"])["sound"].play()

def ambient():
    # if not muted:
    random.choice(sounds["ambient"])["sound"].play()

def superclick():
    theSound = getSoundByName("superclick", "special")
    if theSound is not None:
        theSound.play()

def megaclick():
    theSound = getSoundByName("megaclick", "special")
    if theSound is not None:
        theSound.play()

percentFontClass = pygame.font.Font(titleFont, 16)
descFontClass = pygame.font.Font(titleFont, textSizeDescription)
cpcFontClass = pygame.font.Font(titleFont, textSizeCPC)
spaceFontClass = pygame.font.Font(titleFont, textSizeClicks)

initSounds()

# print(sounds)

AMBIENT_EVENT_TIME_MIN = 60*1000
AMBIENT_EVENT_TIME_MAX = 300*1000

SUPERCLICK_EVENT_TIME_MIN = 3*1000
SUPERCLICK_EVENT_TIME_MAX = 3*1000

AMBIENT_EVENT, AMBIENT_EVENT_TIME = pygame.USEREVENT + 1, random.randint(AMBIENT_EVENT_TIME_MIN, AMBIENT_EVENT_TIME_MAX)
SUPERCLICK_EVENT, SUPERCLICK_EVENT_TIME = pygame.USEREVENT + 2, random.randint(SUPERCLICK_EVENT_TIME_MIN, SUPERCLICK_EVENT_TIME_MAX)
pygame.time.set_timer(AMBIENT_EVENT, AMBIENT_EVENT_TIME, 1)
pygame.time.set_timer(SUPERCLICK_EVENT, SUPERCLICK_EVENT_TIME, 1)

superClicks = 0
maxSuperClicksUntilMegaClick = random.randint(7, 10)

barColour = (255 - (255 * (superClicks / maxSuperClicksUntilMegaClick)), 100 + (155 * (superClicks / maxSuperClicksUntilMegaClick)), 100)

secretMusicEnabled = False
secretMusic = getSoundByName("secretmusic", "special")

while running:
    megaClickFormula = round(1000 * cpc * min(max((clicks / 1000) / 50, 1), 100))
    screen.fill((155, 155, 155))
    barColour = (255 - (255 * (superClicks / maxSuperClicksUntilMegaClick)), 100 + (155 * (superClicks / maxSuperClicksUntilMegaClick)), 100)

    pygame.draw.rect(screen, barColour, (screen.get_width() // 2 - ((screen.get_width() // 2) / 2), screen.get_height() - 50, (screen.get_width() // 2) * (superClicks / maxSuperClicksUntilMegaClick), 30), 0, 4, 4, 4, 4)
    pygame.draw.rect(screen, (255, 255, 255), (screen.get_width() // 2 - ((screen.get_width() // 2) / 2), screen.get_height() - 50, screen.get_width() // 2, 30), 4, 4, 4, 4, 4)

    superClicksText = makeText(f"Megaclick will give you +{megaClickFormula} clicks! ({round(superClicks/maxSuperClicksUntilMegaClick * 100, 2)}% - {superClicks}/{maxSuperClicksUntilMegaClick})", (255, 255, 255), percentFontClass)
    screen.blit(superClicksText, (screen.get_width() // 2 - ((screen.get_width() // 2) / 2) + 4, screen.get_height() - 50 - 20))
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
            if superClicks > maxSuperClicksUntilMegaClick:
                megaclick()
                SUPERCLICK_EVENT_TIME_MIN = max(SUPERCLICK_EVENT_TIME_MIN - 250, 1000)
                SUPERCLICK_EVENT_TIME_MAX = max(SUPERCLICK_EVENT_TIME_MAX - 250, 1000)
                clicks += megaClickFormula
                superClicks = 0
                maxSuperClicksUntilMegaClick = random.randint(round(10*SUPERCLICK_EVENT_TIME_MIN/1000), round(30*SUPERCLICK_EVENT_TIME_MIN/1000))
            else:
                superclick()
                clicks += 10 * cpc
            SUPERCLICK_EVENT_TIME = random.randint(SUPERCLICK_EVENT_TIME_MIN, SUPERCLICK_EVENT_TIME_MAX)
            pygame.time.set_timer(SUPERCLICK_EVENT, SUPERCLICK_EVENT_TIME-1*1000, 1)
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
                    clicks += cpc
                    bleep()
                descriptionText = makeText(getDescriptionText(), (255, 255, 255), descFontClass)

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

# Clean up
pygame.quit()