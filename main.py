### Tidy and Review all code at the end. Make sure everything is of industry practice (ogranisation, varaible delecration (how and where), etc)
####

# REMOVE TEST "PRINTS", AND ANY OTHER TESTING FLAGS

###
import pygame
from pygame.locals import *

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 900


class Pieces:
    
    def __init__(self, parent_surface, all_coords, lg_coords, dg_coords):
        
        self.parent_surface = parent_surface
        self.piece_selection = 100    # Piece selection tracker

        #Chess board coords
        self.all_coords = all_coords
        self.lg_coords = lg_coords
        self.dg_coords = dg_coords
        
        self.prev_cc = 0 # Previous Clicked Coords
        
        self.white_pieces = ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook",
                        "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
        
        self.white_coords = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                             (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
        

        self.black_pieces = ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook",
                        "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]

        self.black_coords = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                             (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
        
        self.valid_moves = []
        self.eliminated_w = []
        self.eliminated_b = []

        # Index for "previous" black or white selected piece coords
        self.previous_index_b = 0
        self.previous_index_w = 0

        # Load chess piece images
        self.pawn_b = pygame.image.load("resources/pieces/pawn_b.png")
        self.pawn_w = pygame.image.load("resources/pieces/pawn_w.png")
        self.king_b = pygame.image.load("resources/pieces/king_b.png")
        self.king_w = pygame.image.load("resources/pieces/king_w.png")
        self.queen_b = pygame.image.load("resources/pieces/queen_b.png")
        self.queen_w = pygame.image.load("resources/pieces/queen_w.png")
        self.knight_b = pygame.image.load("resources/pieces/knight_b.png")
        self.knight_w = pygame.image.load("resources/pieces/knight_w.png")
        self.bishop_b = pygame.image.load("resources/pieces/bishop_b.png")
        self.bishop_w = pygame.image.load("resources/pieces/bishop_w.png")
        self.rook_b = pygame.image.load("resources/pieces/rook_b.png")
        self.rook_w = pygame.image.load("resources/pieces/rook_w.png")

        # Scaling chess piece images: Big
        self.pawn_b = pygame.transform.scale(self.pawn_b, (80,80))
        self.pawn_w = pygame.transform.scale(self.pawn_w, (80,80))
        self.king_b = pygame.transform.scale(self.king_b, (80,80))
        self.king_w = pygame.transform.scale(self.king_w, (80,80))
        self.queen_b = pygame.transform.scale(self.queen_b, (80,80))
        self.queen_w = pygame.transform.scale(self.queen_w, (80,80))
        self.knight_b = pygame.transform.scale(self.knight_b, (80,80))
        self.knight_w = pygame.transform.scale(self.knight_w, (80,80))
        self.bishop_b = pygame.transform.scale(self.bishop_b, (80,80))
        self.bishop_w = pygame.transform.scale(self.bishop_w, (80,80))
        self.rook_b = pygame.transform.scale(self.rook_b, (80,80))
        self.rook_w = pygame.transform.scale(self.rook_w, (80,80))

        # Scaling chess piece images: Small
        self.pawn_b_small = pygame.transform.scale(self.pawn_b, (45,45))
        self.pawn_w_small = pygame.transform.scale(self.pawn_w, (45,45))
        self.king_b_small = pygame.transform.scale(self.king_b, (45,45))
        self.king_w_small = pygame.transform.scale(self.king_w, (45,45))
        self.queen_b_small = pygame.transform.scale(self.queen_b, (45,45))
        self.queen_w_small = pygame.transform.scale(self.queen_w, (45,45))
        self.knight_b_small = pygame.transform.scale(self.knight_b, (45,45))
        self.knight_w_small = pygame.transform.scale(self.knight_w, (45,45))
        self.bishop_b_small = pygame.transform.scale(self.bishop_b, (45,45))
        self.bishop_w_small = pygame.transform.scale(self.bishop_w, (45,45))
        self.rook_b_small = pygame.transform.scale(self.rook_b, (45,45))
        self.rook_w_small = pygame.transform.scale(self.rook_w, (45,45))
        
        self.black_images = [self.pawn_b, self.king_b, self.queen_b, self.knight_b, self.bishop_b, self.rook_b]
        self.small_black_images = [self.pawn_b_small, self.king_b_small, self.queen_b_small, self.knight_b_small, self.bishop_b_small, self.rook_b_small]

        self.white_images = [self.pawn_w, self.king_w, self.queen_w, self.knight_w, self.bishop_w, self.rook_w]
        self.small_white_images = [self.pawn_w_small, self.king_w_small, self.queen_w_small, self.knight_w_small, self.bishop_w_small, self.rook_w_small]

        self.piece_list = ["pawn", "king", "queen", "knight", "bishop", "rook"]
    
    def draw_all(self):
        
        # Drawing all black pieces to the board (with a slight offset value (+10)
        for i in range(len(self.black_pieces)):
            index = self.piece_list.index(self.black_pieces[i])
            self.parent_surface.blit(self.black_images[index], (self.black_coords[i][0] * 100 + 10, self.black_coords[i][1] * 100 + 10))

        # Drawing all white pieces to the board (with a slight offset value (+10)
        for i in range(len(self.white_pieces)):
            index = self.piece_list.index(self.white_pieces[i])
            self.parent_surface.blit(self.white_images[index], (self.white_coords[i][0] * 100 + 10, self.white_coords[i][1] * 100 + 10))

    
    # Highlighting pieces based on game state
    def highlight_pieces(self): # Working on Highlighting for selected pieces, based on turn cycle.
        
        match self.turn_cycle:
            case 0: # White turn, no selection
                Game.outline_tiles(self.parent_surface)
                for i in range(len(self.white_coords)):
                   pygame.draw.rect(self.parent_surface, "yellow", [self.white_coords[i][0] * 100,self.white_coords[i][1] * 100, 100, 100], 1,)


            case 1: # White turn, piece selected
                Game.outline_tiles(self.parent_surface)
                for i in range(len(self.white_pieces)):
                    if self.piece_selection == i:
                        pygame.draw.rect(self.parent_surface, "red", [self.white_coords[i][0] * 100,self.white_coords[i][1] * 100, 100, 100], 1,)
                # Highlights valid moves
                for i in range(len(self.valid_moves)):
                    pygame.draw.rect(self.parent_surface, "green", [self.valid_moves[i][0] * 100,self.valid_moves[i][1] * 100, 100, 100], 1,)


            case 2: # Black turn, no selection
                Game.outline_tiles(self.parent_surface)
                for i in range(len(self.black_coords)):
                   pygame.draw.rect(self.parent_surface, "yellow", [self.black_coords[i][0] * 100,self.black_coords[i][1] * 100, 100, 100], 1,)


            case 3: # Black turn, piece selected
                Game.outline_tiles(self.parent_surface)
                for i in range(len(self.black_pieces)):
                    if self.piece_selection == i:
                        pygame.draw.rect(self.parent_surface, "red", [self.black_coords[i][0] * 100,self.black_coords[i][1] * 100, 100, 100], 1,)
                # Highlights valid moves
                for i in range(len(self.valid_moves)):
                    pygame.draw.rect(self.parent_surface, "green", [self.valid_moves[i][0] * 100,self.valid_moves[i][1] * 100, 100, 100], 1,)
                        
            case _:
                pass
    
    def check_clicked(self, turn_cycle, clicked_coords):
        self.turn_cycle = turn_cycle            # Turn cycle of the game
        self.clicked_coords = clicked_coords # Clicked coords of the mouse

        if self.clicked_coords in self.all_coords: # Prevents players from moving a piece out of bounds
        # White turn, no selection
            if self.turn_cycle == 0:
                self.highlight_pieces()
            
                for i in range(len(self.white_coords)):
                    if self.clicked_coords == self.white_coords[i]:
                        self.piece_selection = i
                        Game.turn_cycler()
                        print("Total White Turns: ", Game.player_1_turns)

                    
            elif self.turn_cycle == 1:
                self.previous_index_w = self.piece_selection # Previous white piece selected index
                self.prev_white_coords = self.white_coords[self.previous_index_w] # Previous white piece coords
                self.move_piece()

        # Black turn, no selection
            if self.turn_cycle == 2:
                self.highlight_pieces()
                for i in range(len(self.black_coords)):
                    if self.clicked_coords == self.black_coords[i]:
                        self.piece_selection = i
                        Game.turn_cycler()
                        print("Total Black Turns: ", Game.player_2_turns)

            elif self.turn_cycle == 3:
                self.previous_index_b = self.piece_selection # Previous black piece selected index
                self.prev_black_coords = self.black_coords[self.previous_index_b] # Previous white piece coords
                self.move_piece()


            self.prev_cc = self.clicked_coords # Stores previously clicked_coords

    def move_piece(self):

        if self.turn_cycle == 1:  # White's turn to move
            piece_type = self.piece_list.index(self.white_pieces[self.piece_selection])
            valid = self.is_valid(piece_type)
            self.highlight_pieces()

            if self.clicked_coords not in self.white_coords and valid:
                self.eliminated_piece()
                self.white_coords[self.piece_selection] = self.clicked_coords
                self.parent_surface.blit(self.white_images[piece_type], (self.clicked_coords[0] * 100 + 10, self.clicked_coords[1] * 100 + 10))
                self.delete_piece(1, self.prev_white_coords) # delete piece upon moving
                Game.turn_cycler()

            elif self.clicked_coords != self.prev_white_coords and self.clicked_coords in self.white_coords: # Allows player to change piece selected
                Game.master_turn_cycle = 0

        elif self.turn_cycle == 3:  # Black's turn to move
            piece_type = self.piece_list.index(self.black_pieces[self.piece_selection])
            valid = self.is_valid(piece_type)
            self.highlight_pieces()

            if self.clicked_coords not in self.black_coords and valid:
                self.eliminated_piece()
                self.black_coords[self.piece_selection] = self.clicked_coords
                self.parent_surface.blit(self.black_images[piece_type], (self.clicked_coords[0] * 100 + 10, self.clicked_coords[1] * 100 + 10))
                self.delete_piece(1, self.prev_black_coords)
                Game.turn_cycler()

            elif self.clicked_coords != self.prev_black_coords and self.clicked_coords in self.black_coords: # Allows player to change piece selected
                Game.master_turn_cycle = 2

    #Movement System Blueprint #1
    def is_valid(self, piece_type = 0):
        flag = False

        if self.piece_list[piece_type] == "pawn":
            flag = self.check_pawn()
            

        elif self.piece_list[piece_type] == "king":
            flag = self.check_king()

        elif self.piece_list[piece_type] == "queen":
            flag = self.check_queen()

        elif self.piece_list[piece_type] == "knight":
            flag = self.check_knight()

        elif self.piece_list[piece_type] == "bishop":
            flag = self.check_bishop()

        else:
            flag = self.check_rook()
        return flag

    #Movement System Blueprint #2
    def check_pawn(self):
        
        print("Pawn Coords: ", self.white_coords[self.piece_selection])
        print("Valid Moves :", self.valid_moves)
        match self.turn_cycle:

            # White Turn to move
            case 1:

                if Game.player_1_turns == 1:
                    self.valid_moves = [((self.white_coords[self.piece_selection][0]), (self.white_coords[self.piece_selection][1] + 1)),
                                        ((self.white_coords[self.piece_selection][0]), (self.white_coords[self.piece_selection][1] + 2))]
                else:
                    self.valid_moves = [((self.white_coords[self.piece_selection][0] + 1), (self.white_coords[self.piece_selection][1] + 1)),
                                        ((self.white_coords[self.piece_selection][0] - 1), (self.white_coords[self.piece_selection][1] + 1))]
                if self.clicked_coords in self.valid_moves:
                    return True
                else:
                    return False

            # Black Turn to move
            case 3:

                if Game.player_2_turns == 1:
                    self.valid_moves = [((self.black_coords[self.piece_selection][0]), (self.black_coords[self.piece_selection][1] - 1)),
                                        ((self.black_coords[self.piece_selection][0]), (self.black_coords[self.piece_selection][1] - 2))]
                else:
                    self.valid_moves = [((self.black_coords[self.piece_selection][0] + 1), (self.black_coords[self.piece_selection][1] - 1)),
                    ((self.black_coords[self.piece_selection][0] - 1), (self.black_coords[self.piece_selection][1] - 1))]

                if self.clicked_coords in self.valid_moves:
                    return True
                else:
                    return False



    def eliminated_piece(self):
        if self.turn_cycle == 1 and self.clicked_coords in self.black_coords:
            eliminated_index = self.black_coords.index(self.clicked_coords)
            eliminated_piece = self.black_pieces.pop(eliminated_index) # Removes the eliminated black piece from the piece list
            self.black_coords.pop(eliminated_index) # Removes the specific eliminated black piece coord based on its index from black_coords list
            self.eliminated_b.append(eliminated_piece) # Adds eliminated piece to list
            print("White captures:", eliminated_piece)
            self.delete_piece(2)

        elif self.turn_cycle == 3 and self.clicked_coords in self.white_coords:
            eliminated_index = self.white_coords.index(self.clicked_coords)
            eliminated_piece = self.white_pieces.pop(eliminated_index)
            self.white_coords.pop(eliminated_index)
            self.eliminated_w.append(eliminated_piece)
            print("Black captures:", eliminated_piece)
            self.delete_piece(2)
        #print("Elminated White Pieces: ", self.eliminated_w,)
        #print("Elminated Black Pieces: ", self.eliminated_b,)
        
        self.draw_elim(self.eliminated_w, self.eliminated_b)

    def delete_piece(self, mode = 0, previous_coords = (0,0)):
        # Deletes piece by bliting the chess board square with its correspoding color
        # Mode 1: Deletion of piece upon moving
        # Mode 2: Deletion of piece upon collision
        match mode:
            case 1:
                if previous_coords != self.clicked_coords:
                    if previous_coords in self.lg_coords:
                        pygame.draw.rect(self.parent_surface, "light grey", [previous_coords[0] * 100,previous_coords[1] * 100, 100, 100], 50,)
                        print("Deleted")
                    else:
                        pygame.draw.rect(self.parent_surface, "dark grey", [previous_coords[0] * 100,previous_coords[1] * 100, 100, 100], 50,)
                        
            case 2:
                if self.clicked_coords in self.lg_coords:
                    pygame.draw.rect(self.parent_surface, "light grey", [self.clicked_coords[0] * 100,self.clicked_coords[1] * 100, 100, 100], 50,)
                else:
                    pygame.draw.rect(self.parent_surface, "dark grey", [self.clicked_coords[0] * 100,self.clicked_coords[1] * 100, 100, 100], 50,)

    # Draws eliminated piece on the side screen, takes eliminated piece list of each colour
    def draw_elim(self, eliminated_white, eliminated_black):
        
        elim_pos_y = list(range(10,730,45)) # Creates a list for the y-axis position of eliminated pieces (10 - y-axis offset, 730 - max eliminated piece pos, 45 - scale of small images)

        if eliminated_white or eliminated_black:
            
            for i in range(0,len(eliminated_white)):
                index_w = self.piece_list.index(eliminated_white[i])
                #print("Index of white piece: ", index_w)
                self.parent_surface.blit(self.small_white_images[index_w], (800, elim_pos_y[i]))

            for i in range(0,len(eliminated_black)):
                index_b = self.piece_list.index(eliminated_black[i])
                #print("Index of black piece: ", index_b)
                self.parent_surface.blit(self.small_black_images[index_b], (900, elim_pos_y[i]))
    

class Game:
    # Game state tracking - Global Variable
    # Turn Tracker: 0 = White Turn, No Selection, 1 = White turn, Piece Selected, 2 = Black Turn, No selection, 3 = Black Turn, Piece Selected
    master_turn_cycle = 0 # change to getter and setter mechanism
    player_1_turns = 1 # Number of player 1 turns
    player_2_turns = 0 # Number of player 2 turns

    def __init__(self):
        self.game_running = True
        pygame.init()
        pygame.mixer.init() # Sound

        #Init Images, Fonts, etc.
        pygame.display.set_caption("Said's Chess Game")
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Creates a display[w x h]
        self.start_image = pygame.image.load("resources/start_screen.jpg") # loads start screen image
        self.font_big = pygame.font.SysFont("Gabriola", 130)  # Initialises big start screen font
        self.font_small = pygame.font.SysFont("Gabriola", 50)  # Initialises small start screen font

        # Init text to be displayed
        self.title = self.font_big.render("Classical Chess", True, (255, 255, 255))
        self.credits = self.font_small.render("Said Ali", True, (255, 255, 255))
        self.play_text = self.font_big.render("Press SPACE to Play!", True, (255, 255, 255))

        # Game clock and timer
        self.timer = pygame.time.Clock()
        self.fps = 60
        
        # Chess Board Coords
        self.all_coords = [] # all chess board coords
        self.lg_squares = [] # light grey square coords.
        self.dg_squares = [] # dark grey square coords.
        
        # Mouse x and y coords
        self.x = 0
        self.y = 0
        self.clicked_coords = [(0,1)] # init clicked coords - starts at player one's first pawn
        self.pieces = Pieces(self.surface, self.all_coords, self.lg_squares, self.dg_squares)
        self.start_screen()
        
    def start_screen(self):
    # Draw images and texts
        self.surface.blit(self.start_image, (0, 0))
        self.surface.blit(self.title, (200, 25))
        self.surface.blit(self.credits, (850, 850))
        self.surface.blit(self.play_text, (100, 600))
        pygame.display.flip()


        while (self.game_running):  # Start Screen Loop

            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.exit()

                    elif event.key == K_SPACE:
                        self.game_run()

                elif event.type == QUIT:
                    self.exit()

    def chess_coords(self):
        
        for i in range(8):
            for j in range(8):
                self.all_coords.append((i,j))
        # Converts all_coords and lg_coords to sets, takes differences, and converts back to a list
        set_lg = set(self.lg_squares)
        set_all_coords = set(self.all_coords)
        self.dg_squares = list(set_all_coords.difference(set_lg))

    def draw_chess_board(self):
        self.surface.fill("dark gray")
        
        # Drawing square pattern for board. *Go over******
        for i in range(32):
            column = i % 4
            row = i // 4
            if row % 2 == 0:
                pygame.draw.rect(self.surface, "light gray", [600 - (column * 200), row * 100, 100, 100])
                self.lg_squares.append(( (600 - (column * 200)) // 100, (row * 100) // 100)) # Stores and formats light grey squares coords
            else:
                pygame.draw.rect(self.surface, "light gray", [700 - (column * 200), row * 100, 100, 100])
                self.lg_squares.append(( (700 - (column * 200)) // 100, (row * 100) // 100)) # Stores and formats light grey squares coords
            
            

        pygame.draw.rect(self.surface, "black", [800,0,200,800], 3) # Creates boarder for right-side section - Eliminated pieces
        #pygame.draw.rect(self.surface, "black", [0,800,SCREEN_WIDTH,100], 3) # Creates boarder for bottom-side section - Game commands/instructions
        # ^ removed because I am clearing this section in game_prompts() case 0:

        Game.outline_tiles(self.surface) # creates chess board box outlines
        
        #pygame.display.flip()

    @classmethod # I have changed this to a class method in order to be able to use it in Pieces.Highlight_pieces() because the hightlights need to be erased every turn cycle as it changes. And a way to do that is to redraw the chess BOARD outlines
    def outline_tiles(cls, surface):
        # Outlining chess titles
        for i in range(0,900,100):
            pygame.draw.line(surface,[0,0,0], (i,0), (i,800), 3) # Columns
            pygame.draw.line(surface,[0,0,0], (0,i), (800,i), 3) # Row

    def game_prompts(self, prompt):
        self.prompt = prompt

        self.action_text = ["White: Select a Piece!", "White: Select a Position!", "Black: Select a Piece", "Black: Select a Position"]
        self.game_status = ["Checkmate!", "Draw!"]

        match self.prompt:
            case 0: # Turn Cycle used as action_text index
                pygame.draw.rect(self.surface, [245, 255, 250], [0,800,SCREEN_WIDTH,100], 50) # Erases text in game command section by filling section
                self.surface.blit(self.font_small.render(self.action_text[self.master_turn_cycle], True, (0, 0, 0)), (10, 820))

            case 1: # Game Status

                # For game status texts
                pass
            case _:
                pass

# Cycles the turn of the game once a piece is clicked
    @classmethod
    def turn_cycler(cls):
        cls.master_turn_cycle += 1
        if cls.master_turn_cycle > 3:
            cls.master_turn_cycle = 0

        # Tracks total amount of turns had by players
        if cls.master_turn_cycle == 0:
            cls.player_1_turns += 1
        elif cls.master_turn_cycle == 2:
            cls.player_2_turns += 1

    def play_chess(self):

       self.pieces.check_clicked(Game.master_turn_cycle, self.clicked_coords[0]) # Checks if a piece is clicked
       self.game_prompts(0) # Selecting game instruction prompts * Arg has to be returned from "move piece" method, to know if the game is over/checkmate
       pygame.display.flip()


    def timer(self):
        # chess game timer. switch turns (using turn cycle) after a set amount of time *CHECK HOW TIMING WORKS IN CHESS*
        ...

    # Runs game.
    def game_run(self):
        self.chess_coords()
        self.draw_chess_board()
        self.pieces.draw_all()
        pygame.display.flip()
        while (self.game_running):  # Infinite game loop
            
            # Game event handling
            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.x = event.pos[0] // 100 # // (floor) 100 formats mouse pos integers to match piece coord values
                    self.y = event.pos[1] // 100
                    self.clicked_coords = [(self.x,self.y)]

                elif event.type == QUIT:
                    self.exit()

            self.play_chess()

            self.timer.tick(self.fps) # Set game to 60 FPS

    def exit(self):
        self.game_running = False


if __name__ == "__main__":
    game = Game()
    