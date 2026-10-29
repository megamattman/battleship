########
#TODO
# Ships that are more tan one grid space
# Playable by player in console
# Some GUI
########

from random import randint
import lib.game_board as game_board
import lib.battleship as battleship
# battlefield parameters
board_rows = 10
board_cols = 10
#debug message vars
debug = 1
ship_gen_error_msg = "Incorrect ships"
ship_gen_error_flg = 0
#end debug mesg vars

#class to hold row/col
class coords (object):
    def __init__ (self, row = 0, col = 0) :
        self.row = row
        self.col = col

#board that has the boat locations
master_board = game_board.GameBoard(board_rows, board_cols, 'O', 'F')

#board that has players hit locations
player_board = game_board.GameBoard(board_rows, board_cols, 'O', 'X')

#Dictionary of battleships, the key is the letter that fills in the master board
battleships ={}

if (debug): 
    print("master board")
    master_board.print_board()

    print("\nplayer board")
    player_board.print_board()

#Fills a space in on the master boards, represents a 'boat'
#If the random location is already filled, call the fucntion again

#NOTE: A generation count to break the function if it falls into a deep recursive loop
#      This can happen if asked to gen more ships than available spaces or bad luck

def add_random_enemy_ship(board, gen):
    #Recursive function breaker
    if (gen >= 10):
        ship_gen_error_flg = 1
        return -1
    #generate random location
    row = randint(0, board.rows-1)
    col = randint(0, board.cols-1)
    if (debug):
        print("New ship at %s,%d"%( chr(ord('A')+row),col))
    #if failed to add the ship, try again
    if (add_enemy_ship(board,row,col) == False):
        add_random_enemy_ship(board, gen+1)
    #return no_ships
    return board.filled_spaces

#actually add the ship
def add_enemy_ship (board, row, col):
    return board.fill_space(row,col) 

#Output message when ship is hit 
def output_hit_string(battleships,ship_id): 
    if (ship_id == 'F') :
        print ("fishing ship has been hit!")
    else :
        ship_name = battleships[ship_id].name
        if battleships[ship_id].ship_hit() == True:
            print ("YOU SUNK MY %s!"%  ship_name.upper())

#Take the player shot coords return True on Hit, False on miss
def player_shot(row, col, player_board, master_board, battleships):
    #Check if already shot, is_space_empty(false) on play board
    if (player_board.is_space_empty(row,col) == True):
        # if NOT empty there a boat, check for empty
        if (master_board.is_space_empty(row,col) == False) :
            # if boat set player board to hit
            player_board.set_space(row,col, 'H', 1)
            output_hit_string(battleships, master_board.get_space(row,col))
            return True
        else:
            #if not set player board location to X
            player_board.fill_space(row,col)
            return False
    else:
        print ("Location %d,%d has already been hit" % (row,col))
        return False


master_board.print_board()

