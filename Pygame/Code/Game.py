import pygame
from pygame import mixer
import math
import random

# Initialise pygame
pygame.init()

# Create the creen with width and height
screen = pygame.display.set_mode( (800, 600) )

# Load background image

background = pygame.image.load('background.png')

# Load background music
mixer.music.load('background.wav')

# Set background music volume
mixer.music.set_volume(0.2)
# Play background music
mixer.music.play(-1)


# Set caption
pygame.display.set_caption('Space Invaders')

# Load icon image
icon = pygame.image.load('ufo.png')
# Set icon image
pygame.display.set_icon(icon)
# Load spaceship image
playerImg = pygame.image.load('player.png')

# Set player image
playerX = 370
playerY = 480
# Set plater speed
playerSpeed = 5


# Diplay player
def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemies variables
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

#Display enemies
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Bullet variables
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready' # Fire bullet when ready

# Fire bullet 
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire" # Bullet moving
    screen.blit(bulletImg, (x + 16, y + 10))

# Collision functions
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt( math.pow(enemyX - bulletX, 2)+ (math.pow(enemyY - bulletY, 2)))
    
    if distance < 27:
        return True
    else:
        return False

# Score variables
score_value = 0
font =  pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Game over function
def game_over_text():
    over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Scoring function
def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

    
#----Game loop----

# Stores down keys
down_keys = []

running = True

while running:
    # Set background to white
    screen.fill( (255, 255, 255) )

    # Set background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Quits game if user presses red x button
            running = False
        
        # Get down keys
        if event.type == pygame.KEYDOWN:
            print(event.unicode)
            down_keys.append(event.key)
            
        if event.type == pygame.KEYUP:
            down_keys.remove(event.key)
            
    # Check down_keys to change movement

    # Move left
    if pygame.K_LEFT in down_keys:
        playerX -= playerSpeed
        
    # Move right
    if pygame.K_RIGHT in down_keys:
        playerX += playerSpeed

    # Keep player within screen
    if playerX < 0:
        playerX = 0

    elif playerX > 736:
        playerX = 736
        
    
    # Bullet logic
    ## Check if space key is pressed
    # Bullet logic
    if pygame.K_SPACE in down_keys:
        if bullet_state == "ready":
            bulletSound = mixer.Sound("laser.wav")
            bulletSound.set_volume(0.05)
            bulletSound.play()

            bulletX = playerX # Getting the current X coords of the player
            fire_bullet(bulletX, bulletY)

    # Bullet logic part 2
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
        
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Score logic
    show_score(textX, textY)
    

    # Enemy movement
    # Enemy logic
    for i in range(num_of_enemies):

        # Game over logic
        if enemyY[i] > 440:
            # Move enemies out of the sreen
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
            
        enemyX[i] += enemyX_change[i]
        
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
            
    

        # Collision logic
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.set_volume(0.05)
            explosionSound.play()

            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    
    # Display player
    player(playerX, playerY)
  
    # Update game
    pygame.display.update()
# Quits pygame
pygame.quit()
