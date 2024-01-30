# When in doubt, create CODE TEST POINTS and DEBUG!

import random
import time
import os, sys

import pygame  
from pygame.locals import * 

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
JUMP = 80 # x-y value for a piece to move the the centre of a square


class Buttons:
    
    def __init__(self, parent_surface, pos, style = 1, text = "", text_pos = (0,0), rgb = (0,0,0)):
        
        # Button attributes
        self.text = text
        self.pos = pos
        self.text_pos = text_pos
        self.rgb = rgb
        self.style = style
        self.parent_surface = parent_surface

        # Image and Font init
        self.big_button = pygame.image.load("resources/main_button.png").convert_alpha()
        self.font = pygame.font.SysFont("Gabriola", 40)  # Initialises start screen font
        self.button_text = self.font.render(self.text, True, (self.rgb[0],self.rgb[1],self.rgb[2])) # Text init
        

        # Class Methods to be called
        self.check_style()


    # Checks style of the button selected, Big or Small button. Default is Big button.
    def check_style(self):

        if self.style == 1:
            self.main_button()

        elif self.style == 2:
            self.small_button()


    # Main and biggest button
    def main_button(self):
         
         self.parent_surface.blit(self.big_button,(self.pos[0],self.pos[1]))                        # Prints button
         self.parent_surface.blit(self.button_text,(self.text_pos[0],self.text_pos[1]))              # Prints text
         
         pygame.display.flip()

    # Checks if a button has been clicked. Returns a unique ID for each button clicked.
    @classmethod
    def check_clicked(cls, x, y):

        cls.button_ID = 0 # Unique ID for each button. 0 == Reset
        cls.x = x
        cls.y = y
        
        # *Amened to be dynamic with the button length and width using image resolution of the button.

        if (cls.x in range(260, 450)) and (cls.y in range(200, 250)): # Clicked First Button
            cls.button_ID = 1

        if (cls.x in range(260, 450)) and (cls.y in range(300, 350)): # Clicked Second Button
            cls.button_ID = 2


        if (cls.x in range(260, 450)) and (cls.y in range(400, 450)): # Clicked Exit Button
            cls.button_ID = 3
        
        return cls.button_ID
                

    # Small button
    def small_button(self):
         pass
         #button = pygame.image.load("resources/options_button.png").convert_alpha
         
         #pygame.Surface.blit(button,(self.pos[0],self.pos[1]))

        # pygame.display.flip()


class Pieces:
    pass


