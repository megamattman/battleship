########
#TODO
# Ships that are more tan one grid space
# Playable by player in console
# Some GUI
########

from random import randint
import battleship_test
import game_board_module
import battleship_module
#battle field parameters
board_rows = 10;
board_cols = 10;
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
master_board = game_board_module.game_board(board_rows, board_cols, 'O', 'F')

#board that has players hit locations
player_board = game_board_module.game_board(board_rows, board_cols, 'O', 'X')

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
        battleships[ship_id].ship_hit()
        
        if (battleships[ship_id].destroyed):
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

#Add random ships
no_battleships = 5;
for i in range (5):
    add_random_enemy_ship(master_board, 0)
#Check correct number of ships
battleship_test.check_battleship_number(5,master_board.filled_spaces)
#end random ship add
print ("ADD A SHIP TEST")
#add ship in known location
if (master_board.get_space(0,0) != '0') :
    master_board.fill_space(0,0)
    battleship_test.check_battleship_number(6,master_board.filled_spaces)
    master_board.fill_space(0,0)
    battleship_test.check_battleship_number(6,master_board.filled_spaces)
master_board.print_board()
#Set up known empty space
master_board.empty_space(1,1)
#Player shot test
print("PLAYER MISS TEST")
#Miss before, After and repeat cases
miss_row = 1
miss_col = 1
battleship_test.check_grid_pos(player_board, miss_row,miss_col, 'O', "Empty Space")
battleship_test.check_result(player_shot(miss_row,miss_col,player_board,master_board,battleships), False, "Empty Space")
battleship_test.check_grid_pos(player_board, miss_row,miss_col, 'X', "Player Miss")
battleship_test.check_result(player_shot(miss_row,miss_col,player_board,master_board,battleships), False, "Prev miss shot")
battleship_test.check_grid_pos(player_board, miss_row,miss_col, 'X', "Player Repeated Miss")
#end miss
#player hit
print("PLAYER HIT TEST")
hit_row = 0
hit_col = 0
battleship_test.check_grid_pos(player_board, hit_row,hit_col, 'O', "Before player hit")
battleship_test.check_result(player_shot(hit_row,hit_col,player_board,master_board,battleships), True, "Good shot")
battleship_test.check_grid_pos(player_board, hit_row,hit_col, 'H', "Player Hit")
battleship_test.check_result(player_shot(hit_row,hit_col,player_board,master_board,battleships), False, "Prev hit shot")
battleship_test.check_grid_pos(player_board, hit_row,hit_col, 'H', "Hit repeat")
#end player shot test

#Adding a larger boat
print("DEPLOY THE MATTAZOR")
#Create it 
battleship_matt = battleship_module.battleship("Mattazor", 4)
#DEPLOY THE BOAT
for i in range(4):
    master_board.set_space(2,int(i),'M',1)
    battleship_test.check_grid_pos(master_board, 2,i, 'M', "Mattazor Deploy" + str(i))

#TRACK THE SHIP
battleships['M'] = battleship_matt

for i in range(4):
    battleship_test.check_grid_pos(player_board, 2,i, player_board.empty_space, "Before Mattazor hit" + str(i))
    battleship_test.check_result(player_shot(2,i,player_board,master_board,battleships), True, "Good shot Mattazor" + str(i))
    battleship_test.check_grid_pos(player_board, 2,i, 'H', "Player Hit Mattazor" + str(i))
    battleship_test.check_result(player_shot(2,i,player_board,master_board,battleships), False, "Prev hit shot Mattazor" + str(i))
    battleship_test.check_grid_pos(player_board, 2,i, 'H', "Hit repeat Mattazor" + str(i))

battleship_test.check_result(battleships['M'].destroyed, True, "MATTAZOR DESTROYED")

#Will return a list of coords in the coords object format
#Will check 'end' of potential coord range,
#If out of bound will return empty 
def get_list_of_coords (row, col, facing, size, board):
    ship_coords =[]
    if   facing == 'U':
        if (row-size) < 0 :
            return ship_coords
        for i in range(size):
            ship_coords.append(coords(row-i,col)) 
    elif facing == 'D':
        if (row-size) > board.row-1 :
            return ship_coords
        for i in range(size):
            ship_coords.append(coords(row+i,col)) 
    elif facing == 'L':
        if (row-size) < 0 :
            return ship_coords
        for i in range(size):
            ship_coords.append(coords(row,col-i)) 
    elif facing == 'R':
        if (row-size) > board.rows :
            return ship_coords
        for i in range(size):
            ship_coords.append(coords(row,col+i)) 
    return ship_coords

#Makes sure all coords have a particular char
def check_valid_ship_coords(ships_coords, board, legal_char):
    for item in ship_coords:
        row = ship_coords[item].row
        col = ship_coords[item].col
        if (board.board[row][col] != legal_char):
            return False
    return True

#check the request facing to determine if valid
#on fail return list of valid facings
def check_facing (row, col, facing, size, master_board) :
    possible_ships_coords = get_list_of_coords(row, col, facing, size)
    if (check_valid_ship_coords == True):
        return True
    
    return False
for items in get_list_of_coords(4,4,'U',2, master_board):
    print str(items.row) + " " +str(items.col)

#Start position will be added to 
#def place_ship (row, col, master_board, battleship, facing) :
    
