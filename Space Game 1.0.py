import pygame  # This is needed to access the functions of pygame
import math  # This is required to detect the collision between the bullet and the enemy
import random  # This package will allow us to randomize where the enemies spawn after being shot
from pygame import mixer  # Allows for music or sound effects to be added to the game

# Initialize the pygame
pygame.init()

# Create the window screen
screen = pygame.display.set_mode((800, 600))

# Background

background = pygame.image.load('Spaceshipbackground.png')

# Background Sound
mixer.music.load('background.wav')  # Background music file
mixer.music.play(-1)  # The "-1" will allow for it to play on loop/forever

# Title and Icon
pygame.display.set_caption("SpaceMania.")  # Adding the title/captions
icon = pygame.image.load('startup (1).png')  # Adding the icon
pygame.display.set_icon(icon)  # Icon Function

# Player
playerImg = pygame.image.load('001-space-invaders.png')
playerX = 370  # The X axis of where the spaceship will appear
playerY = 480  # The Y axis of where the spaceship will appear
playerX_change = 0  # This allows the spaceship to stop when the left or right key is released

# Enemy
enemyImg = []  # This signifies an empty list, where we will put values in
enemyX = []  # Each time the game is run, each of these square brackets will have a random value added to them
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# Append - Adds values to the list

# The "for i in range" command repeats the coding that it precedes, 6 consecutive times

for i in range(num_of_enemies):  # This loop will run for 6 times and therefore, 6 enemies will be created
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))  # Randomizes the coordinate that the enemies spawn
    enemyY.append(random.randint(50, 150))  # The enemies will spawn somewhere in between these coordinates
    enemyX_change.append(4)  # The speed of the enemies on the x-axis
    enemyY_change.append(40)  # When the enemy hits the boundary, they'll move down 40 pixels

# Bullet

# Ready - You can't see the bullet on the screen, because it hasn't yet been fired
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0  # The x-axis of the bullet will be changed depending on the movement of the spaceship
bulletY = 480  # The starting point y-axis of the bullet will always be at 480 pixels
bulletY_change = 10  # The speed of the bullet
bullet_state = 'ready'

# Font

score_value = 0  # You will start with a score of 0
font = pygame.font.Font('freesansbold.ttf', 32)  # Creates the font type and font size of the scoreboard

textX = 10  # X coordinate of the scoreboard
textY = 10  # Y coordinate of the scoreboard

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))  # Detailing the text and rendering it
    screen.blit(score, (x, y))  # Draws the scoreboard into the game


def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))  # Detailing the text and rendering
    screen.blit(over_text, (200, 250))  # Draws the scoreboard into the game in the middle of the screen


def player(x, y):  # The coordinates of the spaceship on the screen
    screen.blit(playerImg, (x, y))  # Draws image of the spaceship at its given x and y-axis coordinates


def enemy(x, y, i):  # The i value specifies all 6 enemies
    screen.blit(enemyImg[i], (x, y))  # Draws the enemies into the game, over the background


def fire_bullet(x, y):  # This function helps with shooting the bullet
    global bullet_state  # "Global" allows the "bullet_state" variable to be accessed within functions
    bullet_state = 'fire'  # The bullet is shot and is in motion
    screen.blit(bulletImg, (x + 16, y + 10))  # Draw the bullet on the screen.
    # The "+16" and "+10" cause the bullet to be centered slightly above the spaceship, making it more realistic


def isCollision(enemyX, enemyY, bulletX, bulletY):  # Detects collision between bullet and enemy
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))  # Math formula that calculates distance between bullet and enemy
    if distance < 27:  # If the distance between the bullet and enemy is less than 27 pixels
        return True  # The collision has occurred
    else:
        return False  # Or else, the collision has not occurred


