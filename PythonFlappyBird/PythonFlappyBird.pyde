
"""
Name: Python Flappy Bird
Last Updated: 6 September 2023
Description: This is a Python Flappy Bird game that has almost all of the features that the original Flappy Bird game did have. Some of the more complicated aspects of this program is its collision detection system, animation use, object-oriented class use, and call to online images for the graphics
Important Notes: The code below does make calls to online images for the graphics, and wifi is needed in order for the program to run
Personal Best Score: 85
"""

from random import randrange

def setup():
    global player_y_cor, GAME_GRAVITY, game_velocity, building_1, building_2, building_3, building_4, building_5, game_score, game_state, BACKGROUND_IMAGE, PIPE_IMAGE, BIRD_IMAGE, background_image
    
    # Load images for the game graphics from online sources
    PIPE_IMAGE = loadImage("https://cutewallpaper.org/24/flappy-bird-pipe-png/download-hd-flappy-bird-pipes-png-bottle-transparent-png-image--nicepngcom.png")
    BIRD_IMAGE = loadImage("https://www.pngkey.com/png/full/325-3257134_flappy-bird-flappy-bird-sprite-png.png")
    
    # Creates the object that allows for the scrolling background
    background_image = Background("https://www.desktopbackground.org/download/1024x768/2014/07/26/799254_flappy-generator-plus-create-your-own-flappy-bird-game_9600x950_h.png", 2)
    
    # Screen size
    size(700, 700)
    
    # Game parameters for the movement
    game_velocity = 0
    player_y_cor = 200
    GAME_GRAVITY = -.4
    
    # Game score setup
    game_score = 0 
    game_state = True
    
    # Initialize the buildings with random heights
    building_1 = Buildings(800, random(100, 300))
    building_2 = Buildings(975, random(100, 300))
    building_3 = Buildings(1150, random(100, 300))
    building_4 = Buildings(1325, random(100, 300))
    building_5 = Buildings(1500, random(100, 300))   

def draw():
    global game_velocity, player_y_cor, GAME_GRAVITY, building_1, building_2, building_3, building_4, building_5, game_score, game_state, BACKGROUND_IMAGE, PIPE_IMAGE, BIRD_IMAGE, background_image
    
    # This loop runs when the player is active (has not run into a pillar)
    if game_state:
        # Displays and moves the background
        background_image.display()
        background_image.move()
        
        # Boundary for the player (to not go off screen)
        if player_y_cor < 0:
            player_y_cor = 1
            game_velocity = 0
        if player_y_cor > 655:
            player_y_cor = 654
            game_velocity = 0
            
        # Display the player's bird (have to resize the image to make it smaller)
        scale(0.2)
        image(BIRD_IMAGE, 20*15, (game_velocity + player_y_cor)*5)
        scale(5)
        
        # Draws each building, moves each building, resets the building's coordinates, check if the player has run into the building
        building_1.allBuildingFunctions()
        building_2.allBuildingFunctions()
        building_3.allBuildingFunctions()
        building_4.allBuildingFunctions()
        building_5.allBuildingFunctions()
        
        # Update the player's position and velocity (for the gravity)
        game_velocity = game_velocity - GAME_GRAVITY
        player_y_cor = player_y_cor + game_velocity
    
    # Display's the game's score
    if game_state:
        textSize(20)
        fill(0, 0, 0)
        text("Game Score: " + str(game_score), 540, 33)
        fill(255, 255, 255)

    # Display's the game-over screen
    else:
        textSize(40)
        fill(255, 255, 255)
        text("Game Over!", 275, 340)
        textSize(24)
        fill(255, 255, 255)
        text("Game Score: " + str(game_score), 305, 380)
        textSize(14)
        fill(255, 255, 255)
        text("Press the space bar to continue", 290, 440)
        text("(it might take a couple of seconds to restart)", 252, 460)
    
# Checks if the player has typed on the keyboard
def keyPressed():
    global game_velocity, game_state
    
    # Reset's the player's velocity
    game_velocity = -8
    
    # If the game is over, and the player wants to restart, the player is able to do so
    if not game_state:
        setup()

# Buildings class represents the buildings that the player have to avoid
class Buildings():
    global building_width, PIPE_IMAGE
    
    # Width of each building
    building_width = 50
    
    def __init__(self, building_x_cor, building_y_cor):
        # Initializing x and y coordinates for each building object (used for the start of the game to load the buildings at the correct places)
        self.building_x_cor = building_x_cor
        self.building_y_cor = building_y_cor
    
    # Groups the functions that are always called together
    def allBuildingFunctions(self):
        self.drawBuilding()
        self.moveLeft()
        self.resetX()
        self.gameContinue()
        
    # Draw the buildings onto the screen
    def drawBuilding(self):
        global building_width, PIPE_IMAGE
        
        # Building on the bottom
        image(PIPE_IMAGE, self.building_x_cor, 740-self.building_y_cor, 55, 500)
        
        # Building on the top (have to rotate the entire screen)
        rotate(HALF_PI)
        rotate(HALF_PI)
        image(PIPE_IMAGE, -self.building_x_cor-55, -440+self.building_y_cor, 55, 500)
        rotate(HALF_PI)
        rotate(HALF_PI)
     
        
    # Move the buildings to the left each iteration
    def moveLeft(self):
        self.building_x_cor -= 5   
    
    # Resets the x position of the building when it goes out of the screen. Also increases game score.
    def resetX(self):
        global game_score
        
        # Buildings are out-of-bounds
        if self.building_x_cor < -100:
            self.building_x_cor = 800
      # Randomizes the y-cordinate after reset
            self.building_y_cor = random(100, 400)
            
            # Game score increase
            game_score += 1
    
    # Checks for colision with the building and the player
    def gameContinue(self):
        global game_state
        
        circle_radius = 6
        # If the player is within the x-cordinate of the building
        if self.building_x_cor <= 100 + circle_radius and self.building_x_cor + building_width >= 100 - circle_radius:
            # If thep layer is within the y-cordinate of the building
            if player_y_cor + circle_radius >= 700-self.building_y_cor or player_y_cor - circle_radius <= 440-self.building_y_cor:
                # If so, the game ends
                game_state = False

# This class handles the scrolling background of the game. The background consists of two images of the same scene side by side. As one moves out of the view on the left, the other takes its place, creating a looped effect
# NOTE: A lot of this code took inspiration from this YouTube video: "https://www.youtube.com/watch?v=ARt6DLP38-Y", but I changed some things so that the functions are in a class
class Background:
    def __init__(self, img_url, speed):
        self.image = loadImage(img_url)
        self.speed = speed
        
        # Initial x-cordinate of the image
        self.first_background_x_cordinate = 0
        # X-cordinate for the second image
        self.second_background_x_cordinate = self.image.width

   # Display both images side by side
    def display(self):
        image(self.image, self.first_background_x_cordinate, 0)
        image(self.image, self.second_background_x_cordinate, 0)

    # Move both images to the left at the specified speed
    def move(self):
        self.first_background_x_cordinate -= self.speed
        self.second_background_x_cordinate -= self.speed

        # If the first image has entirely moved to the left, it is positioned on the right
        if self.first_background_x_cordinate <= -self.image.width:
            self.first_background_x_cordinate = self.image.width
        # If the second image has entirely moved to the left, it is positioned on the right
        if self.second_background_x_cordinate <= -self.image.width:
            self.second_background_x_cordinate = self.image.width
