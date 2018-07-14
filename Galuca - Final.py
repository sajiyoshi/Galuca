import sys,pygame
from pygame.locals import *
pygame.init()

import random
import fractions
import math
import copy

class Galaga(object):
    baseScaleFactor = 1.8 #Changes the game Window Size 
    def __init__(self):
        self.baseScaleFactor = Galaga.baseScaleFactor #Adjusts default window size
        self.baseWidth = 224
        self.baseHeight = 288
        self.baseHeader = 30 #Pixels Tall
        self.baseFooter = 30 #Pixels Tall
        self.header = self.baseHeader * self.baseScaleFactor
        self.footer = self.baseHeader * self.baseScaleFactor
        self.baseScreenWidth = int(self.baseWidth * self.baseScaleFactor)
        self.baseScreenHeight = int((self.baseHeight + self.baseHeader +\
                            self.baseFooter)* self.baseScaleFactor)
        self.scaleFactor = 1 #Used to adjust window size in-game

        self.screenWidth = self.baseScreenWidth * self.scaleFactor
        self.screenHeight = self.baseScreenHeight * self.scaleFactor

        self.newScreenWidth = self.baseScreenWidth * self.scaleFactor
        self.newScreenHeight = self.baseScreenHeight * self.scaleFactor
        
        self.startScreen()

    def startScreen(self):
        self.initStart()
