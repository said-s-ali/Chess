# Chess Game using Pygame - Said Ali
import pygame
from pygame.locals import *

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

class Pieces:

    def __init__(self, parent_surface, all_coords, lg_coords, dg_coords, right_perim_coords):
        
        self.parent_surface = parent_surface

        # Chess Pieces
        self.white_pieces = ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook",
                        "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
        
        self.black_pieces = ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook",
                        "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
        
        self.piece_selection = 100    # Piece Selection Tracker

        # Piece Coords
        self.white_coords = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                            (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

        self.black_coords = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                            (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
        
        # Chess board coords
        self.all_coords = all_coords
        self.lg_coords = lg_coords
        self.dg_coords = dg_coords
        self.right_perim_coords = right_perim_coords

        # Promotion Coords
        self.promo_white = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)]
        self.promo_black = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]

        self.valid_moves = []
        self.eliminated_w = []
        self.eliminated_b = []

        self.previous_tc = None     # Previous Turn cycle
        self.prev_cc = 0            # Previous Clicked Coords

        # Index for previous black or white selected piece coords
        self.previous_index_b = 0
        self.previous_index_w = 0

        self.check_mate_flag = 0
        self.winner = ""

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

        # Scaling chess piece images
        self.pawn_b = pygame.transform.scale(self.pawn_b, (48,48))
        self.pawn_w = pygame.transform.scale(self.pawn_w, (48,48))
        self.king_b = pygame.transform.scale(self.king_b, (48,48))
        self.king_w = pygame.transform.scale(self.king_w, (48,48))
        self.queen_b = pygame.transform.scale(self.queen_b, (48,48))
        self.queen_w = pygame.transform.scale(self.queen_w, (48,48))
        self.knight_b = pygame.transform.scale(self.knight_b, (48,48))
        self.knight_w = pygame.transform.scale(self.knight_w, (48,48))
        self.bishop_b = pygame.transform.scale(self.bishop_b, (48,48))
        self.bishop_w = pygame.transform.scale(self.bishop_w, (48,48))
        self.rook_b = pygame.transform.scale(self.rook_b, (48,48))
        self.rook_w = pygame.transform.scale(self.rook_w, (48,48))

        self.black_images = [self.pawn_b, self.king_b, self.queen_b, self.knight_b, self.bishop_b, self.rook_b]
        self.white_images = [self.pawn_w, self.king_w, self.queen_w, self.knight_w, self.bishop_w, self.rook_w]

        self.piece_list = ["pawn", "king", "queen", "knight", "bishop", "rook"]

        # Sound effects
        self.move_sound = pygame.mixer.Sound("resources/move.mp3")
        self.capture_sound = pygame.mixer.Sound("resources/capture.mp3")
        self.win_sound = pygame.mixer.Sound("resources/winner.mp3")

    def sound_effect(self, effect):
        match effect:
            case 0:
                pygame.mixer.Sound.play(self.move_sound, 0)
            case 1:
                pygame.mixer.Sound.play(self.capture_sound, 0)
            case 2:
                pygame.mixer.Sound.play(self.win_sound, 0)
                pass

    def draw_all(self):
        
        # Drawing all black pieces to the board (with a slight offset value (+5)
        for i in range(len(self.black_pieces)):
            index = self.piece_list.index(self.black_pieces[i])
            self.parent_surface.blit(self.black_images[index], (self.black_coords[i][0] * 60 + 5, self.black_coords[i][1] * 60 + 5))

        # Drawing all white pieces to the board (with a slight offset value (+5)
        for i in range(len(self.white_pieces)):
            index = self.piece_list.index(self.white_pieces[i])
            self.parent_surface.blit(self.white_images[index], (self.white_coords[i][0] * 60 + 5, self.white_coords[i][1] * 60 + 5))

    def highlight_pieces(self):
        # Highlighting pieces based on game turn cycle

        match self.turn_cycle:
            case 0: # White turn, no selection
                Game.outline_tiles(self.parent_surface) # Redraws chess board outline tiles
                for i in range(len(self.white_coords)):
                   pygame.draw.rect(self.parent_surface, "brown", [self.white_coords[i][0] * 60,self.white_coords[i][1] * 60, 60, 60], 1,)

            case 1: # White turn, piece selected
                Game.outline_tiles(self.parent_surface)
                for i in range(len(self.white_pieces)):
                    if self.piece_selection == i:
                        pygame.draw.rect(self.parent_surface, "brown", [self.white_coords[i][0] * 60,self.white_coords[i][1] * 60, 60, 60], 1,)
                # Highlights valid moves
                for i in range(len(self.valid_moves)):
                    pygame.draw.rect(self.parent_surface, "gold", [self.valid_moves[i][0] * 60,self.valid_moves[i][1] * 60, 60, 60], 1,)

            case 2: # Black turn, no selection
                Game.outline_tiles(self.parent_surface)
                for i in range(len(self.black_coords)):
                   pygame.draw.rect(self.parent_surface, "brown", [self.black_coords[i][0] * 60,self.black_coords[i][1] * 60, 60, 60], 1,)

            case 3: # Black turn, piece selected
                Game.outline_tiles(self.parent_surface)
                for i in range(len(self.black_pieces)):
                    if self.piece_selection == i:
                        pygame.draw.rect(self.parent_surface, "brown", [self.black_coords[i][0] * 60,self.black_coords[i][1] * 60, 60, 60], 1,)
                # Highlights valid moves
                for i in range(len(self.valid_moves)):
                    pygame.draw.rect(self.parent_surface, "gold", [self.valid_moves[i][0] * 60,self.valid_moves[i][1] * 60, 60, 60], 1,)
            case _:
                pass

    def check_clicked(self, turn_cycle, clicked_coords):
        pygame.display.flip()
        self.turn_cycle = turn_cycle                 # Turn cycle of the game
        self.clicked_coords = clicked_coords         # Clicked coords of the mouse

        if self.clicked_coords in self.all_coords:    # Prevents players from moving a piece out of bounds
        # White turn, no selection
            if self.turn_cycle == 0:
                self.highlight_pieces()

                for i in range(len(self.white_coords)):
                    if self.clicked_coords == self.white_coords[i]:
                        self.piece_selection = i
                        Game.turn_cycler()

            elif self.turn_cycle == 1:
                self.previous_index_w = self.piece_selection   # Previous white piece selected index - Needed for piece deletion when moving
                self.prev_white_coords = self.white_coords[self.previous_index_w]  # Previous white piece coords - Needed for piece deletion when moving
                self.move_piece()

        # Black turn, no selection
            if self.turn_cycle == 2:
                self.highlight_pieces()
                for i in range(len(self.black_coords)):
                    if self.clicked_coords == self.black_coords[i]:
                        self.piece_selection = i
                        Game.turn_cycler()

            elif self.turn_cycle == 3:
                self.previous_index_b = self.piece_selection
                self.prev_black_coords = self.black_coords[self.previous_index_b]
                self.move_piece()

            self.prev_cc = self.clicked_coords # Stores previously clicked_coords

            # Promotion
            if Game.master_turn_cycle == 4:
                self.promotion()

    def move_piece(self):

        if self.turn_cycle == 1:  # White's turn to move
            piece_type = self.piece_list.index(self.white_pieces[self.piece_selection]) # Finds Piece Type that was selected
            valid = self.is_valid(piece_type)                                           # Checks if new desired move is valid
            self.highlight_pieces()

            if self.clicked_coords not in self.white_coords and valid:
                self.eliminated_piece()                                        # Check if Piece is Eliminated
                self.white_coords[self.piece_selection] = self.clicked_coords  # Change Piece coords to new selected location
                self.parent_surface.blit(self.white_images[piece_type], (self.clicked_coords[0] * 60 + 5, self.clicked_coords[1] * 60 + 5)) # Draws Piece
                self.delete_piece(1, self.prev_white_coords)                   # Delete Piece upon Moving
                if self.check_promo():
                    Game.master_turn_cycle = 4                                 # Promotion state
                else:
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
                self.parent_surface.blit(self.black_images[piece_type], (self.clicked_coords[0] * 60 + 5, self.clicked_coords[1] * 60 + 5))
                self.delete_piece(1, self.prev_black_coords)
                if self.check_promo():
                    Game.master_turn_cycle = 4

                else:
                    Game.turn_cycler()

            elif self.clicked_coords != self.prev_black_coords and self.clicked_coords in self.black_coords: # Allows player to change piece selected
                Game.master_turn_cycle = 2

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

    def check_pawn(self):
        self.valid_moves = [] # Resets valid_moves for new calculation

        match self.turn_cycle:

            # White Turn to Move
            case 1:
                if Game.player_1_turns == 1: # Pawn move set at the start of the game
                    self.valid_moves = [((self.white_coords[self.piece_selection][0]), (self.white_coords[self.piece_selection][1] + 1)),
                                        ((self.white_coords[self.piece_selection][0]), (self.white_coords[self.piece_selection][1] + 2))]
                else:
                    # Pawn Attack Moves
                    attacks = [((self.white_coords[self.piece_selection][0] + 1), (self.white_coords[self.piece_selection][1] + 1)),
                                ((self.white_coords[self.piece_selection][0] - 1), (self.white_coords[self.piece_selection][1] + 1))]

                    for attack in attacks:
                        if attack in self.black_coords:
                            self.valid_moves.append(attack)

                    # Pawn Regular Moves
                    move = ((self.white_coords[self.piece_selection][0]), (self.white_coords[self.piece_selection][1] + 1))
                    if move not in self.black_coords:
                        self.valid_moves.append(move)

                if self.clicked_coords in self.valid_moves:
                    self.sound_effect(0)
                    return True
                else:
                    return False

            # Black Turn to Move
            case 3:

                if Game.player_2_turns == 1:
                    self.valid_moves = [((self.black_coords[self.piece_selection][0]), (self.black_coords[self.piece_selection][1] - 1)),
                                        ((self.black_coords[self.piece_selection][0]), (self.black_coords[self.piece_selection][1] - 2))]
                else:
                    attacks = [((self.black_coords[self.piece_selection][0] - 1), (self.black_coords[self.piece_selection][1] - 1)),
                                ((self.black_coords[self.piece_selection][0] + 1), (self.black_coords[self.piece_selection][1] - 1))]

                    for attack in attacks:
                        if attack in self.white_coords:
                            self.valid_moves.append(attack)

                    move = ((self.black_coords[self.piece_selection][0]), (self.black_coords[self.piece_selection][1] - 1))
                    if move not in self.white_coords:
                        self.valid_moves.append(move)

                if self.clicked_coords in self.valid_moves:
                    self.sound_effect(0)
                    return True
                else:
                    return False

    def check_king(self):
        self.valid_moves = []

        match self.turn_cycle:

            # White Turn to move
            case 1:
                moves = [((self.white_coords[self.piece_selection][0]), (self.white_coords[self.piece_selection][1] + 1)), # Up
                                    ((self.white_coords[self.piece_selection][0]), (self.white_coords[self.piece_selection][1] - 1)), # Down
                                    ((self.white_coords[self.piece_selection][0] + 1), (self.white_coords[self.piece_selection][1])), # Right
                                    ((self.white_coords[self.piece_selection][0] - 1), (self.white_coords[self.piece_selection][1])), # Left
                                    ((self.white_coords[self.piece_selection][0] + 1), (self.white_coords[self.piece_selection][1] + 1)), # Down Diagnol Right
                                    ((self.white_coords[self.piece_selection][0] - 1), (self.white_coords[self.piece_selection][1] + 1)), # Down Diagnol Left
                                    ((self.white_coords[self.piece_selection][0] - 1), (self.white_coords[self.piece_selection][1] - 1)), # Up Diagnol Right
                                    ((self.white_coords[self.piece_selection][0] + 1), (self.white_coords[self.piece_selection][1] - 1))] # Up Diagnol Left
                for move in moves:
                    if (move not in self.white_coords) and (move not in self.right_perim_coords):
                        self.valid_moves.append(move)
                
                if self.clicked_coords in self.valid_moves:
                    self.sound_effect(0)
                    return True
                else:
                    return False

            # Black Turn to Move
            case 3:
                moves = [((self.black_coords[self.piece_selection][0]), (self.black_coords[self.piece_selection][1] + 1)), # Down
                                    ((self.black_coords[self.piece_selection][0]), (self.black_coords[self.piece_selection][1] - 1)), # Up
                                    ((self.black_coords[self.piece_selection][0] + 1), (self.black_coords[self.piece_selection][1])), # Right
                                    ((self.black_coords[self.piece_selection][0] - 1), (self.black_coords[self.piece_selection][1])), # Left
                                    ((self.black_coords[self.piece_selection][0] + 1), (self.black_coords[self.piece_selection][1] + 1)), # Down Diagnol Right
                                    ((self.black_coords[self.piece_selection][0] - 1), (self.black_coords[self.piece_selection][1] + 1)), # Down Diagnol Left
                                    ((self.black_coords[self.piece_selection][0] - 1), (self.black_coords[self.piece_selection][1] - 1)), # Up Diagnol Left
                                    ((self.black_coords[self.piece_selection][0] + 1), (self.black_coords[self.piece_selection][1] - 1))] # Up Diagnol Right

                for move in moves:
                    if (move not in self.black_coords) and (move not in self.right_perim_coords):
                        self.valid_moves.append(move)

                if self.clicked_coords in self.valid_moves:
                    self.sound_effect(0)
                    return True
                else:
                    return False

    def check_queen(self):
        self.valid_moves = []

        match self.turn_cycle:

            # White Turn to move
            case 1:
                x = self.white_coords[self.piece_selection][0] # X-axis coord of the selected Queen
                y = self.white_coords[self.piece_selection][1] # Y-axis coord of the selected Queen
                # Direction equations (Up, Down, Diagonals)
                directions = [(lambda z: ((x + z), (y + z))), (lambda z: ((x - z), (y + z))), (lambda z: ((x + z), (y - z))), (lambda z: ((x - z), (y - z))), (lambda z: ((x), (y + z))), (lambda z: ((x), (y - z))), (lambda z: ((x + z), (y))), (lambda z: ((x - z), (y)))] # position functions

                # Calculates possible coords in all directions
                for direction in directions:
                    for i in range(1,8):
                        move = direction(i)

                    # Moves on to next position if blocked or out of bounds
                        if (move in self.white_coords) or (move in self.right_perim_coords):
                            break
                        elif move in self.black_coords:
                            self.valid_moves.append(move)
                            break
                        else:
                            self.valid_moves.append(move)

                if self.clicked_coords in self.valid_moves:
                    self.sound_effect(0)
                    return True
                else:
                    return False

            # Black Turn to move
            case 3:
                x = self.black_coords[self.piece_selection][0]
                y = self.black_coords[self.piece_selection][1]

                directions = [(lambda z: ((x + z), (y - z))), (lambda z: ((x - z), (y - z))), (lambda z: ((x + z), (y + z))), (lambda z: ((x - z), (y + z))), (lambda z: ((x), (y + z))), (lambda z: ((x), (y - z))), (lambda z: ((x + z), (y))), (lambda z: ((x - z), (y)))] # position functions

                for direction in directions:
                    for i in range(1,8):
                        move = direction(i)

                        if (move in self.black_coords) or (move in self.right_perim_coords):
                            break
                        elif move in self.white_coords:
                            self.valid_moves.append(move)
                            break
                        else:
                            self.valid_moves.append(move)

                if self.clicked_coords in self.valid_moves:
                    self.sound_effect(0)
                    return True
                else:
                    return False

    def check_knight(self):
        self.valid_moves = []

        match self.turn_cycle:

            # White Turn to move
            case 1:
                # Knight Move-set (L Shape)
                moves = [((self.white_coords[self.piece_selection][0] + 2), (self.white_coords[self.piece_selection][1] + 1)),
                                    ((self.white_coords[self.piece_selection][0] + 2), (self.white_coords[self.piece_selection][1] - 1)),
                                    ((self.white_coords[self.piece_selection][0] - 2), (self.white_coords[self.piece_selection][1] + 1)),
                                    ((self.white_coords[self.piece_selection][0] - 2), (self.white_coords[self.piece_selection][1] - 1)),
                                    ((self.white_coords[self.piece_selection][0] + 1), (self.white_coords[self.piece_selection][1] + 2)),
                                    ((self.white_coords[self.piece_selection][0] - 1), (self.white_coords[self.piece_selection][1] + 2)),
                                    ((self.white_coords[self.piece_selection][0] + 1), (self.white_coords[self.piece_selection][1] - 2)),
                                    ((self.white_coords[self.piece_selection][0] - 1), (self.white_coords[self.piece_selection][1] - 2))]

                for move in moves:
                    if (move not in self.white_coords) and (move not in self.right_perim_coords):
                        self.valid_moves.append(move)

                if self.clicked_coords in self.valid_moves:
                    self.sound_effect(0)
                    return True
                else:
                    return False

            # Black Turn to move
            case 3:

                moves = [((self.black_coords[self.piece_selection][0] + 2), (self.black_coords[self.piece_selection][1] + 1)),
                                    ((self.black_coords[self.piece_selection][0] + 2), (self.black_coords[self.piece_selection][1] - 1)),
                                    ((self.black_coords[self.piece_selection][0] - 2), (self.black_coords[self.piece_selection][1] + 1)),
                                    ((self.black_coords[self.piece_selection][0] - 2), (self.black_coords[self.piece_selection][1] - 1)),
                                    ((self.black_coords[self.piece_selection][0] + 1), (self.black_coords[self.piece_selection][1] + 2)),
                                    ((self.black_coords[self.piece_selection][0] - 1), (self.black_coords[self.piece_selection][1] + 2)),
                                    ((self.black_coords[self.piece_selection][0] + 1), (self.black_coords[self.piece_selection][1] - 2)),
                                    ((self.black_coords[self.piece_selection][0] - 1), (self.black_coords[self.piece_selection][1] - 2))]
                for move in moves:
                    if (move not in self.black_coords) and (move not in self.right_perim_coords):
                        self.valid_moves.append(move)

                if self.clicked_coords in self.valid_moves:
                    self.sound_effect(0)
                    return True
                else:
                    return False

    def check_bishop(self):
        self.valid_moves = []

        match self.turn_cycle:

            # White Turn to move
            case 1:
                x = self.white_coords[self.piece_selection][0] # X-axis coord of the selected Bishop
                y = self.white_coords[self.piece_selection][1] # Y-axis coord of the selected Bishop

                # Direction equations (Diagonals)
                directions = [(lambda z: ((x + z), (y + z))), (lambda z: ((x - z), (y + z))), (lambda z: ((x + z), (y - z))), (lambda z: ((x - z), (y - z)))] # position functions

                # Calculates diagonal positions
                for direction in directions:
                    for i in range(1,8):
                        move = direction(i)

                    # Moves on to next position if blocked or out of bounds
                        if (move in self.white_coords) or (move in self.right_perim_coords):
                            break
                        elif move in self.black_coords:
                            self.valid_moves.append(move)
                            break
                        else:
                            self.valid_moves.append(move)

                if self.clicked_coords in self.valid_moves:
                    self.sound_effect(0)
                    return True
                else:
                    return False

            # Black Turn to move
            case 3:
                x = self.black_coords[self.piece_selection][0]
                y = self.black_coords[self.piece_selection][1]

                directions = [(lambda z: ((x + z), (y - z))), (lambda z: ((x - z), (y - z))), (lambda z: ((x + z), (y + z))), (lambda z: ((x - z), (y + z)))] # position functions

                for direction in directions:
                    for i in range(1,8):
                        move = direction(i)

                        if (move in self.black_coords) or (move in self.right_perim_coords):
                            break
                        elif move in self.white_coords:
                            self.valid_moves.append(move)
                            break
                        else:
                            self.valid_moves.append(move)

                if self.clicked_coords in self.valid_moves:
                    self.sound_effect(0)
                    return True
                else:
                    return False

    def check_rook(self):
        self.valid_moves = []

        match self.turn_cycle:

            # White Turn to move
            case 1:
                x = self.white_coords[self.piece_selection][0] # X-axis coord of the selected Rook
                y = self.white_coords[self.piece_selection][1] # Y-axis coord of the selected Rook

                # Rook Direction equations (Up and Down)
                directions = [(lambda z: ((x), (y + z))), (lambda z: ((x), (y - z))), (lambda z: ((x + z), (y))), (lambda z: ((x - z), (y)))] # position functions

                # Calculates horizonal and vertical positions using equations stored in lambda functions
                for direction in directions:
                    for i in range(1,8):
                        move = direction(i)

                    # Moves on to next position if blocked or out of bounds
                        if (move in self.white_coords) or (move in self.right_perim_coords):
                            break
                        elif move in self.black_coords:
                            self.valid_moves.append(move)
                            break
                        else:
                            self.valid_moves.append(move)

                if self.clicked_coords in self.valid_moves:
                    self.sound_effect(0)
                    return True
                else:
                    return False

            # Black Turn to move
            case 3:
                x = self.black_coords[self.piece_selection][0]
                y = self.black_coords[self.piece_selection][1]

                directions = [(lambda z: ((x), (y + z))), (lambda z: ((x), (y - z))), (lambda z: ((x + z), (y))), (lambda z: ((x - z), (y)))] # position functions

                for direction in directions:
                    for i in range(1,8):
                        move = direction(i)

                        if (move in self.black_coords) or (move in self.right_perim_coords):
                            break
                        elif move in self.white_coords:
                            self.valid_moves.append(move)
                            break
                        else:
                            self.valid_moves.append(move)

                if self.clicked_coords in self.valid_moves:
                    self.sound_effect(0)
                    return True
                else:
                    return False

    def eliminated_piece(self):

        if self.turn_cycle == 1 and self.clicked_coords in self.black_coords:
            eliminated_index = self.black_coords.index(self.clicked_coords) # Gets the index of the eliminated black piece
            eliminated_piece = self.black_pieces.pop(eliminated_index) # Removes the eliminated black piece from the piece list
            self.black_coords.pop(eliminated_index) # Removes the eliminated black piece coord
            self.eliminated_b.append(eliminated_piece) # Adds eliminated piece to the eliminated list
            self.delete_piece(2)
            self.sound_effect(1)

        elif self.turn_cycle == 3 and self.clicked_coords in self.white_coords:
            eliminated_index = self.white_coords.index(self.clicked_coords)
            eliminated_piece = self.white_pieces.pop(eliminated_index)
            self.white_coords.pop(eliminated_index)
            self.eliminated_w.append(eliminated_piece)
            self.delete_piece(2)
            self.sound_effect(1)

        self.draw_elim(self.eliminated_w, self.eliminated_b)

        if ("king" in self.eliminated_w):
            self.winner = "Player 2"
            self.check_mate_flag = 1
        elif ("king" in self.eliminated_b):
            self.winner = "Player 1"
            self.check_mate_flag = 1

    def delete_piece(self, mode = 0, previous_coords = (0,0)):
        # Deletes piece by bliting the chess board square with its correspoding color
        # Mode 1: Deletion of piece upon moving
        # Mode 2: Deletion of piece upon collision
        match mode:
            case 1:
                if previous_coords != self.clicked_coords:
                    if previous_coords in self.lg_coords:
                        pygame.draw.rect(self.parent_surface, "light grey", [previous_coords[0] * 60,previous_coords[1] * 60, 60, 60], 50,)
                    else:
                        pygame.draw.rect(self.parent_surface, "dark grey", [previous_coords[0] * 60,previous_coords[1] * 60, 60, 60], 50,)
                        
            case 2:
                if self.clicked_coords in self.lg_coords:
                    pygame.draw.rect(self.parent_surface, "light grey", [self.clicked_coords[0] * 60,self.clicked_coords[1] * 60, 60, 60], 50,)
                else:
                    pygame.draw.rect(self.parent_surface, "dark grey", [self.clicked_coords[0] * 60,self.clicked_coords[1] * 60, 60, 60], 50,)

    def check_promo(self):

            # Checks if any pawn piece is at promotion coordinates and returns True if there is
            for i in range(len(self.white_pieces)):
                if self.white_pieces[i] == "pawn":
                    if self.white_coords[i] in self.promo_white:
                        self.previous_tc = self.turn_cycle # Stores the turn cycle - Needed to resume the game once the promotion ends
                        return True

            for i in range(len(self.black_pieces)):
                if self.black_pieces[i] == "pawn" and self.black_coords[i] in self.promo_black:
                    self.previous_tc = self.turn_cycle
                    return True

    def promotion(self):

        pygame.draw.rect(self.parent_surface, "white", [0,480,480,120], border_radius=3) # Clears bottom area of the screen to draw promotion pieces
        Game.outline_tiles(self.parent_surface)                                          # Redraws outline tiles to get rid of highlights

        x_coord = [0, 0, 120, 180, 240, 300] # X-axis coords to draw promotion piece options, one by one
        # Adding the out of boundary coords in order for it to be clickable for promotion, these coords are not in self.all_coords
        self.all_coords.append((2,8))
        self.all_coords.append((3,8))
        self.all_coords.append((4,8))
        self.all_coords.append((5,8))

        # Promotion Piece coords
        queen = (2,8)
        knight = (3,8)
        bishop = (4,8)
        rook = (5,8)

        # Player 1 Promotion
        if self.previous_tc == 1:
            # Draws Promotion Pieces One by One
            for i in range(2,6,1):
                self.parent_surface.blit(self.white_images[i], (x_coord[i], 480))

            self.delete_piece(2) # Delete Old Demoted Pawn

            if self.clicked_coords == queen:
                self.white_pieces[self.piece_selection] = "queen" # Changes pawn piece to a queen piece
                # Draws new promoted piece in the same location
                self.parent_surface.blit(self.white_images[2], (self.white_coords[self.piece_selection][0] * 60 + 5, self.white_coords[self.piece_selection][1] * 60 + 5))
                Game.master_turn_cycle = 2 # Resumes Game - Moves on to the next turn

            if self.clicked_coords == knight:
                self.white_pieces[self.piece_selection] = "knight"
                self.parent_surface.blit(self.white_images[3], (self.white_coords[self.piece_selection][0] * 60 + 5, self.white_coords[self.piece_selection][1] * 60 + 5))
                Game.master_turn_cycle = 2

            if self.clicked_coords == bishop:
                self.white_pieces[self.piece_selection] = "bishop"
                self.parent_surface.blit(self.white_images[4], (self.white_coords[self.piece_selection][0] * 60 + 5, self.white_coords[self.piece_selection][1] * 60 + 5))
                Game.master_turn_cycle = 2

            if self.clicked_coords == rook:
                self.white_pieces[self.piece_selection] = "rook"
                self.parent_surface.blit(self.white_images[5], (self.white_coords[self.piece_selection][0] * 60 + 5, self.white_coords[self.piece_selection][1] * 60 + 5))
                Game.master_turn_cycle = 2

        # Player 2 Promotion
        elif self.previous_tc == 3:
            for i in range(2,6,1):
                self.parent_surface.blit(self.black_images[i], (x_coord[i], 480))

            self.delete_piece(2)

            if self.clicked_coords == queen:
                self.black_pieces[self.piece_selection] = "queen"
                self.parent_surface.blit(self.black_images[2], (self.black_coords[self.piece_selection][0] * 60 + 5, self.black_coords[self.piece_selection][1] * 60 + 5))
                Game.master_turn_cycle = 0

            if self.clicked_coords == knight:
                self.black_pieces[self.piece_selection] = "knight"
                self.parent_surface.blit(self.black_images[3], (self.black_coords[self.piece_selection][0] * 60 + 5, self.black_coords[self.piece_selection][1] * 60 + 5))
                Game.master_turn_cycle = 0

            if self.clicked_coords == bishop:
                self.black_pieces[self.piece_selection] = "bishop"
                self.parent_surface.blit(self.black_images[4], (self.black_coords[self.piece_selection][0] * 60 + 5, self.black_coords[self.piece_selection][1] * 60 + 5))
                Game.master_turn_cycle = 0

            if self.clicked_coords == rook:
                self.black_pieces[self.piece_selection] = "rook"
                self.parent_surface.blit(self.black_images[5], (self.black_coords[self.piece_selection][0] * 60 + 5, self.black_coords[self.piece_selection][1] * 60 + 5))
                Game.master_turn_cycle = 0

    def check_mate(self):

        # Returns True if King is Eliminated
        match self.check_mate_flag:
            case 0:
                return False
            case 1:
                #print("Checkmate")
                self.sound_effect(2)
                return True, self.winner

    def draw_elim(self, eliminated_white, eliminated_black):
        # Draws eliminated piece on the side of the screen, using eliminated piece list of each colour

        # Creates a list for the y-axis position of the eliminated pieces
        elim_pos_y = list(range(10,600,48)) # (10 = y-axis offset, 600 = max eliminated piece pos, 45 = scale of images)

        if eliminated_white or eliminated_black:
            for i in range(0,len(eliminated_white)):
                index_w = self.piece_list.index(eliminated_white[i]) # Finds the index in the piece list, of the eliminated piece
                self.parent_surface.blit(self.white_images[index_w], (480, elim_pos_y[i])) # Draws the elminated piece using the above index

            for i in range(0,len(eliminated_black)):
                index_b = self.piece_list.index(eliminated_black[i])
                self.parent_surface.blit(self.black_images[index_b], (540, elim_pos_y[i]))

