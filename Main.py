#!/usr/bin/env python

# Import the pygame library and initialise the game engine
import pygame
import sys
import math
import random
import time
pygame.init()
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.


# Open a new window
WinSize = [1000, 900]
size = (WinSize[0], WinSize[1])
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Space Adventures")


# Global Variables
score = 0
FPS = 60
Speed = 30
Espeed = 5
Color = [0,0,1]
cSwitch = False

# All of our sprites
class CreatePlayer(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.x = 1000 - 210
		self.y = 900 - 190
		self.image = pygame.image.load('SpaceShip.png')
		self.rect = pygame.Rect(self.x,self.y,210,190) #The rect for collision detection.
		self.health = 100

class CreateEnemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 580
        self.y = 420
        self.image = pygame.image.load("EnemyMissle.png")
        self.rect = pygame.Rect(self.x,self.y,110,90)
        self.status = "hit"
        self.Damage = 10

class CreateBoom(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("Explosion.png")

class CreateBullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 0
        self.image = pygame.image.load("Bullet.png")
        self.rect = pygame.Rect(self.x, self.y, 30, 80)
        self.status = "chambered"
        self.speed = 50
        self.attack = "beeline"

# We create the player object
Player = CreatePlayer()
# We create the enemy object
Missle = CreateEnemy()
# We create the explosion FX
Explosion = CreateBoom()
# We make the bullet
Bullet = CreateBullet()

# Game Loop and clock
GameOver = False
clock = pygame.time.Clock()


# This function works specificallSpaceShipImgy for the KEYDOWN function
# 10(1) = initial interval and 10(2) = repeat interval
pygame.key.set_repeat(10,10)

# This function can detect collision between two different sprites
def col_check(x,y,w,h,x2,y2,w2,h2):
    if (x < (x2 + w2) and (x + w) > x2 and y < (y2 + h2) and (h + y) > y2):                     
        return True

while GameOver:
    pygame.display.update()
    screen.fill(Color)
    clock.tick(FPS)
    

while not GameOver:

    if Player.health <= 0:
        GameOver = True
    
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              pygame.display.quit()
              pygame.quit()
              sys.exit()
        
        if event.type == pygame.KEYDOWN: # event space for user Key input
            
            if event.key == pygame.K_RIGHT:
				if (Player.x + 210 >= WinSize[0]):
					Player.x = WinSize[0] - 210
					
				else:
					Player.x += Speed

                
            if event.key == pygame.K_LEFT:        
                if (Player.x <= 0):                # Left side collision
                    Player.x = 0
                    
                else:                             # Left Side movement
                    Player.x -= Speed
            
            if event.key == pygame.K_UP:
                if (Player.y <= 0):                # Up side collision
                    Player.y = 0
                
                else:                             # Up side movement
                    Player.y -= Speed
                
            if event.key == pygame.K_DOWN:
                if (Player.y + 190 >= WinSize[1]): # Down side collision
                    Player.y = WinSize[1] - 190
                
                else:                             # Down side movement
                    Player.y += Speed
            
            if event.key == pygame.K_SPACE:
                # Make it shoot a bullet
                if Bullet.status == "chambered":
                    Bullet.status = "shot"
                    Bullet.x = Player.x + 90
                    Bullet.y = Player.y
 
 
 
    # --- Drawing code should go here
    
    # Missle
    PointAngle = math.atan2(Player.y - Missle.y, Player.x - Missle.x)
    MissleSurf = pygame.transform.rotate(Missle.image, 270 - PointAngle * 57.29) # 270 and 57.29 are random numbers found online / 360
    screen.blit(MissleSurf, (Missle.x, Missle.y))
    
    # Choose a random attack to use
    # This doesn't work
    # MAKE SURE TO CHECK IF THIS IS CORRECT!!!!
    attack = random.randrange(1,2)
    if attack == 1:
        Missle.attack = "beeline"
    elif attack == 2:
        Missle.attack = "flank"
    
    # I added this in order for different 'Enemy Types' with miminal effort
    if Bullet.attack == "beeline":
        # x axis movement
        if Player.x > Missle.x:
            Missle.x += Espeed
        
        if Player.x < Missle.x:
            Missle.x -= Espeed
        
        # y axis movement
        if Player.y > Missle.y:
            Missle.y += Espeed
    
        if Player.y < Missle.y:
            Missle.y -= Espeed
    
    if Bullet.attack == "flank":
        Espeed = 10
        # y axis movement
        if Player.y + 50 > Missle.y:
            Missle.y += Espeed
        elif Player.y + 50 <= Missle.y:
            Missle.y -= Espeed
            if Player.x > Missle.x:
                Missle.x += Espeed
            
            if Player.x < Missle.x:
                Missle.x -= Espeed
    
    # "Deletes" The missle and spawns a new one
    # I'll have to iron out a better gameplay loop later
    if Missle.status == "hit":
        screen.blit(Explosion.image,(Missle.x, Missle.y))
        Missle.x = random.randint(0, 1000)
        Missle.y = 0
        Missle.status = "normal"
    
    # Player
    screen.blit(Player.image, (Player.x, Player.y)) # paint to screen
    
    # Bullet
    #if score >= 1500:
        #Bullet.attack = "flank"
    if Bullet.status == "shot":
        screen.blit(Bullet.image, (Bullet.x, Bullet.y))
        Bullet.y -= Bullet.speed
    if Bullet.y <= 0:
        Bullet.status = "chambered"
    
    # Collision
    if col_check(Player.x, Player.y, 210, 190, Missle.x, Missle.y, 110, 90):
        screen.blit(Explosion.image, (Player.x +30, Player.y + 20)) # we have to offset the player x and y for convincing effect
        Player.health -= Missle.Damage # Decreases the player health
        Missle.status = "hit"
        print(Player.health)
    
    if col_check(Missle.x, Missle.y, 110, 90, Bullet.x, Bullet.y, 30, 80):
        Missle.status = "hit"
        score += 100
        Espeed += 0.1
        print("Score: ",score)
        
    
    if Color[2] >= 120:
        cSwitch = True
        Color[2] -= 5
    elif Color[2] <= 20:
        cSwitch = False
        Color[2] += 5
    
    if cSwitch == False:
        Color[2] += 2
    elif cSwitch == True:
        Color[2] -= 2
    
    
    # Personal High Score 23600
    # See if you can beat it
    
    pygame.display.update()
    screen.fill(Color)
    clock.tick(FPS)
    
