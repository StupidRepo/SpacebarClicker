import colorsys
import time

import pygame
import json
import random
import sys
from appdirs import user_data_dir
import os
from glob import glob
from enum import Enum

class Colours(Enum):
    ERR = (255, 100, 100)
    WARN = (255, 255, 100)
    INFO = (100, 100, 255)
    GOOD = (100, 255, 100)

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

maximumFallenKeys = 3000
maxConsoleTexts = 7
timeBeforeDeleteConsoleTexts = 4
minForUltra = maximumFallenKeys / 2

pygame.init()

iconsGroup = pygame.sprite.Group()
fontSizeConsole = 18
consoleFont = pygame.font.Font("assets/fonts/title.ttf", fontSizeConsole)

delta = 1

settings = json.loads(open("assets/core/settings.json", "r").read())
debugConsoleEnabled = settings["console"]

def makeText(text, color, font):
    return font.render(text, False, color)

class DebugConsole():
    def __init__(self) -> None:
        self.texts = []
        pass
    
    def log(self, text, colour=Colours.INFO):
        if debugConsoleEnabled:
            if len(self.texts) > maxConsoleTexts:
                self.texts.pop(0)
            self.texts.append({
                "text": text,
                "colour": colour.value,
                "time": time.time()
            })
    
    def draw(self, screen):
        if debugConsoleEnabled:
            surf = pygame.Surface((screen.get_width(), fontSizeConsole * len(self.texts)))
            surf.set_alpha(180)
            surf.fill((64, 64, 64))
            screen.blit(surf, (0, screen.get_height()-(fontSizeConsole * len(self.texts))))
            for text in self.texts:
                screen.blit(makeText(text["text"], text["colour"], consoleFont), (0, screen.get_height()-(self.texts.index(text) * fontSizeConsole)-fontSizeConsole))
                if time.time() - text["time"] > timeBeforeDeleteConsoleTexts:
                    self.texts.remove(text)

class FallenKey(pygame.sprite.Sprite):
    # constructor
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.transform.scale(self.image, (round(self.rect.width / 2), round(self.rect.height / 2)))
        self.speed = random.uniform(0.1, 0.05) * delta

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > screen.get_height() + 25:
            self.kill()

fallenKeys = pygame.sprite.Group()
keyImages = glob("assets/textures/keys/*.png")

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

scale = 1.4
resizeable = False

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
    def __init__(self, imageTrue, imageFalse, variable, x=0, y=0):
        super().__init__()
        self.image = pygame.image.load(imageTrue if variable else imageFalse)
        self.rect = self.image.get_rect()
        self.rect.x = x + (48 * len(iconsGroup)) + 8 if len(iconsGroup) > 0 else x
        self.rect.y = y
        self.varString = variable
        self.var = globals()[variable]
        self.imageTrue = imageTrue
        self.imageFalse = imageFalse
        # self.x = x + (48 * len(iconsGroup)) + 8

    def update(self):
        self.image = pygame.image.load(self.imageTrue if globals()[self.varString] else self.imageFalse)

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
    console.log("Saving game...")
    with open(saveLocation, "w") as saveFile:
        saveFile.write(dataToSave % (clicks, cpc, version))
        saveFile.close()
        console.log("Game saved!", Colours.GOOD)

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
antikey = False

# def ultraclick():
#     global clicks, cpc
#     soundUltra = getSoundByName("ultraclick", "special")
#     if soundUltra is not None:
#         soundUltra.play()
#     clicks *= 3
#     cpc *= 2

def fall(isMClick=False):
    fallenX = random.randint(50, screen.get_width() - 50)
    if not isMClick:
        fallenY = random.randint(0, 48*2)
    else:
        fallenY = random.randint(0, 48*8)
    fallenKey = FallenKey(random.choice(keyImages), fallenX, fallenY)
    fallenKeys.add(fallenKey)

def bleep():
    fall()
    # if len(fallenKeys) > minForUltra:
        # fallenKeys.empty()
        # ultraclick()
    if not muted:
        random.choice(sounds["clicks"])["sound"].play()

def ambient():
    random.choice(sounds["ambient"])["sound"].play()

def superclick():
    theSound = getSoundByName("superclick", "special")
    if theSound is not None:
        theSound.play()
    for i in range(random.randint(2, 5)):
        fall()

def megaclick():
    theSound = getSoundByName("megaclick", "special")
    if theSound is not None:
        theSound.play()
    for i in range(random.randint(500, 1000)):
        fall(True)


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
AUTOSAVE_EVENT, AUTOSAVE_EVENT_TIME = pygame.USEREVENT + 3, 60*1000
pygame.time.set_timer(AMBIENT_EVENT, AMBIENT_EVENT_TIME, 1)
pygame.time.set_timer(SUPERCLICK_EVENT, SUPERCLICK_EVENT_TIME, 1)

superClicks = 0
maxSuperClicksUntilMegaClick = random.randint(20, 50)

secretMusicEnabled = False
secretMusic = getSoundByName("secretmusic", "special")

rainbowSpeed = 20

clock = pygame.time.Clock()

iconsGroup.add(Icon("assets/textures/mute.png", "assets/textures/unmute.png", 'muted'))
iconsGroup.add(Icon("assets/textures/antikey.png", "assets/textures/key.png", 'antikey'))

console = DebugConsole()

lastSave = time.time()

console.log("Welcome to Spacebar Clicker! Press - or = to change font size of console.", Colours.GOOD)

chaos = False