# Game Loop (Infinite loop that helps run your game forever)
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))  # These 3 values let you implement any colour onto the screen through combinations

    # Background image
    screen.blit(background, (0, 0))  # This allows for the background image to always stay in the game

    # The quit function
    for event in pygame.event.get():  # This line of code is an event function that gives the user control
        if event.type == pygame.QUIT:  # If the user presses the exit button, the infinite loop is disabled
            running = False

        # Controlling the movement of the spaceship left and right
        if event.type == pygame.KEYDOWN:  # This line checks for keystroke presses
            if event.key == pygame.K_LEFT:  # If left key is pressed...
                playerX_change = -6  # the x-axis of the player is changed by -6
            if event.key == pygame.K_RIGHT:  # If right key is pressed...
                playerX_change = 6  # the x-axis of the player is changed by +6

            if event.key == pygame.K_SPACE:  # When space bar is pressed
                if bullet_state == 'ready':  # Allows for you to only shoot, after the bullet is out of screen
                    bullet_sound = mixer.Sound('laser.wav')  # Sound effect whenever a bullet is shot
                    bullet_sound.play()

                    bulletX = playerX  # Gets the current x coordinate of the spaceship
                    fire_bullet(bulletX, bulletY)  # Fire function
        if event.type == pygame.KEYUP:  # Detects when you release keystroke
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # If left or right arrow key is released
                playerX_change = 0  # Stops the spaceship from moving after keystroke is released

    # Increases or decreases x-coordinate of spaceship, depending on the value of playerX_change
    playerX += playerX_change

    # Checking for boundaries of spaceship, so that it doesn't go out of bounds
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # Take into consideration the size of the spaceship
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:  # If any of the enemies reach a y coordinate of 440 pixels
            for j in range(num_of_enemies):  # Specifies all 6 enemies
                enemyY[j] = 2000  # All the enemies are moved out of the screen at a y coordinate of 2000 pixels
            game_over_text()
            break  # The loop is ended

        # The [i] specifies all 6 enemies and therefore implements the same movement for all of them
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:  # If an enemy hits the left side of the screen
            enemyX_change[i] = 5  # The enemy moves to the other direction by having it X value increased
            enemyY[i] += enemyY_change[i]  # If enemy hits right side, they move 40 pixels down
        elif enemyX[i] >= 736:  # If an enemy hits the right side of the screen
            enemyX_change[i] = -5  # They will move to the other direction by having their X value decreased
            enemyY[i] += enemyY_change[i]  # If enemy hits left side, they move 40 pixels down

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)  # The collision function
        if collision:  # If collision has occurred
            explosion_sound = mixer.Sound('explosion.wav')  # Explosion sound effect upon collision
            explosion_sound.play()
            bulletY = 480  # The bullet resets to its starting point
            bullet_state = 'ready'  # Change the state of the bullet to ready
            score_value += 1  # Increases the score by 1 everytime the enemy is hit
            enemyX[i] = random.randint(0, 735)  # Randomizes x coordinate of the spawn point of the enemy, after being shot
            enemyY[i] = random.randint(50, 150)  # Randomizes y coordinate of the spawn point of the enemy, after being shot

        enemy(enemyX[i], enemyY[i], i)  # Draws all the enemies
        # The "i" specifies which x and y coordinates you want to be drawn on the screen

    # Bullet movement
    if bulletY <= 0:  # If bullet is out of the screen/crosses the 0 coordinate
        bulletY = 480  # The location of the bullet will reset to 480 pixels.
        bullet_state = 'ready'  # The state of the bullet will be changed to ready

    if bullet_state == 'fire':  # If the bullet state is "fire" or is in motion
        fire_bullet(bulletX, bulletY)  # The fire function
        bulletY -= bulletY_change  # Reduces the y value of the bullet, which moves it up

    player(playerX, playerY)  # Draws the image of the player onto the screen, over the background
    show_score(textX, textY)  # Maintains the scoreboard throughout the whole game
    pygame.display.update()  # Constantly updates the movement of the images on the screen