##        self.playIntroAnimation()
        while True:
            self.moveStartScreen()
            self.drawStartScreen()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN or event.type == KEYUP:
                    self.keyPressed(event)
                elif event.type == MOUSEMOTION or event.type == MOUSEBUTTONDOWN \
                     or event.type == MOUSEBUTTONUP:
                    self.mousePressed(event)
                elif event.type == VIDEORESIZE:
                    self.resizeWindow(event)
                if self.gameStart == True:
                    creditSound =\
                    pygame.mixer.Sound("galaga_sounds/game_sounds/creditSound.wav")
                    self.music.pause()
                    self.soundFX.queue(creditSound)
                    self.runGalaga()
                elif self.exitGame:
                    self.music.unpause()
                    self.exitGame = False
            pygame.time.delay(int(1000/self.fps))

    def mousePressed(self,event):
        if self.gameStart == False:
            mousePos = pygame.mouse.get_pos()
            if event.type == MOUSEMOTION:
                for button in Button.buttonList:
                    if button.touching(mousePos,self):
                        button.image = button.lgtImage
                    else:
                        button.image = button.regImage
                if self.customScreen:
                    if (self.recordPoints) and mousePos[1] <= \
                       ((self.baseScreenHeight*self.scaleFactor)*.83)\
                       and (not self.saving):
                        self.addPoints(mousePos)
                        
            if event.type == MOUSEBUTTONDOWN:
                (button1,button2,button3) = pygame.mouse.get_pressed()
                if button1:
                    if self.customScreen:
                        if self.backButton.touching(mousePos,self):
                            self.backClicked = True
                        elif self.customScreenRep.touching(mousePos,self):
                            self.recordPoints = True
                        elif self.deleteButton.touching(mousePos,self):
                            self.deletePoints()
                        elif self.saveButton.touching(mousePos,self) and\
                             len(self.tempPoints) >= 1:
                            self.convertPoints()
                        elif self.resetButton.touching(mousePos,self):
                            self.resetPaths()
                        else:
                            self.backClicked = False
                        if self.saving:
                            if self.butterflyButton.touching(mousePos,self):
                                self.saveToButterfly = not self.saveToButterfly
                            elif self.beeButton.touching(mousePos,self):
                                self.saveToBee = not self.saveToBee
                            elif self.galagaButton.touching(mousePos,self):
                                self.saveToGalaga = not self.saveToGalaga
                            elif self.cancelButton.touching(mousePos,self):
                                self.saving = False
                                self.saveToButterfly = False
                                self.saveToBee = False
                                self.saveToGalaga = False
                            elif self.finishButton.touching(mousePos,self):
                                self.savePoints()
                    elif self.howToPlay:
                        if self.backButton.touching(mousePos,self):
                            self.backClicked = True
                                    
                    else: #Only make these available on home screen
                        if self.startButton.touching(mousePos,self):
                            self.startClicked = True
                        else:
                            self.startClicked = False
                        if self.customButton.touching(mousePos,self):
                            self.customClicked = True
                        else:
                            self.customClicked = False
                        if self.howToPlayButton.touching(mousePos,self):
                            self.howToPlayClicked = True
                        else:
                            self.howToPlayClicked = False
                        
                    if self.muteMusic == False:
                        if self.muteButton.touching(mousePos,self):
                            self.muteMusic = True
                            pygame.mixer.pause()
                    else:
                        if self.muteButton.touching(mousePos,self):
                            self.muteMusic = False
                            pygame.mixer.unpause()
                            
            if event.type == MOUSEBUTTONUP:
                if self.customScreen:
                    if self.backButton.touching(mousePos,self):
                        if self.backClicked:
                            self.customScreen = False
                            self.backClicked = False
                        else:
                            self.backClicked = False
                    if self.recordPoints == True:
                        self.recordPoints = False
                elif self.howToPlay:
                    if self.backButton.touching(mousePos,self):
                        if self.backClicked:
                            self.howToPlay = False
                            self.backClicked = False
                        else:
                            self.backClicked = False
                else:
                    if self.startButton.touching(mousePos,self):
                        if self.startClicked:
                            self.gameStart = True
                            self.startClicked = False
                        else:
                            self.startClicked = False
                    if self.customButton.touching(mousePos,self):
                        if self.customClicked:
                            self.customScreen = True
                            self.customClicked = False
                        else:
                            self.customClicked = False
                    if self.howToPlayButton.touching(mousePos,self):
                        if self.howToPlayClicked == True:
                            self.howToPlay = True
                            self.howToPlayClicked = False
                        else:
                            self.howToPlayClicked = False
            
    def initStart(self):
        self.gameTitle = "Galuca"
        self.fps = 60.0
        self.initScreen()
        self.initButtons()

        self.gameStart = False
        self.quitScreen = False
        self.exitGame = False
        self.saving = False
        self.animationOn = False
        self.settingLevel = False
        self.musicOn = False

        #Empty image for testing / Various Purposes
        (self.empty,self.emptywidth,self.emptyHeight) = \
        importImage("galaga_sprites/empty.png",True)
        
        #Speed Objects
        self.PPS = 100 * self.baseScaleFactor #Pixels per second
        self.PPT = self.PPS / self.fps #Pixels per Tick

        #Star Objects / Animation Parameters
        self.starList = []
        baseStarSize = 1
        self.starSizes = [baseStarSize,baseStarSize*2,baseStarSize*3-1]
        baseStarSpeed = self.baseScreenHeight/200
        self.starSpeeds = [-baseStarSpeed,-int(baseStarSpeed*1.3),
                           -int(baseStarSpeed*1.6)]

        #Time Objects
        self.clock = pygame.time.Clock() #Initialize game clock
        self.milliseconds = 0

        #Sound Objects
        self.soundFX = pygame.mixer.Channel(0)
        self.deathSounds = pygame.mixer.Channel(1)
        self.missileSounds = pygame.mixer.Channel(2)
        self.music = pygame.mixer.Channel(3)
        self.ambience = pygame.mixer.Channel(4)
        self.levelSound =\
        pygame.mixer.Sound("galaga_sounds/game_sounds/stageFlag_appearence.wav")

        startScreenMusic =\
        pygame.mixer.Sound("galaga_sounds/music/start_screen.ogg")
        self.music.play(startScreenMusic,-1)

        #Font Objects
        textSize = int(self.header/1.8)
        self.gameFont = pygame.font.SysFont("Joystix",textSize)

        #Custom Screen
        self.customPoints = []
        self.tempPoints = []
        self.recordPoints = False

    def initButtons(self):
       #Logo
        logoScale = .6
        logoFile = "galaga_sprites/galaga-logo.png"
        (self.logo,self.logoHeight,self.logoWidth) = \
        importImage(logoFile,True,logoScale)
        self.logoX = self.baseScreenWidth/2 - self.logoWidth/2
        self.logoY = 50

        self.initStartButtons()
        self.initCustomScreenButtons()
        self.initHowToPlayButtons()
        self.initInGameButtons()


    def initStartButtons(self):
        #Start Button
        self.startClicked = False
        startButtonLocation = (self.baseScreenWidth/2,self.baseScreenHeight*.5)
        startButtonScale = 2
        startButtonFile = "galaga_sprites/text/start.png"
        startLightFile = "galaga_sprites/text/startLight.png"
        self.startButton = Button(startButtonLocation,startButtonScale,
                                 startButtonFile,startLightFile)

        sKeyLogo = "galaga_sprites/text/s.png"
        sKeyLocation = (startButtonLocation[0]+self.startButton.width/2+20,
                        startButtonLocation[1])
        self.sKeyLogo = Button(sKeyLocation, startButtonScale*1.5, sKeyLogo)

        #Custom Button
        self.customClicked = False
        self.customScreen = False
        customButtonLocation = (self.baseScreenWidth/2,self.baseScreenHeight*.6)
        customButtonScale = 2
        customButtonFile = "galaga_sprites/text/custom.png"
        customLgtFile = "galaga_sprites/text/customLight.png"
        self.customButton = Button(customButtonLocation,customButtonScale,
                                   customButtonFile,customLgtFile)

        #How To Play
        self.howToPlay = False
        self.howToPlayClicked = False
        howToPlayLocation = (self.baseScreenWidth/2,self.baseScreenHeight*.7)
        howToPlayScale = 2
        howToPlayFile = "galaga_sprites/buttons/howToPlay.png"
        howToPlayLgt = "galaga_sprites/buttons/howToPlayLgt.png"
        self.howToPlayButton = Button(howToPlayLocation,howToPlayScale,
                                      howToPlayFile,howToPlayLgt)

        #Mute Button
        self.muteMusic = False
        muteButtonLocation = (self.baseScreenWidth/10,
                              int(self.baseScreenHeight*.9))
        muteScale = 3
        muteButtonFile = "galaga_sprites/buttons/soundOff.png"
        muteButtonLgtFile = "galaga_sprites/buttons/soundOffLgt.png"
        self.muteButton = Button(muteButtonLocation,muteScale,
                                 muteButtonFile,muteButtonLgtFile)

        musicOnFile = "galaga_sprites/buttons/soundOn.png"
        musicOnLgtFile = "galaga_sprites/buttons/soundOnLgt.png"
        self.musicOnButton = Button(muteButtonLocation,muteScale,
                                    musicOnFile,musicOnLgtFile)

        #Back Button
        self.backClicked = False
        backButtonLocation = (int(self.baseScreenWidth*.9),
                              int(self.baseScreenHeight*.9))
        backScale = 3
        backButtonFile = "galaga_sprites/buttons/back.png"
        backButtonLgt = "galaga_sprites/buttons/backLgt.png"
        self.backButton = Button(backButtonLocation,backScale,
                                 backButtonFile,backButtonLgt)

    def initCustomScreenButtons(self):
        #Reset All Button
        resetLoc = (self.baseScreenWidth/2,self.baseScreenHeight*.95)
        resetScale = 2
        resetButtonFile = "galaga_sprites/buttons/resetAll.png"
        resetButtonLgt = "galaga_sprites/buttons/resetAllLgt.png"
        self.resetButton = Button(resetLoc,resetScale,resetButtonFile,
                                  resetButtonLgt)

        #Which Enemy Button
        whichEnLoc = (self.baseScreenWidth/2,self.baseScreenHeight * .25)
        whichEnScale = 4
        whichEnFile = "galaga_sprites/buttons/whichEnemies.png"
        self.whichEnemyButton = Button(whichEnLoc,whichEnScale,whichEnFile)

        #Click and Drag
        clickDragLoc = (self.baseScreenWidth/2,self.baseScreenHeight*.03)
        clickDragScale = 3
        clickDragFile = "galaga_sprites/buttons/clickAndDrag.png"
        self.clickDragButton = Button(clickDragLoc,clickDragScale,clickDragFile)

        #Finish Button
        finishLoc = (self.baseScreenWidth * .7,self.baseScreenHeight * .5)
        finishScale = 3
        finishFile = "galaga_sprites/buttons/finish.png"
        finishLgt = "galaga_sprites/buttons/finishLgt.png"

        self.finishButton = Button(finishLoc,finishScale,finishFile,finishLgt)

        #Cancel Button
        cancelLoc = (self.baseScreenWidth * .3,self.baseScreenHeight * .5)
        cancelScale = 3
        cancelFile = "galaga_sprites/buttons/cancel.png"
        cancelLgt = "galaga_sprites/buttons/cancelLgt.png"

        self.cancelButton = Button(cancelLoc,cancelScale,cancelFile,cancelLgt)

        #Enemy Select
        enemyButtonScale = 4

        #ButterFly
        butterflyLoc = (self.baseScreenWidth * .3,self.baseScreenHeight*.4)
        butterflyFile = "galaga_sprites/buttons/butterfly.png"

        butterflyLgt = "galaga_sprites/buttons/butterflyLgt.png"

        self.butterflyButton = Button(butterflyLoc,enemyButtonScale,
                                butterflyFile,butterflyLgt)
        self.butterflyButtonLgt = Button(butterflyLoc,enemyButtonScale,
                                butterflyLgt)

        #Bee
        beeLoc = (self.baseScreenWidth * .7,self.baseScreenHeight*.4)
        beeFile = "galaga_sprites/buttons/bee.png"

        beeLgt = "galaga_sprites/buttons/beeLgt.png"

        self.beeButton = Button(beeLoc,enemyButtonScale,beeFile,beeLgt)
        self.beeButtonLgt = Button(beeLoc,enemyButtonScale,beeLgt)

        #Galaga
        galagaLoc = (self.baseScreenWidth*.5,self.baseScreenHeight*.4)
        galagaFile = "galaga_sprites/buttons/galaga.png"

        galagaLgt = "galaga_sprites/buttons/galagaLgt.png"

        self.galagaButton = Button(galagaLoc,enemyButtonScale,galagaFile,
                                   galagaLgt)
        self.galagaButtonLgt = Button(galagaLoc,enemyButtonScale,galagaLgt)

        #Custom Screen
        customScreenLoc = (self.baseScreenWidth/2,self.baseScreenHeight/20)
        customScreenScale = Galaga.baseScaleFactor * .9
        customScreenFile = "galaga_sprites/custom/screenRep2.png"

        self.customScreenRep = Button(customScreenLoc,customScreenScale,
                                   customScreenFile,None,"t")

        #Save Button
        saveLoc = (self.baseScreenWidth * .38,self.baseScreenHeight * .85)
        saveScale = 3
        saveFile = "galaga_sprites/buttons/save.png"
        saveLgt = "galaga_sprites/buttons/saveLgt.png"
        self.saveButton = Button(saveLoc,saveScale,saveFile,saveLgt)

        #Delete Button
        deleteLoc = (self.baseScreenWidth*.6,self.baseScreenHeight *.85)
        deleteScale = 3
        deleteFile = "galaga_sprites/buttons/delete.png"
        deleteLgt = "galaga_sprites/buttons/deleteLgt.png"
        self.deleteButton = Button(deleteLoc,deleteScale,deleteFile,deleteLgt)

    def initHowToPlayButtons(self):
        #Plain Enemies
        
        #PlainButterfly
        butterflyLoc = (self.baseScreenWidth*.2,self.baseScreenHeight*.65)
        butterflyScale = 3
        butterflyFile = "galaga_sprites/buttons/plainButterfly.png"
        self.plainButterfly = Button(butterflyLoc,butterflyScale,butterflyFile)

        #PlainBee
        beeLoc = (self.baseScreenWidth * .4,self.baseScreenHeight*.65)
        beeScale = 3
        beeFile = "galaga_sprites/buttons/plainBee.png"
        self.plainBee = Button(beeLoc,beeScale,beeFile)

        #PlainGalaga
        galagaLoc = (self.baseScreenWidth * .3, self.baseScreenHeight*.65)
        galagaScale = 3
        galagaFile = "galaga_sprites/buttons/plainGalaga.png"
        self.plainGalaga = Button(galagaLoc,galagaScale,galagaFile)

        #Missile
        missileLoc = (self.baseScreenWidth * .1,self.baseScreenHeight*.65)
        missileScale = Galaga.baseScaleFactor
        missileFile = "galaga_sprites/missiles/enemy_missile.png"
        self.missileButton = Button(missileLoc,missileScale,missileFile)

        #Left arrow
        scale = 1.5
        leftArrowLoc = (self.baseScreenWidth * .2,self.baseScreenHeight*.4)
        leftArrowFile = "galaga_sprites/buttons/left.png"
        self.leftArrow = Button(leftArrowLoc,scale,leftArrowFile)

        spaceLoc = (self.baseScreenWidth * .25,self.baseScreenHeight * .5)
        spaceFile = "galaga_sprites/buttons/space.png"
        self.spaceBar = Button(spaceLoc,scale,spaceFile)

        rightArrowLoc = (self.baseScreenWidth * .3,self.baseScreenHeight * .4)
        rightArrowFile = "galaga_sprites/buttons/right.png"
        self.rightArrow = Button(rightArrowLoc,scale,rightArrowFile)

        #Move And Shoot
        moveShootScale = 4
        moveShootLoc = (self.baseScreenWidth*.75,self.baseScreenHeight *.45)
        moveShootFile = "galaga_sprites/buttons/moveAndShoot.png"
        self.moveShootButton = Button(moveShootLoc,moveShootScale,moveShootFile)

        #Avoid These
        avoidScale = 4
        avoidLoc = (self.baseScreenWidth * .75, self.baseScreenHeight*.65)
        avoidFile = "galaga_sprites/buttons/avoidThese.png"
        self.avoidThese = Button(avoidLoc,avoidScale,avoidFile)

        #Have Fun
        haveFunScale = 4
        haveFunLoc = (self.baseScreenWidth *.5,self.baseScreenHeight*.75)
        haveFunFile = "galaga_sprites/buttons/haveFun.png"
        self.haveFunButton = Button(haveFunLoc,haveFunScale,haveFunFile)
        
    def initInGameButtons(self):
        #Get Ready
        getReadyLocation = (self.baseScreenWidth/2,self.baseScreenHeight*.6)
        getReadyScale = 3
        getReadyFile = "galaga_sprites/buttons/getReady.png"
        self.getReadyButton =Button(getReadyLocation,getReadyScale,getReadyFile)
        
    def addPoints(self,mousePos):
        pixelDistance = 4 * self.scaleFactor
        maxPoints = 350

        if len(self.tempPoints) == 0:
            self.tempPoints.append((mousePos[0]/self.scaleFactor,
                                    mousePos[1]/self.scaleFactor))
        elif Movement.distance(self.tempPoints[len(self.tempPoints)-1],
                mousePos) >= pixelDistance*self.scaleFactor:
            if len(self.tempPoints) <= maxPoints:
                self.tempPoints.append((mousePos[0]/self.scaleFactor,
                                    mousePos[1]/self.scaleFactor))
            else:
                self.tempPoints.pop(0)
                self.tempPoints.append((mousePos[0]/self.scaleFactor,
                                    mousePos[1]/self.scaleFactor))

    def deletePoints(self):
        self.tempPoints = []
        self.customPoints = []

    def convertPoints(self):
        self.saving = True
        self.saveToBee = False
        self.saveToButterfly = False
        self.saveToGalaga = False
        for point in self.tempPoints:
            #.9 == scale of the custom screen
            #.05 is the indent of the custom screen
            x = int(round(((point[0] - self.baseScreenWidth*.05)/.9)))
            y = int(round(((point[1] - self.baseScreenHeight*.05)/.9))+self.header)
            self.customPoints.append((x,y))

    def savePoints(self):
        if self.saveToButterfly:
            pathsFile = open("paths/butterflyPaths.txt","a")
            pathsFile.write("\n")
            pathsFile.write(str(self.customPoints))
        if self.saveToBee:
            pathsFile = open("paths/beePaths.txt","a")
            pathsFile.write("\n")
            pathsFile.write(str(self.customPoints))
        if self.saveToGalaga:
            pathsFile = open("paths/galagaBossPaths.txt","a")
            pathsFile.write("\n")
            pathsFile.write(str(self.customPoints))
        self.saving = False
        self.saveToButterfly = False
        self.saveToBee = False
        self.saveToGalaga = False
        self.tempPoints = []
        self.customPoints = []

    def resetPaths(self):
        #Default Paths == 1 and 2
        #Butterfly defaults : 1
        butterflyFile = open("paths/butterflyPaths.txt","w")
        butterflyFile.write("1")
        butterflyFile.close()

        #Bee defaults : 1 and 2
        beeFile = open("paths/beePaths.txt","a")
        beeFile.truncate()
        beeFile.write("1")
        beeFile.write("\n")
        beeFile.write("2")
        beeFile.close()

        #Galaga defaults: 1 and 2
        galagaFile = open("paths/galagaBossPaths.txt","a")
        galagaFile.truncate()
        galagaFile.write("1")
        galagaFile.write("\n")
        galagaFile.write("2")
        galagaFile.close()

    def moveStartScreen(self):
        self.moveStars()
        
    def drawStartScreen(self):
        pygame.draw.rect(self.screen,(0,0,0),
        ((0,0),(self.baseScreenWidth * self.scaleFactor,
                self.baseScreenHeight*self.scaleFactor))) #Draw Black Background
        self.drawStars()
        if self.customScreen:
            self.drawCustomScreen()
        elif self.howToPlay:
            self.drawLogo()
            self.drawHowToPlay()
        else:
            self.drawStartButtons()
            self.drawLogo()
        pygame.display.update()

    def drawCustomScreen(self):
        pygame.draw.rect(self.screen,(0,0,0),
        ((0,0),(self.baseScreenWidth * self.scaleFactor,
                self.baseScreenHeight*self.scaleFactor)))
        self.drawStars()
        self.drawPoints()
        self.drawCustomButtons()
        pygame.display.update()

    def drawPoints(self):
        size = 1
        for point in self.tempPoints:
            pygame.draw.circle(self.screen,(0,224,255),
                               (int(point[0]*self.scaleFactor),
                                int(point[1]*self.scaleFactor)),
                               size)
        
    def drawCustomButtons(self):
        if self.customScreen:
            self.backButton.draw(self)
            self.customScreenRep.draw(self)
            self.deleteButton.draw(self)
            self.saveButton.draw(self)
            self.resetButton.draw(self)
            self.clickDragButton.draw(self)
            if self.saving:
                if self.saveToBee:
                    self.beeButtonLgt.draw(self)
                if not self.saveToBee:
                    self.beeButton.draw(self)
                    
                if self.saveToButterfly:
                    self.butterflyButtonLgt.draw(self)
                if not self.saveToButterfly:
                    self.butterflyButton.draw(self)
                    
                if self.saveToGalaga:
                    self.galagaButtonLgt.draw(self)
                if not self.saveToGalaga:
                    self.galagaButton.draw(self)
                self.whichEnemyButton.draw(self)
                self.cancelButton.draw(self)
                self.finishButton.draw(self)
        if self.muteMusic == False:
            self.musicOnButton.draw(self)
        else:
            self.muteButton.draw(self)

    def drawStartButtons(self):
        self.startButton.draw(self)
        self.sKeyLogo.draw(self)
        self.howToPlayButton.draw(self)
        self.customButton.draw(self)
        if self.muteMusic == False:
            self.musicOnButton.draw(self)
        else:
            self.muteButton.draw(self)

    def drawHowToPlay(self):
        self.drawHowToPlayButtons()
        self.howtoquitMsg()

    def drawHowToPlayButtons(self):
        self.backButton.draw(self)
        
        #Avoid These
        self.avoidThese.draw(self)
        self.plainBee.draw(self)
        self.plainButterfly.draw(self)
        self.plainGalaga.draw(self)
        self.missileButton.draw(self)

        #Use These
        self.leftArrow.draw(self)
        self.rightArrow.draw(self)
        self.spaceBar.draw(self)
        self.moveShootButton.draw(self)

        #haveFun
        self.haveFunButton.draw(self)
        
        if self.muteMusic == False:
            self.musicOnButton.draw(self)
        else:
            self.muteButton.draw(self)
        

    def drawLogo(self):
        self.screen.blit(\
            pygame.transform.scale(self.logo,
            (int(self.logoWidth  * self.scaleFactor),
             int(self.logoHeight * self.scaleFactor))),
            (int(round((self.logoX * self.scaleFactor))),
             int(round((self.logoY * self.scaleFactor)))))
            
    def runGalaga(self):
        self.initGame()
        introMusic =\
        pygame.mixer.Sound("galaga_sounds/game_sounds/startMusic.wav")
        self.ambience.play(introMusic,0)
        self.animationOn = True
        while True:
            if self.animationOn:
                self.gameStartAnimation()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN or event.type == KEYUP:
                    self.keyPressed(event)
                elif event.type == VIDEORESIZE:
                    self.resizeWindow(event)
            self.keepTime()
            if not (self.gameOver):
                self.moveGalaga()
                self.drawGalaga()
            else:
                self.moveGalaga()
                self.drawGalaga()
                self.gameOverMsg()
            pygame.time.delay(int(1000/self.fps)) #1000 milliseconds/fps
            if self.exitGame:
                break

    def gameStartAnimation(self):
        self.settingLevel = True
        if self.ambience.get_busy() == False:
            self.animationOn = False
            self.settingLevel = False
            ambience =\
            pygame.mixer.Sound("galaga_sounds/game_sounds/ambience.ogg")
            self.ambience.play(ambience,-1)

    def settingLevelAnimation(self):
        self.moveGalaga()
        self.drawGalaga()
        pygame.time.delay(int(1000/self.fps)) #1000 milliseconds/fps
        
    def resizeWindow(self,event):
        (newWidth,newHeight) = event.size

        widthScaleFactor = ((newWidth * 1.0) / self.baseScreenWidth)

        heightScaleFactor = ((newHeight * 1.0) / self.baseScreenHeight)

        self.scaleFactor = min(widthScaleFactor,heightScaleFactor)
        if self.scaleFactor < 1:
            self.scaleFactor = 1

        self.initScreen()

        self.newScreenWidth = self.baseScreenWidth * self.scaleFactor
        self.newScreenHeight = self.baseScreenHeight * self.scaleFactor
        
    def initScreen(self):
        self.screenSize = (int(self.baseScreenWidth * self.scaleFactor),
                           int(self.baseScreenHeight * self.scaleFactor))

        self.screen =\
        pygame.display.set_mode(self.screenSize,RESIZABLE)

        pygame.display.set_caption(self.gameTitle) #Window Caption (title)

        (iconImage,iconWidth,iconHeight) =\
        importImage('galaga_sprites/fighter/fighter.png',True) #True == alpha

        pygame.display.set_icon(iconImage)
        pygame.display.flip()

    def keepTime(self):
        self.milliseconds += self.clock.tick()
        self.seconds = self.milliseconds/1000.0
        
    def initGame(self):
        self.initPaths()
        self.initObjects()
        self.initEnemies()
        self.initFighter()
             
    def keyPressed(self,event):
        if self.gameStart == False:
            if event.type == KEYDOWN:
                if event.key == K_s:
                    self.gameStart = True
                if event.key == K_c:
                    if self.customScreen == False:
                        self.customScreen = True
                    else:
                        self.customScreen = False
        else:
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.fighter.vx = -self.fighter.speed
                elif event.key == K_RIGHT:
                    self.fighter.vx = self.fighter.speed
                elif event.key == K_SPACE:
                    if len(self.missileList) < Missile.maxMissiles and\
                       self.animationOn == False and not(self.gameOver) and\
                       not self.fighterIsDown:
                        self.shotsFired += 1
                        self.missileList.append(self.fighter.fireMissile(self.\
                                                            fighterMissileSpeed))
                elif event.key == K_q:
                    self.quit()
                    self.quitScreen = True
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    if self.fighter.vx < 0:
                        self.fighter.vx = 0
                elif event.key == K_RIGHT:
                    if self.fighter.vx >0:
                        self.fighter.vx = 0
    def quit(self):
        self.resetGame()
        self.ambience.stop()
        self.gameStart = False
        self.exitGame = True

    def initPaths(self):
        butterflyPathsPre = open("paths/butterflyPaths.txt","r")
        butterflyPathsStr = butterflyPathsPre.read()
        butterflyPathsList = butterflyPathsStr.split("\n")
        butterflyPathsPre.close()
        self.butterflyPaths = []
        for item in butterflyPathsList:
            self.butterflyPaths.append(eval(item))
        
            
        beePathsPre = open("paths/beePaths.txt","r")
        beePathsStr = beePathsPre.read()
        beePathsList = beePathsStr.split("\n")
        beePathsPre.close()
        self.beePaths = []
        for item in beePathsList:
            self.beePaths.append(eval(item))
        
        galagaPathsPre = open("paths/galagaBossPaths.txt","r")
        galagaPathsStr = galagaPathsPre.read()
        galagaPathsList = galagaPathsStr.split("\n")
        galagaPathsPre.close()
        self.galagaPaths = []
        for item in galagaPathsList:
            self.galagaPaths.append(eval(item))
        
        
    def initEnemies(self):
        totalEnemies = self.formation.totalEnemies
        bossGalaga = self.formation.bossGalaga
        butterflies = self.formation.butterflies
        bees = self.formation.bees
        for enemy in xrange(self.formation.totalEnemies):
            position = self.formation.positionList[enemy]
            if enemy < bossGalaga:
                self.enemyList.append(EnemyGalaga(position[0],position[1],self))
            elif enemy < bossGalaga + butterflies:
                self.enemyList.append(EnemyButterfly(position[0],position[1],self))
            else:
                self.enemyList.append(EnemyBee(position[0],position[1],self))        
        for enemy in self.enemyList:
            (enemy.floatVX,enemy.floatVY) = Movement.calculateFloat(enemy,self)
                
    def initFighter(self):
        self.fighterMissileSpeed = -int(self.baseScreenHeight/self.fps*1.5)
        self.fighter = Fighter(self)
        
    def initObjects(self):
        #Game Start Objects
        self.gameOver = False

        self.hiScore = self.findHiScore()
        
        self.fighterIsDown = False

        #Missile Objects
        self.missileList = []
        self.enemyMissiles = []

        #Enemy Objects
        self.enemyList = []

        #Formation Objects
        self.formation = Formations(1,self) #Basic Formation

        #Explosion animation Objects
        self.explosionList = []

        #Score Objects
        self.score = 0

        #Shot Objects
        self.shotsFired = 0
        self.shotsHit = 0

        #Gameplay objects
        self.score = 0
        self.lives = 3

        #Level Objects
        self.level = 1
        self.levelChecker = 0
        self.maxLevelSeconds = 3
        
        #Text Markers
        #HighScore
        highScoreLocation = (self.baseScreenWidth/2,0)
        highScoreScale = 3
        highScoreFile = "galaga_sprites/text/high_score.png"
        justify = "t"
        self.highScoreImage = Button(highScoreLocation,highScoreScale,
                                     highScoreFile,None,justify)
        #1up
        oneUpLocation = (self.baseScreenWidth/5,0)
        oneUpScale = 3
        oneUpFile = "galaga_sprites/text/1up.png"
        justify = "t"
        self.oneUpImage = Button(oneUpLocation,oneUpScale,
                                 oneUpFile,None,justify)
        
    def drawGalaga(self):
        self.drawScreen()
        self.drawGameButtons()
        pygame.display.update()

    def drawScreen(self):
        self.screen.fill((0,0,0))# Black Backdrop
        self.drawStars()
        self.drawFighter()
        self.drawFooter()
        self.drawEnemies()
        self.drawMissiles()
        self.drawExplosions()
        self.drawHeader()

    def drawGameButtons(self):
        if self.settingLevel and not self.gameOver:
            self.getReadyButton.draw(self)

    def drawHeader(self):
        pygame.draw.rect(self.screen,(0,0,0),((0,0),
        (int(self.baseScreenWidth*self.scaleFactor),
         int(self.header*self.scaleFactor))))

        self.oneUpImage.draw(self)
        self.highScoreImage.draw(self)

        self.drawScore()

    def drawFooter(self):
        pygame.draw.rect(self.screen,(0,0,0),((0,(self.baseScreenHeight -\
        self.footer)*self.scaleFactor),
        (int(self.baseScreenWidth*self.scaleFactor),
         int(self.footer*self.scaleFactor))))

        level = "Level %s" % self.level
        levelText = self.gameFont.render(level, 1, (0,224,255),(0,0,0))
        levelTextRect = levelText.get_rect()
        levelTextRect.right = int(((self.baseScreenWidth * self.baseScaleFactor)*.49)*\
        self.scaleFactor)
        levelTextRect.top = int(self.baseScreenHeight * self.scaleFactor - self.footer)
        self.screen.blit(levelText, levelTextRect)
        
        self.drawLives()
        

    def drawLives(self):
        xPosition = self.fighter.width * 2
        yPosition = self.baseScreenHeight * self.scaleFactor - self.footer

        for life in xrange(self.lives-1):
            self.screen.blit(self.fighter.fighterImage,(xPosition,yPosition))
            xPosition -= self.fighter.width + self.fighter.width/2

    def drawScore(self):
        score = str(self.score)
        score = self.gameFont.render(score,1,(255,255,255),(0,0,0))
        scoreRect = score.get_rect()
        scoreRect.right = int(self.baseScreenWidth*self.baseScaleFactor*self.scaleFactor*0.125)
        scoreRect.top = 20
        self.screen.blit(score, scoreRect)

        if self.score > self.hiScore:
            self.hiScore = self.score
        hiScore = str(self.hiScore)
        hiScore = self.gameFont.render(hiScore,1,(255,255,255),(0,0,0))
        hiScoreRect = hiScore.get_rect()
        hiScoreRect.centerx = int(self.baseScreenWidth*self.baseScaleFactor*self.scaleFactor*0.25)
        hiScoreRect.top = 20
        self.screen.blit(hiScore, hiScoreRect)
              
    def drawEnemies(self):
        for enemy in self.enemyList:
            enemy.draw(self)

    def drawMissiles(self):
        for missile in self.missileList:
            missile.draw(self)
        for missile in self.enemyMissiles:
            missile.draw(self)

    def drawStars(self):
        starLife = self.fps/2
        starWait = self.fps/10
        for star in self.starList:
            if star.flash == starLife: #Reset Star Flash
                star.flash = 0
            elif star.flash > starWait: #Only draw if flash is on.  
                star.draw(self) #Draw method
                star.flash += 1
            else:
                star.flash += 1
            
    def drawFighter(self):
        self.fighter.draw(self)

    def drawExplosions(self):
        for explosion in self.explosionList:
            explosion.draw(self)

    def moveGalaga(self):
        self.moveFighter()
        self.moveStars()
        self.moveMissiles()
        self.updateEnemies()
        self.moveEnemies()
        self.updateExplosions()
        if not self.gameOver:
            self.checkForCollisions()

    def moveEnemies(self):
        for enemy in self.enemyList:
            enemy.move()

    def updateEnemies(self):
        if (len(self.enemyList) == 0):
            self.advanceLevel()
        Enemy.flutterCheck(self)
        Enemy.floatCheck(self)
        Enemy.attackingEnemies = 0
        for enemy in self.enemyList:
            if enemy.isAttacking:
                Enemy.attackingEnemies += 1
            enemy.update(self)
        if Enemy.attackingEnemies < Enemy.maxAttackingEnemies and\
           not(self.settingLevel) and not(self.gameOver):
            enemy = random.choice(self.enemyList)
            if enemy.isAttacking == False:
                attackNumber = random.choice(enemy.attacks)
                attackingEnemies = enemy.chooseNearby(self)
                for enemy in attackingEnemies:
                    enemy.attack(self,attackNumber)
                sound = pygame.mixer.Sound('galaga_sounds/enemy/flying.wav')
                self.soundFX.stop()
                self.soundFX.play(sound,0)
        self.enemyList = [enemy for enemy in self.enemyList \
                            if (enemy.isAlive)]

    def moveFighter(self):
        """Checks to ensure fighter is within the bounds of the board, and then
            moves the fighter in the proper direction."""
        if self.fighterIsDown:
            self.fighterDown()
        else:
            if self.fighter.vx < 0: #Moving Left
                if self.fighter.x >= 0:
                    self.fighter.x += self.fighter.vx
            elif self.fighter.vx > 0: #Moving Right
                if self.fighter.x <= self.baseScreenWidth \
                 - self.fighter.width: 
                    self.fighter.x += self.fighter.vx

    def moveStars(self):
        numberOfStars = self.baseScreenHeight/20
        startingStars = numberOfStars-1
        if len(self.starList) < startingStars:
               self.starList.append(Star.createStar(self,True))#Random star
        elif len(self.starList) < numberOfStars:
            self.starList.append(Star.createStar(self,False))#Non random star
        for star in self.starList:
            star.move()
        self.starList =[star for star in self.starList if star.isOnScreen(self)]

    def moveMissiles(self):
        for missile in self.missileList:
            missile.move()
        #Next Lines: Removes all missiles which have traveled off screen.
        self.missileList = [missile for missile in self.missileList \
                            if (missile.isOnScreen(self) and missile.isAlive)]
        for missile in self.enemyMissiles:
            missile.move()
        self.enemyMissiles = [missile for missile in self.enemyMissiles \
                            if (missile.isOnScreen(self) and missile.isAlive)]
        Enemy.missilesFired = len(self.enemyMissiles)
        
    def updateExplosions(self):
        for explosion in self.explosionList:
            explosion.update()
        self.explosionList = [explosion for explosion in self.explosionList \
                              if (explosion.isAlive)]

    def checkForCollisions(self):
        for enemy in self.enemyList:
            for missile in self.missileList:
                if (enemy.collisionWith(missile) and (missile.isAlive)):
                    self.shotsHit += 1
                    missile.isAlive = False
                    enemy.hitPoints -= 1  
                    if enemy.hitPoints == 0:
                        self.deathSounds.stop
                        self.deathSounds.queue(enemy.deathSound)
                        enemy.isAlive = False
                        self.score += enemy.points
                        self.explosionList.append(Explosion(enemy,self))
                    elif isinstance(enemy,EnemyGalaga):
                        self.deathSounds.stop
                        self.deathSounds.queue(enemy.weakSound)
                        enemy.openImage = enemy.weakOpenImage
                        enemy.closedImage = enemy.weakClosedImage        
            if (self.fighter.collisionWith(enemy) and (enemy.isAlive))\
               and not self.settingLevel:
                enemy.isAlive = False
                self.score += enemy.points
                self.fighterIsDown = True
        for missile in self.enemyMissiles:
            if (self.fighter.collisionWith(missile) and (missile.isAlive))\
               and not self.settingLevel:
                missile.isAlive = False
                self.fighterIsDown = True

    def fighterDown(self):
        if self.settingLevel == False:
            self.explosionList.append(Explosion(self.fighter,self))
            self.ticks = 0
            self.soundFX.stop()
            self.deathSounds.stop()
            self.deathSounds.play(self.fighter.deathSound,0)
            self.settingLevel = True
        if self.settingLevel:
            self.fighter.image = self.empty
        enemiesFlying = 0
        for enemy in self.enemyList:
            if enemy.isFlying:
                enemiesFlying += 1
        if self.ticks == int(self.fps):
                twoSeconds = True
        else:
            twoSeconds = False
            self.ticks += 1
        if self.lives == 1:
            self.gameOver = True
            self.settingLevel = False
            self.fighterIsDown = False
            self.writeToHiScores()
        else:
            if (not(enemiesFlying) and twoSeconds):
                self.lives -= 1
                self.initFighter()
                self.settingLevel = False
                self.fighterIsDown = False
                
       
    def advanceLevel(self):
        if self.musicOn == False:
            self.settingLevel = True
            self.soundFX.stop()
            self.soundFX.play(self.levelSound,0)
            self.musicOn = True
        if self.soundFX.get_busy() == False:
            self.musicOn = False
            self.initEnemies()
            self.settingLevel = False
            self.level += 1
            if Enemy.speedValue < 1.2:
                Enemy.speedValue += .05
            if Enemy.maxAttackingEnemies < 6:
                if self.level % 2 == 0:
                    Enemy.maxAttackingEnemies += 1

    def gameOverMsg(self):
        endText = self.gameFont.render("Game Over! press q for quit",True,(255,0,0),(0,0,0))
        endTextRect = endText.get_rect()
        endTextRect.centerx = self.baseScreenWidth*self.scaleFactor/2
        endTextRect.top = self.baseScreenHeight * self.scaleFactor/2 + self.header * \
        self.scaleFactor/2
        self.screen.blit(endText,endTextRect)

        pygame.display.update()

    def howtoquitMsg(self):
        howtoquitText = self.gameFont.render("press q for quit",True,(255,255,255),(0,0,0))
        howtoquitTextRect = howtoquitText.get_rect()
        howtoquitTextRect.centerx = self.baseScreenWidth*self.scaleFactor/2
        howtoquitTextRect.top = self.baseScreenHeight * self.scaleFactor/2 + self.header * \
        self.scaleFactor/2
        self.screen.blit(howtoquitText,howtoquitTextRect)

        pygame.display.update()


    def resetGame(self):
        self.score = 0
        self.shotsFired = 0
        self.shotsHit = 0
        self.level = 0
        Enemy.resetClass()

    def writeToHiScores(self):
        hiScores = open("HiScores.txt","a")
        hiScores.write("\n")
        hiScores.write(str(self.score))
        hiScores.close()

    @classmethod
    def findHiScore(self):
        hiScores = open("HiScores.txt","r")
        hiScoreStr = hiScores.read()
        hiScoreList = hiScoreStr.split("\n")
        hiScores.close()
        hiScores = []
        if not hiScoreStr:
            hiScores.append(eval("2000"))
        for item in hiScoreList:
            if item:
                hiScores.append(eval(item))
        return max(hiScores)

 