class Game:
    # Game States: 0 = White Turn, No Selection, 1 = White turn, Piece Selected, 2 = Black Turn, No selection, 3 = Black Turn, Piece Selected
    # 4 = Promotion
    master_turn_cycle = 0 # Dictates the Game State
    player_1_turns = 1 # Number of Player 1 Turns
    player_2_turns = 0 # Number of Player 2 turns

    def __init__(self):

        self.game_running = True
        pygame.init()
        pygame.mixer.init() # Init Sound System

        #Init Images, Fonts, etc.
        pygame.display.set_caption("Said's Chess Game")
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Creates a display[w x h]
        self.start_image = pygame.image.load("resources/start_screen.jpg") # Loads start screen image
        self.end_image = pygame.image.load("resources/end_screen.jpg") # Loads end screen image
        self.play_button = pygame.image.load("resources/Play_Button.png") # Loads start screen image
        self.font_big = pygame.font.SysFont("Gabriola", 80)  # Initialises big start screen font
        self.font_small = pygame.font.SysFont("Gabriola", 40)  # Initialises small start screen font

        # Init text to be displayed
        self.title_text = self.font_big.render("Classical Chess", True, (255, 255, 255))
        self.credits_text = self.font_small.render("Said Ali", True, (255, 255, 255))
        self.game_end_text = self.font_small.render("Game Over", True, (255, 255, 255))

        # Game clock, timer, and fps
        self.timer = pygame.time.Clock()
        self.fps = 60

        # Chess Board Coords
        self.all_coords = [] # All Chess Board Coords
        self.lg_squares = [] # Light Grey Square Coords
        self.dg_squares = [] # dark grey square coords

        # Right Screen Perimeter Coords
        self.right_perim_coords = [(8,0), (8,1), (8,2), (8,3), (8,4), (8,5), (8,6),
                                    (8,7), (8,8), (9,0), (9,1), (9,2), (9,3), (9,4), (9,5), (9,6), (9,7)]
        # Winner of the game
        self.winner = None

        # Mouse x and y coords
        self.x = 0
        self.y = 0
        self.clicked_coords = [(0,1)] # Init clicked coords - starts at player one's first pawn
        self.pieces = Pieces(self.surface, self.all_coords, self.lg_squares, self.dg_squares, self.right_perim_coords)
        self.start_screen()

    def start_screen(self):
    # Draw images and texts
        self.surface.blit(self.start_image, (0, 0))
        self.surface.blit(self.title_text, (120, 70))
        self.surface.blit(self.credits_text, (7, 10))
        self.surface.blit(self.play_button, (180, 520))
        pygame.display.flip()

        while (self.game_running):  # Start Screen Loop

            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.exit()

                # Play game if button is clicked
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                   if (180 < event.pos[0] < 400) and (520 < event.pos[1] < 590):
                        self.game_run()

                elif event.type == QUIT:
                    self.exit()

    def chess_coords(self):

        # Creates all chess board coords
        for i in range(8):
            for j in range(8):
                self.all_coords.append((i,j))

        # Converts all_coords and lg_coords to sets, takes differences, and converts back to a list to find the dark grey coords
        set_lg = set(self.lg_squares)
        set_all_coords = set(self.all_coords)
        self.dg_squares = list(set_all_coords.difference(set_lg))

    def draw_chess_board(self):

        self.surface.fill("dark gray") # Main Surface Color

        # Drawing square chess board pattern ||
        for i in range(32):
            column = i % 4
            row = i // 4
            if row % 2 == 0:
                pygame.draw.rect(self.surface, "light gray", [360 - (column * 120), row * 60, 60, 60])
                self.lg_squares.append(( (360 - (column * 120)) // 60, (row * 60) // 60)) # Stores and formats light grey squares coords
            else:
                pygame.draw.rect(self.surface, "light gray", [420 - (column * 120), row * 60, 60, 60])
                self.lg_squares.append(( (420 - (column * 160)) // 60, (row * 60) // 60)) # Stores and formats light grey squares coords

        pygame.draw.rect(self.surface, "black", [480,0,120,600], 2) # Creates boarderd area for right-side section for the eliminated pieces

        Game.outline_tiles(self.surface) # Creates Chess Board Box Outlines

    @classmethod
    def outline_tiles(cls, surface):
        # Outlines Chess Tiles
        for i in range(0,540,60):
            pygame.draw.line(surface,[0,0,0], (i,0), (i,480), 3) # Columns
            pygame.draw.line(surface,[0,0,0], (0,i), (480,i), 3) # Row

    def game_prompts(self):

        self.action_text = ["Player 1: Select a Piece!", "Player 1: Select a Position!", "Player 2: Select a Piece", "Player 2: Select a Position", "Promotion: Select a Piece"]

        # Turn Cycle used as action_text Index
        if Game.master_turn_cycle == 4:
            self.surface.blit(self.font_small.render(self.action_text[self.master_turn_cycle], True, (0, 0, 0)), (80, 525))
        else:
            pygame.draw.rect(self.surface, [245, 255, 250], [0,480,480,120], 80) # Erases text in game command section by filling section
            self.surface.blit(self.font_small.render(self.action_text[self.master_turn_cycle], True, (0, 0, 0)), (80, 525))

    @classmethod
    def turn_cycler(cls):
        # Cycles the Turn of the Game Once a Piece is Clicked
        cls.master_turn_cycle += 1
        if cls.master_turn_cycle > 3:
            cls.master_turn_cycle = 0

        # Tracks Total Number of Turns Had by Players
        if cls.master_turn_cycle == 0:
            cls.player_1_turns += 1
        elif cls.master_turn_cycle == 2:
            cls.player_2_turns += 1

    def play_chess(self):
        self.pieces.check_clicked(Game.master_turn_cycle, self.clicked_coords[0]) # Checks if a piece is clicked
        self.game_prompts()                                                       # Draws game prompts
        self.winner = self.pieces.check_mate()                                    # Checks if there is a winner
        if self.winner:
            #print(self.winner[1])
            self.game_over()

        pygame.display.flip()

    def reset_game(self):
        # Resets Key Game Variables, Creates a New Pieces Object, and Runs the Game
        Game.master_turn_cycle = 0
        Game.player_1_turns = 1
        Game.player_2_turns = 0
        self.pieces = Pieces(self.surface, self.all_coords, self.lg_squares, self.dg_squares, self.right_perim_coords)
        self.game_run()

    def game_over(self):

        # Draw images and texts
        self.winner_text = self.font_small.render(f"{self.winner[1]} has Won", True, (255, 255, 255))
        self.surface.blit(self.end_image, (0, 0))
        self.surface.blit(self.game_end_text, (230, 7))
        self.surface.blit(self.winner_text, (10, 110))
        self.surface.blit(self.play_button, (180, 520))
        pygame.display.flip()

        while (self.game_running):  # Game Over Screen Loop

            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.exit()

                # Play the Game Again if the Button is Clicked
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if (180 < event.pos[0] < 400) and (520 < event.pos[1] < 590):
                        self.reset_game()

                elif event.type == QUIT:
                    self.exit()

    def timer(self):
        # Chess Game Timer - To Be Added
        pass

    def game_run(self):
        self.chess_coords()
        self.draw_chess_board()
        self.pieces.draw_all()
        pygame.display.flip()

        while (self.game_running):  # Main Program Loop
            
            # Game Event Handling
            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.x = event.pos[0] // 60 # (// floor 60) formats mouse pos integers to match chess board square drawn positions (60 x 60)
                    self.y = event.pos[1] // 60
                    self.clicked_coords = [(self.x,self.y)]
                    #print(self.clicked_coords)

                elif event.type == QUIT:
                    self.exit()

            self.play_chess()

            self.timer.tick(self.fps) # Set game to 60 FPS

    def exit(self):
        self.game_running = False

if __name__ == "__main__":
    game = Game()