while running:
    try:
        barColour = colorsys.hsv_to_rgb((time.time() / rainbowSpeed) % 1, 1, 1)
        barColour = (round(barColour[0] * 255), round(barColour[1] * 255), round(barColour[2] * 255))

        megaClickFormula = round(10 * (cpc // 2) + max((clicks // 20), 10))
        screen.fill((155, 155, 155))

        fallenKeys.update()
        if len(fallenKeys) > 0 and not antikey:
            fallenKeys.draw(screen)
        if len(fallenKeys) > maximumFallenKeys:
            fallenKeys.remove(fallenKeys.sprites()[0])

        pygame.draw.rect(screen, barColour, (screen.get_width() // 4 - ((screen.get_width() // 4) / 1), screen.get_height() - 50, (screen.get_width() // 1) * (superClicks / maxSuperClicksUntilMegaClick), 30), 0, 3, 3, 3, 3)
        pygame.draw.rect(screen, (255, 255, 255), (screen.get_width() // 4 - ((screen.get_width() // 4) / 1), screen.get_height() - 50, screen.get_width() // 1, 30), 3, 3, 3, 3, 3)

        superClicksText = makeText(f"Megaclick will give you +{megaClickFormula:,} clicks! ({round(superClicks/maxSuperClicksUntilMegaClick * 100, 2)}% - {superClicks}/{maxSuperClicksUntilMegaClick})", (255, 255, 255), percentFontClass)
        screen.blit(superClicksText, ((screen.get_width() - superClicksText.get_width()) // 2, screen.get_height() - 50 - 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Saving game...")
                saveGame()
                print("Game saved. Exiting!")
                running = False
            if event.type == AUTOSAVE_EVENT:
                saveGame()
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

                # shitty fullscreen which doesn't work on macOS :/
                # if event.key == pygame.K_o:
                        # screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), flags=(pygame.FULLSCREEN))
                
                if event.key == pygame.K_h:
                    chaos = not chaos

                if event.key == pygame.K_s:
                    saveGame()
                
                if event.key == pygame.K_a:
                    antikey = not antikey

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
                
                if event.key == pygame.K_MINUS:
                    fontSizeConsole -= 2
                    consoleFont = pygame.font.Font("assets/fonts/title.ttf", fontSizeConsole)
                    console.log("Font size changed to " + str(fontSizeConsole) + "!", Colours.GOOD)

                if event.key == pygame.K_EQUALS:
                    fontSizeConsole += 2
                    consoleFont = pygame.font.Font("assets/fonts/title.ttf", fontSizeConsole)
                    console.log("Font size changed to " + str(fontSizeConsole) + "!", Colours.GOOD)

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
            "Spacebar Clicker: %s (%s space%s)" % (version, f'{clicks:,}', '' if clicks == 1 else 's'))

        cpcText = makeText(f"{cpc:,} spaces per click{f' (with a {round(chanceToClick * 100, 1)}% chance of a successful click)' if impossible else ''}", (255, 255, 255), cpcFontClass)
        cpsText = makeText(f"{(10 * cpc):,} spaces per {round(SUPERCLICK_EVENT_TIME / 1000, 3)} seconds", (255, 255, 255), cpcFontClass)
        spaceText = makeText(f"{clicks:,} space{'' if clicks == 1 else 's'}", (255, 255, 255), spaceFontClass)

        iconsGroup.update()
        iconsGroup.draw(screen)

        if pygame.key.get_pressed()[pygame.K_RSHIFT] and pygame.key.get_pressed()[pygame.K_LSHIFT] and pygame.key.get_pressed()[pygame.K_x]:
            resetSaveGame()
            running = False

        if chaos and random.random() < 0.8:
            for i in range(20):
                fall(True)

        screen.blit(spaceText, ((screen.get_width() - spaceText.get_width()) // 2, 0))
        screen.blit(descriptionText, ((screen.get_width() - descriptionText.get_width()) // 2, (textSizeDescription + textSizeClicks) + (textSizeClicks // 4) + 4 + textSizeDescription - textSizeClicks - textSizeClicks // 8))
        screen.blit(cpcText, ((screen.get_width() - cpcText.get_width()) // 2, (textSizeDescription + textSizeClicks) + (textSizeClicks // 4) + 4 + textSizeDescription - textSizeClicks // 1.4))
        screen.blit(cpsText, ((screen.get_width() - cpsText.get_width()) // 2, (textSizeDescription + textSizeClicks) + (textSizeClicks // 4) + 4 + textSizeDescription - textSizeClicks // 1.4 + textSizeCPC))
        # keysOnScreen = makeText(f"{len(fallenKeys)}/{round(minForUltra)} falling keys until ultraclick!", (255, 255, 255), cpcFontClass)
        # screen.blit(keysOnScreen, ((screen.get_width() - keysOnScreen.get_width()) // 2, (textSizeDescription + textSizeClicks) + (textSizeClicks // 4) + 4 + textSizeDescription - textSizeClicks // 1.4 + textSizeCPC + textSizeCPC))
        # if (len(fallenKeys)/maximumFallenKeys) >= 0.5:
        #     maxKeysOnScreen = makeText(f"{round((len(fallenKeys)/maximumFallenKeys)*100, 2)}% of your fallen key allowance!", (255, 255, 255), cpcFontClass)
        #     screen.blit(maxKeysOnScreen, ((screen.get_width() - maxKeysOnScreen.get_width()) // 2, (textSizeDescription + textSizeClicks) + (textSizeClicks // 4) + 4 + textSizeDescription - textSizeClicks // 1.4 + textSizeCPC + textSizeCPC + textSizeCPC))
        console.draw(screen)
        pygame.display.update()
        delta = clock.tick(60)
    except Exception as e:
        console.log("Error: " + str(e), Colours.ERR)

pygame.quit()