###################
#Utility Functions#
###################
                    
def importImage(filePath,alpha,scaleFactor=Galaga.baseScaleFactor):
        """Imports an image and rescales it by the proper offset."""
        image = pygame.image.load(filePath)
        
        if alpha == True:
            image = image.convert_alpha()
        else:
            image = image.convert()

        imageHeight = int(image.get_height() * scaleFactor)
        imageWidth = int(image.get_width() * scaleFactor)
        
        return (pygame.transform.scale(image,(imageWidth,imageHeight)),
                                             imageHeight,imageWidth)

def almostEqual(val1,val2,delta):
    if abs(val1-val2) <= delta:
        return True
    else:
        return False

################################
#       Physics Objects        #
#Anything that moves on screen!#
################################

class PhysObj(object):
    def __init__(self,x,y,vx,vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.isAlive = True

    def move(self):
        """Repositions a physics object by it's x and y velocity."""
        self.x += self.vx
        self.y += self.vy

    def isOnScreen(self,galaga):
        """Returns True if object is on screen and False otherwise."""
        if self.x < 0 or self.x >galaga.baseScreenWidth * galaga.scaleFactor or\
           self.y < 0 or self.y >galaga.baseScreenHeight * galaga.scaleFactor:
            return False
        else:
            return True

    def draw(self,galaga):
        """Evaluates size and position based on scaleFactor"""

        galaga.screen.blit(\
            pygame.transform.scale(self.image,
                (int(self.width * galaga.scaleFactor),
                int(self.height * galaga.scaleFactor))),
            (int(round((self.x * galaga.scaleFactor))),
            int(round((self.y *galaga.scaleFactor)))))

    def importSprite(self,imageFilePath,alpha):
        (self.image,self.height,self.width) = \
              importImage(imageFilePath,True) #True == Alpha

    #Rotation function taken from: http://www.pygame.org/wiki/RotateCenter
    def rotateSprite(self,angle):
        """rotate an image while keeping its center and size"""
        orig_rect = self.image.get_rect()
        rot_image = pygame.transform.rotate(self.image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.image = rot_image #My Modification 
        
    def collisionWith(self,other,point = False):
        if point == False: #Colliding with an object
            hitBoxX0 = self.x-other.width
            hitBoxY0 = self.y
            hitBoxX1 = self.x+self.width+other.width
            hitBoxY1 = self.y+self.height
            if (other.x >= hitBoxX0 and other.x <= hitBoxX1) and \
               (other.y >= hitBoxY0 and other.y <= hitBoxY1):
                return True
            else:
                return False
        else: #Colliding with a point.
            #Uses Radial hit detection
            pointX = other[0]
            pointY = other[1]
            
            offset = self.width/8 ##Tested Variable
            
            centerX = self.x + self.width/2 
            centerY = self.y + self.height/2
            
            distance = ((centerX - pointX)**2 + (centerY -pointY)**2)**.5
            radius = offset
            if distance <= radius:
                return True
            else:
                return False
            

    @classmethod
    def getExplosions(self,classPath):
        imageList = []
        index = 1
        pathFound = True
        while pathFound:
            pathName = "galaga_sprites/explosions/%s_%d.png" % (classPath,index)
            try:
               imageList.append(importImage(pathName,True,Galaga.baseScaleFactor+1))
               index += 1
            except:
               pathFound = False
               return imageList
            
    def centerCall(self):
        xChange = self.width/2
        yChange = self.height/2

        return (self.x + xChange,self.y + yChange)
        
###########                
#Missiles!#
###########
            
class Missile(PhysObj):
    maxMissiles = 2 #Classic Galaga only allowed 4 missiles on screen. 
    def __init__(self,x,y,vx,vy,shooter):
        self.shooter = shooter
        self.importSprite()
        super(Missile,self).__init__(x-self.width/2,y-self.height,vx,vy)

    def importSprite(self):
        if self.shooter == "fighter":
            imageFilePath = "galaga_sprites/missiles/fighter_missile.png"
        elif self.shooter == "enemy":
            imageFilePath = "galaga_sprites/missiles/enemy_missile.png"
        super(Missile,self).importSprite(imageFilePath,True)

#########
#Fighter#
#########
        
class Fighter(PhysObj):
    def __init__(self,galaga):
        self.importSprite()
        self.setInitialLocation(galaga)
        self.speed = int(galaga.screenWidth/(galaga.fps)/3)
        self.deathSound = \
        pygame.mixer.Sound('galaga_sounds/fighter/death.wav')
        explosionPath = "fighter/explosion"
        self.expImages = PhysObj.getExplosions(explosionPath)
        self.fighterImage = self.image
        super(Fighter,self).__init__(self.x,self.y,self.vx,self.vy)

    def importSprite(self):
        imageFilePath = "galaga_sprites/fighter/fighter.png"
        super(Fighter,self).importSprite(imageFilePath,True)
        
    def setInitialLocation(self,galaga):
        self.x = galaga.screenWidth/2 - self.width/2
        self.y = galaga.screenHeight - self.height - galaga.footer
        #Next Lines: Inital Speed of fighter is 0. 
        self.vx = 0
        self.vy = 0

    def fireMissile(self,missileSpeed):
        #Set base parameters
        vx = 0
        vy = missileSpeed 
        shooter = "fighter"

        #Play missile Sound
        sound = pygame.mixer.Sound('galaga_sounds/fighter/fighter_shot1.wav')
        sound.play()

        #Return Missile Instance
        return Missile(self.x+self.width/2,self.y,vx,vy,shooter)

    def collisionWith(self,other):
        smallWidth = int(other.width * .9)
        hitBoxX0 = self.x-smallWidth
        hitBoxY0 = self.y
        hitBoxX1 = self.x+self.width
        hitBoxY1 = self.y+self.height
        if (other.x >= hitBoxX0 and other.x <= hitBoxX1) and \
           (other.y >= hitBoxY0 and other.y <= hitBoxY1):
            return True
        else:
            return False


########
#Stars!#
########
    
class Star(PhysObj):
    def __init__(self,x,y,vx,vy,size,flash):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.flash = flash

    @classmethod
    def createStar(self,galaga,randomStar):
        """Choose random variables to create a circle which simulates stars
            with a paralax effect."""
        x = random.randint(0,galaga.screenWidth)
        if randomStar == False:
            y = 0
        else:
            y = random.randint(0,galaga.screenHeight)
        vx = 0
        vy = -random.choice(galaga.starSpeeds) 
        size = random.choice(galaga.starSizes) 
        flash = random.randint(0,galaga.fps/2)
        return Star(x,y,vx,vy,size,flash)

    def draw(self,galaga):
        pygame.draw.circle(galaga.screen,(255,255,255),\
        (int(self.x*galaga.scaleFactor),int(self.y*galaga.scaleFactor)),
        self.size)
##########
#Enemies!#
##########
        
class Enemy(PhysObj):
    flutterImage = True
    flutterCount = 0
    floatOn = True
    floatCount = 0
    maxAttackingEnemies = 1
    attackingEnemies = 0
    maxMissiles = 2
    missilesFired = 0
    shotChance = .01
    speedValue = 1 # Higher Values == Faster Movement 
    
    def __init__(self,x,y,vx,vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.path = []
        self.isAlive = True
        self.isFlying = False
        self.isAttacking = False
        self.floatX = self.homeX - self.width/2 
        self.floatY = self.homeY - self.height/2
        self.attackIndex = 0
        self.speed = Enemy.speedValue 
        self.angle = 0
        self.angleFound = False

    @classmethod   
    def flutterCheck(self,galaga):
        if self.flutterImage == True:
            self.flutterCount += 1
            if self.flutterCount == int(galaga.fps):
                self.flutterCount = 0
                self.flutterImage = False
        else:
            self.flutterCount += 1
            #Next Line: "Flutter" Twice per second.
            if self.flutterCount == int(galaga.fps)/2:  
                self.flutterImage = True

    def move(self):
        self.floatX += self.floatVX
        self.floatY += self.floatVY
        super(Enemy,self).move()

    def flutter(self):
        if self.flutterImage == True:
            self.image = self.openImage
            self.width = self.openImageWidth
            self.height = self.openImageHeight
        else:
            self.image = self.closedImage
            self.width = self.closedImageWidth
            self.height = self.closedImageHeight

    @classmethod
    def floatCheck(self,galaga):
        if self.floatOn == True:
            self.floatCount += 1
            if self.floatCount == int(galaga.fps*2):
                self.floatCount = 0
                self.floatOn = False
        else:
            self.floatOn = True

    def floatOut(self):
        if Enemy.floatOn == False:
            (self.floatVX,self.floatVY) = (-self.floatVX,-self.floatVY)
            
    def importSprites(self,closedImagePath,openImagePath):
        (self.closedImage,self.closedImageHeight,self.closedImageWidth) = \
              importImage(closedImagePath,True) #True == Alpha
        (self.openImage,self.openImageHeight,self.openImageWidth) = \
              importImage(openImagePath,True) #True == Alpha
        self.width = max(self.closedImageWidth,self.openImageWidth)
        self.height = max(self.closedImageHeight,self.openImageHeight)

    def setInitialLocation(self):
        self.x = self.homeX - self.width/2 
        self.y = self.homeY - self.height/2 
        self.vx = 0
        self.vy = 0
        self.image = self.openImage

    def attack(self,galaga,attackNumber):
        self.attackPath = Movement.calculateAttackPath(self,galaga,attackNumber)
        if type(attackNumber) == list:
            self.attackPath.insert(0,(self.x,self.y))
        self.isFlying = True
        self.isAttacking = True
        self.attackIndex = 1

    def update(self,galaga):
        self.flutter()
        self.floatOut()
        self.center = (self.x + self.width/2, self.y + self.height/2)
        if (self.isFlying == False):
            self.x = self.floatX
            self.y = self.floatY
            self.vx = self.floatVX
            self.vy = self.floatVY
        elif self.isFlying: #Enemy is flying.
            speed = self.speed
            startPoint = self.center
            targetPoint = self.attackPath[self.attackIndex]
            if self.attackIndex == 1:
                (self.vx,self.vy) = Movement.calculateVelocity(startPoint,
                                    targetPoint,galaga.PPT,speed)
                if self.collisionWith(targetPoint,True):
                    self.attackIndex += 1
                    startPoint = self.center
                    targetPoint = self.attackPath[self.attackIndex]                    
                    (self.vx,self.vy) = Movement.calculateVelocity(startPoint,
                    targetPoint,galaga.PPT,speed)
            elif self.collisionWith(targetPoint,True): #True == collide with point
                self.hitPoint(galaga)
            elif self.finishedAttack(galaga):
                self.reposition(galaga)
            if (self.vx != 0 and self.vy != 0): #Accidental "double" point.
                self.angle = Movement.calculateAngle(self.vx,self.vy)
            if self.isAttacking:
                self.attemptShot(galaga)
                
            self.rotateSprite(self.angle)
            
    def hitPoint(self,galaga):
        startPoint = self.center
        targetPoint = self.attackPath[self.attackIndex]
        speed = self.speed
        self.attackIndex += 1
        if self.attackIndex==len(self.attackPath):#Completed the movement
            if self.isAttacking:
                self.attackIndex = 0
                self.reposition(galaga)
            else:
                self.attackIndex = 0
                self.adjustToHome()
        else:
            targetPoint = self.attackPath[self.attackIndex]
            (self.vx,self.vy) = Movement.calculateVelocity(startPoint,
                                  targetPoint,galaga.PPT,speed)

    def adjustToHome(self):
        self.x = self.floatX
        self.y = self.floatY
        self.vx = 0
        self.vy = 0
        self.angle = 0
        self.isFlying = False

    def attemptShot(self,galaga):
        midpoint = Paths.midpoint((self.homeX,self.homeY),
                                  galaga.fighter.centerCall())
        if self.y < midpoint[1]:
            if Enemy.missilesFired < Enemy.maxMissiles:
                if random.random() <= Enemy.shotChance:
                    galaga.enemyMissiles.append(self.fireMissile(galaga))

    def finishedAttack(self,galaga):
        xOffset = galaga.baseScreenWidth/2
        yOffset = galaga.baseScreenHeight/2
        if ((self.x < 0 -xOffset or self.x > galaga.baseScreenWidth + xOffset) \
            or (self.y < 0 - yOffset or self.y > galaga.baseScreenWidth +\
                                                                     yOffset)):
            return True
        else:
            return False
        

    def reposition(self,galaga):
        #Reposition to home
        self.x = self.floatX
        self.y = self.floatY
        self.vx = self.floatVX
        self.vy = self.floatVY
        self.isFlying = False
        self.isAttacking = False
        self.angle = 0

    def chooseNearby(self,galaga):
        attackingEnemies = [self]
        offset = galaga.formation.offset
        chosen = 0
        maxAttempts = 6
        maxEnemies = Enemy.maxAttackingEnemies
        for attempt in xrange(maxAttempts):
            if (chosen < maxEnemies):
                enemy = random.choice(galaga.enemyList)
                if enemy not in attackingEnemies and enemy.isAttacking == False:
                    if ((abs(enemy.homeX - self.homeX) < offset * 2) and \
                       (abs(enemy.homeY - self.homeY) < offset * 2)):
                        attackingEnemies.append(enemy)
                        chosen += 1
        return attackingEnemies
             
    def fireMissile(self,galaga):
        startPoint = self.centerCall()
        endPoint = galaga.fighter.centerCall()
        speed = 1.4 #int(galaga.baseScreenHeight/galaga.fps*1.5)

        (vx,vy) = Movement.calculateVelocity(startPoint,endPoint,galaga.PPT,
        speed)

        shooter = "enemy"

        return Missile(self.x+self.width/2,self.y+self.height/2,vx,vy,shooter)

    @classmethod
    def resetClass(self):
        Enemy.floatCount = 0
        Enemy.maxAttackingEnemies = 1
        Enemy.attackingEnemies = 0
        Enemy.maxMissiles = 2
        Enemy.missilesFired = 0
        Enemy.shotChance = .01
        Enemy.speedValue = 1
        
        
        
###########
        
class EnemyGalaga(Enemy):
    def __init__(self,homeX,homeY,galaga):
        self.hitPoints = 2
        self.homeX = homeX
        self.homeY = homeY
        self.sprites()
        self.setInitialLocation()
        explosionPath = "enemy/explosion"
        self.expImages = PhysObj.getExplosions(explosionPath)
        self.deathSound = \
        pygame.mixer.Sound("galaga_sounds/enemy/galaga/galaga_stricken2.wav")
        self.weakSound =\
        pygame.mixer.Sound("galaga_sounds/enemy/galaga/galaga_stricken1.wav")
        self.points = 400
        self.multiplier = 1
        self.attacks = galaga.galagaPaths
        super(EnemyGalaga,self).__init__(self.x,self.y,self.vx,self.vy)

    def sprites(self):
        strongClosedImagePath = \
        "galaga_sprites/enemies/galaga/galaga_strong/galaga_strong_closed.png"
        strongOpenImagePath = \
        "galaga_sprites/enemies/galaga/galaga_strong/galaga_strong_open.png"
        weakClosedImagePath = \
        "galaga_sprites/enemies/galaga/galaga_weak/galaga_weak_closed.png"
        weakOpenImagePath = \
        "galaga_sprites/enemies/galaga/galaga_weak/galaga_weak_open.png"
        self.importSprites(strongClosedImagePath,strongOpenImagePath,
                           weakClosedImagePath,weakOpenImagePath)

    def importSprites(self,strongClosed,strongOpen,weakClosed,weakOpen):
        
        (self.strongClosedImage,self.strongClosedHeight,self.strongClosedWidth)\
              = importImage(strongClosed,True) #True == Alpha
        (self.strongOpenImage,self.strongOpenHeight,self.strongOpenWidth)\
              = importImage(strongOpen,True)
        
        (self.weakClosedImage,self.weakClosedHeight,self.weakClosedWidth)\
              = importImage(weakClosed,True)
        (self.weakOpenImage,self.weakOpenHeight,self.weakOpenWidth)\
              = importImage(weakOpen,True)
        
        self.openImage = self.strongOpenImage
        self.openImageWidth = self.strongOpenWidth
        self.openImageHeight = self.strongOpenHeight
        self.closedImage = self.strongClosedImage
        self.closedImageWidth = self.strongClosedWidth
        self.closedImageHeight = self.strongClosedHeight

        self.width = max(self.openImageWidth,self.closedImageWidth)
        self.height = max(self.openImageHeight,self.closedImageHeight)
        
###########
        
class EnemyButterfly(Enemy):
    def __init__(self,homeX,homeY,galaga):
        self.hitPoints = 1
        self.homeX = homeX
        self.homeY = homeY
        self.importSprites()
        self.setInitialLocation()
        self.attacks = galaga.butterflyPaths
        explosionPath = "enemy/explosion"
        self.expImages = PhysObj.getExplosions(explosionPath)
        
        self.deathSound =\
    pygame.mixer.Sound("galaga_sounds/enemy/butterfly/butterfly_stricken.wav")
        self.points = 80
        self.multiplier = 1
        super(EnemyButterfly,self).__init__(self.x,self.y,self.vx,self.vy)

    def importSprites(self):
        closedImagePath = \
        "galaga_sprites/enemies/butterfly/butterfly_closed.png"
        openImagePath = \
        "galaga_sprites/enemies/butterfly/butterfly_open.png"
        super(EnemyButterfly,self).importSprites(closedImagePath,openImagePath)

###########
        
class EnemyBee(Enemy):
    def __init__(self,homeX,homeY,galaga):
        self.hitPoints = 1
        self.homeX = homeX
        self.homeY = homeY
        self.importSprites()
        self.setInitialLocation()
        self.attacks = galaga.beePaths
        explosionPath = "enemy/explosion"
        self.expImages = PhysObj.getExplosions(explosionPath)
        self.deathSound = \
        pygame.mixer.Sound("galaga_sounds/enemy/bee/bee_stricken.wav")
        self.points = 40
        self.multiplier = 1
        super(EnemyBee,self).__init__(self.x,self.y,self.vx,self.vy)

    def importSprites(self):
        closedImagePath = \
        "galaga_sprites/enemies/bee/bee_closed.png"
        openImagePath = \
        "galaga_sprites/enemies/bee/bee_open.png"
        super(EnemyBee,self).importSprites(closedImagePath,openImagePath)
        
#############
#Explosions!#
#############
        
class Explosion(PhysObj):
    def __init__(self,character,galaga):
        explosionSpeed = 3
        # Next Line: Stores a 3-tuple list of images[0], image width[1],
        # and image height[2].
        self.expImages = character.expImages 
        self.expFrames = len(character.expImages)
        self.expFrameRate = int(round(galaga.fps/explosionSpeed/self.expFrames))
        self.fps = int(galaga.fps)/explosionSpeed
        self.frameIndex = 0
        self.frame = 0
        self.isAlive = True
        self.characterX = character.x
        self.characterY = character.y
        self.characterWidth = character.width
        self.characterHeight = character.height

    def update(self):
        if self.frame >= self.fps:
            self.isAlive = False
        if self.frame != 0 and self.frame % self.expFrameRate == 0:
            self.frameIndex += 1   
        self.frame += 1

    def draw(self,galaga):
        self.image = self.expImages[self.frameIndex][0]
        self.width = self.expImages[self.frameIndex][1]
        self.height = self.expImages[self.frameIndex][2]
        self.x = self.characterX + self.characterWidth/2 - self.width/2
        self.y = self.characterY + self.characterHeight/2 - self.height/2
        super(Explosion,self).draw(galaga)
        
#############
#Formations!#
#############
        
class Formations(object):
    def __init__(self,formation,galaga):
        self.formation = formation
        self.defineEnemies()
        self.makeFormation(galaga)

    def defineEnemies(self):
        if self.formation == 1:
            self.totalEnemies = 36
            self.bossGalaga = 4
            self.butterflies = 16
            self.bees = 16
            self.enemiesPerRow = 8
            self.rows = math.ceil((self.totalEnemies*1.0)/self.enemiesPerRow)
        
    def makeFormation(self,galaga):
        positionList = []
        #Next Line: 21 Pixels is the base size of an enemy location
        self.offset = offset = 21 * Galaga.baseScaleFactor
        if self.formation == 1:
            #Central Points of Formation, used to apply "floating" animation
            #effect. 
            self.formationX = galaga.screenWidth/2
            self.formationY = self.offset + galaga.header
            totalEnemies = self.totalEnemies
            bossGalaga = self.bossGalaga
            enemiesPerRow = self.enemiesPerRow
            for position in xrange(totalEnemies):
                if (position <= (bossGalaga-1)): #Top 4 Boss Galagas
                    row = 0
                    rowPosition = position
                    posX = ((galaga.screenWidth/2 - offset*(bossGalaga/2))\
                            +offset/2+offset*rowPosition)
                    posY = (offset + offset*row + galaga.header) #1 empty space above enemies
                    positionList.append([posX,posY])
                else: #Basic enemy
                    row = (position-bossGalaga)/enemiesPerRow + 1
                    rowPosition = position % enemiesPerRow
                    #Leftmost Position In Row + Actual Row Position
                    posX = ((galaga.screenWidth/2 - offset*(enemiesPerRow/2))\
                            +offset/2+offset*rowPosition)
                    
                    posY = (offset + (offset*.75)*row + galaga.header)
                    positionList.append([posX,posY])
        self.positionList = positionList

###########
#Movement!#
###########

class Movement(object):
    @classmethod
    def calculateFloat(self,character,galaga):
        (xFloat,yFloat) = self.floatDistance(character,galaga)
        
        #Distance traveled per tick
        xTick = xFloat / (galaga.fps)
        yTick = yFloat / (galaga.fps)

        return (xTick,yTick)
    
    @classmethod    
    def floatDistance(self,character,galaga):
        #Calculate furthest possible x and y position from formation center
        wideOffset=abs(galaga.formation.offset * galaga.formation.enemiesPerRow)
        heightOffset=(galaga.formation.offset * galaga.formation.rows)

        #Calculate Character's distance from formation center
        xDistance = -(galaga.formation.formationX - character.homeX)
        yDistance = -(galaga.formation.formationY - character.homeY)

        #Calculate Ratio of distance from formation center
        xRatio = xDistance/(wideOffset*1.0)
        yRatio = yDistance/(heightOffset*1.0)

        #Total Distance character should travel while floating
        xFloat = galaga.formation.offset * xRatio
        yFloat = galaga.formation.offset * yRatio

        return (xFloat,yFloat)

    @classmethod
    def calculateAttackPath(self,enemy,galaga,attackPath):
        if attackPath == 1:
            return Paths.basicPath(enemy,galaga.fighter)
        elif attackPath == 2:
            return Paths.aroundFighter(enemy,galaga.fighter)
        else:
            return copy.deepcopy(attackPath)

    @classmethod
    def calculateVelocity(self, startPoint,targetPoint,PPT,speed):
        (startX,startY) = (startPoint[0],startPoint[1])
        (targetX,targetY) = (targetPoint[0],targetPoint[1])

        #"Hypotenuse"
        distance = ((targetX - startX)**2 + (targetY - startY)**2)**0.5
        if almostEqual(distance,0,.00000001):
            return (0,0)

        #Regulates speed based on distance. 
        velocity = distance / PPT #Pixels Per Tick
    
        #Total Distance traveled in x and y planes. 
        vector = ((targetX - startX),(targetY - startY))

        xVelocity =  (vector[0] / velocity) * speed 
        yVelocity =  (vector[1] / velocity) * speed
        
        return (xVelocity,yVelocity)

    @classmethod
    def distance(self,startPoint,targetPoint):
        x1 = startPoint[0]
        y1 = startPoint[1]
        x2 = targetPoint[0]
        y2 = targetPoint[1]
        return (((x2-x1)**2+(y2-y1)**2)**0.5)
    

    @classmethod
    def calculateAngle(self,vx,vy):
        #Undefined Slopes
        if (vx < 0 and vy == 0):
            angle = 90
        elif (vx > 0 and vy ==0):
            angle = -90
        elif (vy == 0 and vx == 0):
            return None
        else:
            if vy > 0: #Moving Downward    
                angle = math.degrees(math.atan(vx/vy)) + 180 #Inverts image
            else: 
                angle = math.degrees(math.atan(vx/vy))
        return angle
    
#######
#PATHS#
#######

class Paths(object):

    @classmethod
    def midpoint(self,enemyPoint,fighterPoint):
        enemyX = enemyPoint[0]
        enemyY = enemyPoint[1]
        fighterX = fighterPoint[0]
        fighterY = fighterPoint[1]

        xChange = (fighterX - enemyX)/2
        yChange = (fighterY - enemyY)/2

        return (enemyX + xChange,enemyY + yChange)

    @classmethod
    def repositionMe(self,enemy):
        pointList = []

        enemyPoint = enemy.centerCall()
        pointList.append(enemyPoint)

        targetPoint = (enemy.homeX,enemy.homeY)

        midpoint = Paths.midpoint(enemyPoint,targetPoint)
        pointList.append(midpoint)
        pointList.append(targetPoint)

        return pointList
            
        
        
    @classmethod
    def basicPath(self,enemy,fighter): #Basic single swirl path at midpoint. 
        pointList = []

        enemyPoint = enemy.centerCall() #First Point
        pointList.append(enemyPoint)

        if enemy.x - fighter.x < 0:
            flipX = True
        else:
            flipX = False
        newPoints = self.starting180Turn(pointList[len(pointList)-1],flipX)
        pointList.extend(newPoints)

        midPoint = Paths.midpoint(enemyPoint,fighter.centerCall())
        pointList.append(midPoint)

        #Next Line: 200 == size in pixels
        newPoints = self.fullCircle(pointList[len(pointList)-1],flipX,200)
        pointList.extend(newPoints)

        fighterPoint = fighter.centerCall()
        
        #End Point off the screen
        endPoint = (fighterPoint[0],fighterPoint[1]+fighter.height*2)

        pointList.append(fighterPoint)
        pointList.append(endPoint)

        return pointList

    @classmethod
    def aroundFighter(self,enemy,fighter):
        pointList = []
        if enemy.x - fighter.x < 0:
            flipX = True
        else:
            flipX = False

        if flipX == True:
            coefficient = 1
        else:
            coefficient = -1

        enemyPoint = enemy.centerCall()
        pointList.append(enemyPoint)

        midPoint = Paths.midpoint(enemyPoint,fighter.centerCall())
        twoFifths = Paths.midpoint(enemyPoint,midPoint)

        fighterPoint = fighter.centerCall()

        sideOfFighter = (fighterPoint[0] + (coefficient * (fighter.width * 4)),
                 fighterPoint[1] - (fighter.height))

        vector = (twoFifths[0]-sideOfFighter[0],twoFifths[1]-sideOfFighter[1])
        angle = Movement.calculateAngle(vector[0],vector[1])

        pointList.append(twoFifths)

        newPoints = Paths.curve(twoFifths,abs(angle),100,not(flipX),True)
        pointList.extend(newPoints)

        pointList.append(sideOfFighter)

        #Next Line: 300 == Size in pixels
        newPoints = self.fullCircle(pointList[len(pointList)-1],flipX,350)
        pointList.extend(newPoints)

        endPoint = (sideOfFighter[0],sideOfFighter[1]+fighter.height*2)
        pointList.append(endPoint)

        return pointList

    @classmethod
    def curve(self,lastPoint,degreeTurn,size,flipX,flipY):
        pointList = [lastPoint]
        angleIncrement = 5 #Tighter increments produce smoother curves
        pointIndex = 0 #What is the index of the last point in the list?
        angleIndex = 1 #Which angle measurement is this? 
        circumference = size * Galaga.baseScaleFactor #Size of curve.
        steps = int(degreeTurn / angleIncrement) #Degree Turn 
        stepDistance = int(circumference / steps) #hypotenuse
        for step in xrange(steps-1):
            angle = math.radians(angleIncrement * angleIndex)
            xDifference = (math.sin(angle) * stepDistance)
            yDifference = (math.cos(angle) * stepDistance)
            yDifference = -yDifference
            if flipX == True:
                xDifference = -xDifference
            if flipY == True:
                yDifference = -yDifference
            lastPointX = pointList[pointIndex][0]
            lastPointY = pointList[pointIndex][1]
            newX = lastPointX + xDifference
            newY = lastPointY + yDifference
            pointList.append((newX,newY))
            angleIndex += 1
            pointIndex += 1
        return pointList

    @classmethod
    def starting180Turn(self,lastPoint,flipX):
        pointList = [lastPoint]
        angleIncrement = 5 #Tighter increments produce smoother curves
        pointIndex = 0 #What is the index of the last point in the list?
        angleIndex = 1 #Which angle measurement is this? 
        circumference = 100 * Galaga.baseScaleFactor #Size of curve.
        degreeTurn = 180
        steps = int(degreeTurn / angleIncrement) #Degree Turn 
        stepDistance = int(circumference / steps) #hypotenuse
        for step in xrange(steps-1):
            angle = math.radians(angleIncrement * angleIndex)
            xDifference = (math.sin(angle) * stepDistance)
            yDifference = (math.cos(angle) * stepDistance)
            yDifference = -yDifference
            if flipX == True:
                xDifference = -xDifference
            lastPointX = pointList[pointIndex][0]
            lastPointY = pointList[pointIndex][1]
            newX = lastPointX + xDifference
            newY = lastPointY + yDifference
            pointList.append((newX,newY))
            angleIndex += 1
            pointIndex += 1
        return pointList

    @classmethod
    def fullCircle(self,lastPoint,flipX,size):
        pointList = [lastPoint]
        angleIncrement = 5 #Tighter increments produce smoother curves
        pointIndex = 0 #What is the index of the last point in the list?
        angleIndex = 1#Which angle measurement is this? 
        circumference = size * Galaga.baseScaleFactor #Size of curve.
        degreeTurn = 360
        steps = int(degreeTurn / angleIncrement) #Degree Turn 
        stepDistance = int(circumference / steps) #hypotenuse
        for step in xrange(steps-1):
            angle = math.radians(angleIncrement * angleIndex)
            xDifference = (math.sin(angle) * stepDistance)
            yDifference = (math.cos(angle) * stepDistance)
            if flipX: # Which side is the enemy on?
                xDifference = -xDifference
            lastPointX = pointList[pointIndex][0]
            lastPointY = pointList[pointIndex][1]
            newX = lastPointX + xDifference
            newY = lastPointY + yDifference
            pointList.append((newX,newY))
            angleIndex += 1
            pointIndex += 1
        return pointList

##########
#BUTTONS!#
##########

class Button(object):
    buttonList = []
    def __init__(self,location,scale,regImagePath,lgtImagePath = None,justify= "c"):
        if lgtImagePath == None:
            lgtImagePath = regImagePath
        self.scale = scale
        self.regFile = regImagePath
        self.lgtFile = lgtImagePath
        (self.regImage,self.regImageHeight,self.regImageWidth) = \
        importImage(self.regFile,True,self.scale)
        (self.lgtImage,self.lgtImageHeight,self.lgtImageWidth) = \
        importImage(self.lgtFile,True,self.scale)
        if justify == "c": #center
            (self.x,self.y) = (location[0] - self.regImageWidth/2,
                               location[1] - self.regImageHeight/2)
        elif justify == "t": #top
            (self.x,self.y) = (location[0] - self.regImageWidth/2,
                               location[1])
        else:
            (self.x,self.y) = (location[0] - self.regImageWidth/2,
                               location[1] - self.regImageHeight/2)            
        self.width = self.regImageWidth
        self.height = self.regImageHeight
        self.image = self.regImage
        self.buttonList.append(self)

    def touching(self,mouse,galaga):
        hitBoxX0 = self.x * galaga.scaleFactor
        hitBoxY0 = self.y * galaga.scaleFactor
        hitBoxX1 = hitBoxX0+(self.width*galaga.scaleFactor)
        hitBoxY1 = hitBoxY0+(self.height*galaga.scaleFactor)
        if (mouse[0] >= hitBoxX0 and mouse[0] <= hitBoxX1) and \
            (mouse[1] >= hitBoxY0 and mouse[1] <= hitBoxY1):
            return True
        else:
            return False

    def draw(self,galaga):
        galaga.screen.blit(\
        pygame.transform.scale(self.image,
                               (int(self.regImageWidth * galaga.scaleFactor),
                               int(self.regImageHeight * galaga.scaleFactor))),
                                (int(self.x * galaga.scaleFactor),
                                 int(self.y * galaga.scaleFactor)))

Galaga()

  

        
