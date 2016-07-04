########
#TODO
# Ships that are more tan one grid space
# Playable by player in console
# Some GUI
########

from random import randint
import battleship_test
import game_board_module
#battle field parameters
board_rows = 5;
board_cols = 5;
#debug message vars
debug = 0
ship_gen_error_msg = "Incorrect ships"
ship_gen_error_flg = 0
#end debug mesg vars

#board that has the boat locations
master_board = game_board_module.game_board(board_rows, board_cols, 'O', 'B')

#board that has players hit locations
player_board = game_board_module.game_board(board_rows, board_cols, 'O', 'X')

#Fills a space in on the master boards, represents a 'boat'
#If the random location is already filled, call the fucntion again

#NOTE: A generation count to break the function if it falls into a deep recursive loop
#      This can happen if asked to gen more ships than available spaces
print("master board")
master_board.print_board()

print("\nplayer board")
player_board.print_board()
def add_enemy_ship(board, gen):
    #Recursive function breaker
    if (gen >= 10):
        ship_gen_error_flg = 1
        return -1
    #generate random location
    row = randint(0, board.rows-1)
    col = randint(0, board.cols-1)
    if (debug):
        print("New ship at %d,%d"%(row,col))
    #if failed to fill space on board, try again
    if (board.fill_space(row,col) == False):
        add_enemy_ship(board, gen+1)
    #return no_ships
    return board.filled_spaces

#Take the player shot coords return True on Hit, False on miss
def player_shot(row, col, player_board, master_board):
    #Check if already shot, is_space_empty(false) on play board
    if (player_board.is_space_empty(row,col) == True):
        # if NOT empty there a boat, check for empty
        if (master_board.is_space_empty(row,col) == False) :
            # if boat set player board to hit
            player_board.set_space(row,col, 'H', 1)
            return True
        else:
            #if not set player board location to X
            player_board.fill_space(row,col)
            return False
    else:
        print ("Location %d,%d has already been hit" % (row,col))
        return False

    

#Add random ships
no_battleships = 5;
for i in range (5):
    add_enemy_ship(master_board, 0)
#Check correct number of ships
battleship_test.check_battleship_number(5,master_board.filled_spaces)
#end random ship add
#add ship in known location
master_board.fill_space(0,0)
battleship_test.check_battleship_number(6,master_board.filled_spaces)
master_board.print_board()
#Set up known empty space
master_board.empty_space(1,1)
#Player shot test
battleship_test.check_result_of_shot(player_shot(1,1,player_board,master_board), False, "Empty Space")
battleship_test.check_result_of_shot(player_shot(1,1,player_board,master_board), False, "Prev miss shot")
battleship_test.check_result_of_shot(player_shot(0,0,player_board,master_board), True, "Good shot")
battleship_test.check_result_of_shot(player_shot(0,0,player_board,master_board), False, "Prev hit shot")
#end player shot test
#player shot test
