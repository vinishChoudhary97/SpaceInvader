#================================================================================================
#
#
#
#
#
#
#
#
#================================================================================================

import pygame
import random
import math
from pygame import mixer
# initialise pygame module
pygame.init()

#============== Game Window =====================================================
# game window of width 800px and height 600px
screen = pygame.display.set_mode((800,600))

# Title and logo of game window
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("images\\ufo.png")
pygame.display.set_icon(icon)

#load background image
backgroundImg = pygame.image.load("images\\background.png")
#===============================================================================

#===================Draw player ================================================
#load player image
playerImg = pygame.image.load("images\player.png")
#player coordinates
playerX = 390
playerY = 480
playerXChange = 0 #speed of player 

# function to draw player image on screen
def player(X,Y):
    screen.blit(playerImg,(X,Y))
# ================================================================================

#================== Draw multiple Enemy ===================================================
# no of enemies
noOfEnemies = 6
# enemy variables list
enemyImg = []
enemyX = []
enemyY = []
enemyXChange = []
enemyYChange = []
# setting value of variable for each enemies
for i in range(noOfEnemies):   
#load enemy image
    enemyImg.append(pygame.image.load("images\enemy.png"))
#enemy coordinates
    enemyX.append(random.randint(30, 735))
    enemyY.append(random.randint(50,150))
    enemyXChange.append(4)
    enemyYChange.append(40)

# function to draw player image on screen
def enemy(enemyImg,X,Y):
    screen.blit(enemyImg,(X,Y))
# ========================================================================================

#=================== Draw bullet =========================================================
#load bullet image
bulletImg = pygame.image.load("images\\bullet.png")
#bullet coordinates
bulletX = 0
bulletY = 480
bulletXChange = 0
bulletYChange = 40
# bullet state 
# ready = when bullet is not visible on screen (not fired)
# fire = when bullet is movement on screen or fired
bulletState = "ready"

# bullet fire function
def fireBullet(x,y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg , (x+16, y+10))
#===========================================================================================

#============= Score =======================================================================
scoreValue = 0
font= pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10

def showScore(x,y):
    score = font.render("Score : " + str(scoreValue) , True ,(255,255,255))
    screen.blit(score,(x,y))
# ==========================================================================================
#============= Game over text ==============================================================
overFont = pygame.font.Font("freesansbold.ttf",64)
def gameOver():
    overText = overFont.render("GAME OVER",True,(255,255,255))
    screen.blit(overText,(200,250))

#============= Background music ============================================================
mixer.music.load("sounds\\background.wav")
mixer.music.play(-1)
# ==========================================================================================

#============= Collision Function ==========================================================
def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False
#===========================================================================================

# game running variable (default True)
running = True
#==================== game loop============================================================== 
while running:

    #=============== loop through events in game window=====================================
    for event in pygame.event.get():
        # check if Quit is pressed if yess than running variable = false
        if event.type == pygame.QUIT:
            running = False
        
        #Check for event key pressed
        if event.type == pygame.KEYDOWN:
            # check if key is Left move in left
            if event.key == pygame.K_LEFT:
                playerXChange = -5
            # check if key is Right move in right
            if event.key == pygame.K_RIGHT:
                playerXChange = 5
            # call fire bullet function when space bar is pressed
            if event.key == pygame.K_SPACE :
                #add bullet fire sound
                bulletSound = mixer.Sound("sounds\laser.wav")
                bulletSound.play()
                if bulletState == "ready":
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)
        #check for if key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXChange = 0
        # ================================================================================

    # ============player movement=========================================================
    playerX += playerXChange 
    # ===========================================================================

    #================ set background ============================================
    screen.fill((50,50,50))
    #background image
    screen.blit(backgroundImg , (0,0))
    # ============================================================================

    #================= boundaries conditions for player ==========================
    if playerX <= 0 :
        playerX = 0
    elif playerX>= 736:
        playerX = 736
    # =============================================================================

    #======== boundary condition and collision for each enemy enemy ===============
    for i in range(noOfEnemies):
        #================ enemy Movement ============================================
        enemyX[i] += enemyXChange[i] 
        if enemyY[i] > 420:
            for j in range(noOfEnemies):
                enemyY[j] = 2000
            gameOver()
            break          
        # ===========================================================================
        if enemyX[i] <= 0 :
            enemyXChange[i] = 4
            enemyY[i] += enemyYChange[i]
        elif enemyX[i]>= 736:
            enemyXChange[i] = -4
            enemyY[i] += enemyYChange[i]
        #==================== Check For Collision ============================================
        collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision :
            killSound = mixer.Sound("sounds\explosion.wav")
            killSound.play()
            bulletY = 480
            bulletState = "ready"
            scoreValue += 1
            enemyX[i] = random.randint(30, 735)
            enemyY[i] = random.randint(50,150)
        #====================================================================================
        # call enemy func to draw enemy on screen
        enemy(enemyImg[i],enemyX[i],enemyY[i] )
        
    #=================================================================================

#==================== bullet movement==================================================
    if bulletState == "fire":
        fireBullet(bulletX,bulletY)
        bulletY -= bulletYChange
    #================ Multiple bullet fire ============================================
    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"
    #=================================================================================
#=====================================================================================


    #call player func to draw player on screen
    player(playerX,playerY )
    showScore(textX,textY)
    # update display of game window
    pygame.display.update()