class Game:
    def __init__(self):
        self.game_running = True
        pygame.init()
        pygame.mixer.init()
        self.mouse_pos = [0,0] # Mouse position game attribute
        self.button_ID = 0 # Game Button ID's

        #Loads Images, Fonts, and Texts
        pygame.display.set_caption("Said Ali's Chess Game")
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Creates a display[w x h]
        self.menu_image = pygame.image.load("resources/menu.jpg") # loads menu image
        self.chess_board = pygame.image.load("resources/chess_board.png") # loads chess board image
        self.font_big = pygame.font.SysFont("Gabriola", 100)  # Initialises start screen font
        self.font_small = pygame.font.SysFont("Gabriola", 20)  # Initialises start screen font
        self.menu_text = self.font_big.render("Chess", True, (255, 255, 255))
        self.loading_text = self.font_big.render("Loading...", True, (255, 255, 255))
        self.menu_name = self.font_small.render("Said Ali", True, (255, 255, 255))

        # Main Menu Buttons
        self.play_button = Buttons(self.surface,(250,200), 1, "Play", (320,205), (255,255,255)) # creates "play" button 
        self.options_button = Buttons(self.surface,(250,300), 1, "Options", (300,305), (255,255,255)) # creates "options" button 
        self.exit_button = Buttons(self.surface,(250,400), 1, "Exit", (320,405), (255,255,255)) # creates "exit" button 

        # Game Mode Buttons
        self.single_player_button = Buttons(self.surface,(250,200), 1, "Single Player", (275,205), (255,255,255)) # creates "single" button 
        self.two_player_button = Buttons(self.surface,(250,300), 1, "Two Player", (285,305), (255,255,255)) # creates "two player" button
 

        # Methods
        self.main_menu() # Starts game
        

    def menu_assets(self, button_set):

        self.button_set = button_set

        # Images and Text
        self.surface.blit(self.menu_image, (0, 0))
        self.surface.blit(self.menu_text, (50, 50))
        self.surface.blit(self.menu_name, (700, 560))

        # Button Sets

        if self.button_set == 1:

            self.play_button.main_button() 
            self.options_button.main_button() 
            self.exit_button.main_button() 

        elif self.button_set == 2:

            self.single_player_button.main_button()
            self.two_player_button.main_button()


    def main_menu(self):

        self.menu_assets(1)
        pygame.display.flip()
  
        while (self.game_running):  # infinite game loop
            
            # Checks if Escape key or QUIT is pressed

            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.exit()
                        break
                
                elif event.type == MOUSEBUTTONDOWN:            # Checks mouse position when in the main menu
                    self.mouse_pos = pygame.mouse.get_pos()

                elif event.type == QUIT:
                    self.exit()
                    break

            # Checks if a button has been clicked, returns unique button ID.  
            self.button_ID = Buttons.check_clicked(self.mouse_pos[0],self.mouse_pos[1])

            match self.button_ID:
                case 1:
                    self.game_mode()
                    break
                case 2:
                    self.options()
                    break
                case 3:
                    self.exit()
                    break
                case other:
                    pass
                
    
    def game_mode(self):
         self.button_ID = 0 # Resets button ID
         self.mouse_pos = [0,0] # Resets Mouse Position********* Kept using previous mouse position from main menu and applying it to game mode menu thus setting the button id
         self.menu_assets(2)

         while (self.game_running):  # infinite game loop
            
            # Checks if Escape key or QUIT is pressed

            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.exit()
                        break
                
                elif event.type == MOUSEBUTTONDOWN:            # Checks mouse position when in the main menu
                    self.mouse_pos = pygame.mouse.get_pos()
                  
                elif event.type == QUIT:
                    self.exit()
                    break
        
        
            # Checks if a button has been clicked, returns unique button ID.  
            self.button_ID = Buttons.check_clicked(self.mouse_pos[0],self.mouse_pos[1])

            if self.button_ID == 1:
                self.single_player()
                break

            elif self.button_ID == 2:
                self.two_player
                break



    # Game loading screen.
    def loading(self):

        pygame.Surface.fill(self.surface,(152,152,156)) # Fills the screen black
        
        # Loading text
        self.loading_text = self.font_big.render("Loading", True, (255, 255, 255))  
        self.surface.blit(self.loading_text, (250, 250))

        # Loading dot
        self.dot = self.font_big.render(".", True, (255, 255, 255))

        # Printing moving loading dots
        for i in range(500,530,10):

            self.surface.blit(self.dot, (i, 250))
            pygame.display.flip()
            time.sleep(0.5)

        # Draws chess board
        self.surface.blit(self.chess_board, (0, 0))
        pygame.display.flip()


    def single_player(self):

        self.loading()
        
        self.pieces = Pieces() # Creates chess pieces

        while self.game_running:
            
            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.exit()
                        break
                
                elif event.type == MOUSEBUTTONDOWN:            # Checks mouse position when in the main menu
                    self.mouse_pos = pygame.mouse.get_pos()
                  
                elif event.type == QUIT:
                    self.exit()
                    break
            
            self.sp_logic(self.mouse_pos[0],self.mouse_pos[1]) # calls single player logic


    # single player logic
    def sp_logic(self, m_x, m_y):

        self.sp_mouse_x = m_x # mouse x pos
        self.sp_mouse_y = m_y # mouse y pos
        pass




    def two_player(self):
        pass


    def options(self):

        print("Options")


    def exit(self):
        self.game_running = False        





if __name__ == "__main__":
    game = Game()
    