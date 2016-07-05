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
master_board.print_board()
for i in range(4):
    battleship_test.check_grid_pos(player_board, 2,i, player_board.empty_char, "Before Mattazor hit" + str(i))
    battleship_test.check_result(player_shot(2,i,player_board,master_board,battleships), True, "Good shot Mattazor" + str(i))
    battleship_test.check_grid_pos(player_board, 2,i, 'H', "Player Hit Mattazor" + str(i))
    battleship_test.check_result(player_shot(2,i,player_board,master_board,battleships), False, "Prev hit shot Mattazor" + str(i))
    battleship_test.check_grid_pos(player_board, 2,i, 'H', "Hit repeat Mattazor" + str(i))

mattazor_destroyed = battleships['M'].hits >= battleships['M'].size
battleship_test.check_result(mattazor_destroyed, True, "MATTAZOR DESTROYED")

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
        if (row+size) > board.rows-1 :
            return ship_coords
        for i in range(size):
            ship_coords.append(coords(row+i,col)) 
    elif facing == 'L':
        if (col-size) < 0 :
            return ship_coords
        for i in range(size):
            ship_coords.append(coords(row,col-i)) 
    elif facing == 'R':
        if (col+size) > board.cols-1 :
            return ship_coords
        for i in range(size):
            ship_coords.append(coords(row,col+i)) 
    return ship_coords

##Get list of coords tests
test_coords = get_list_of_coords(4,4,'U',2, master_board) 
for items in test_coords:
    print str(items.row) + " " +str(items.col)
battleship_test.check_result(len(test_coords), 2, "2 space ship")
##End of get_coord_list tests

#Makes sure all coords have a particular char
#Standard use would be checking if all coords are empty for boat placement
#Made more generic to make function more useful
def check_valid_ship_coords(ship_coords, board, legal_char):
    for item in ship_coords:
        row = item.row
        col = item.col
        if (board.get_space(row,col) != legal_char):
            print("Occupied space %d,%d" % (row, col))
            return False
    return True

#check the request facing to determine if valid
#if not valid, return empty list
def check_facing (row, col, facing, size, board) :
    possible_ship_coords = get_list_of_coords(row, col, facing, size, board)
    #return false if ships coords can't be attained
    if not possible_ship_coords :
        if (debug) :
            print("No possible coords, facing %s" %facing)
        return possible_ship_coords
    #Check all positions are empty
    if (check_valid_ship_coords(possible_ship_coords, board, board.empty_char) == True):
        return possible_ship_coords
    #if there is an occupied space in the coord list return empty list    
    possible_ship_coords =[]
    return possible_ship_coords

#Place the ship
#update the master board with the location of the ship
def place_ship (battleship, board):
    for coord in battleship.coords :
        print("Placing ship %s at loc %d,%d with char %s" %(battleship.name, coord.row, coord.col, battleship.ship_id))
        board.set_space(coord.row, coord.col, battleship.ship_id, 1)

##test object class
class ship_place_test(object):
    def __init__ (self, ship, coords, facing):
        self.facing = facing
        self.ship = ship
        self.coords = coords

ships_to_place = [ship_place_test(battleship_module.battleship("Mattazor", 4, "M"), coords(0,0), "D"),
                  ship_place_test(battleship_module.battleship("Lukiator", 3, "L"), coords(0,4), "R"),
                  ship_place_test(battleship_module.battleship("Olidactyl", 2, "I"), coords(3,3), "L"), 
                  ship_place_test(battleship_module.battleship("SuperDan", 4, "S"), coords(0,0), "D"),
                  ship_place_test(battleship_module.battleship("Timmy", 4, "T"), coords(1,1), "L")]

#clear the board
master_board.init_board()
master_board.print_board()

##Place all the ships in the ship_to_place list
#Test cases
# --Valid ships of different sizes
# --Invalid 'first choice' facing
# --Invalid position (no available facings)

for i in range(len(ships_to_place)):
    ship_to_place = ships_to_place[i]

    
    u_coords = check_facing(ship_to_place.coords.row, ship_to_place.coords.col, 'U', ship_to_place.ship.size, master_board) 
    d_coords = check_facing(ship_to_place.coords.row, ship_to_place.coords.col, 'D', ship_to_place.ship.size, master_board) 
    l_coords = check_facing(ship_to_place.coords.row, ship_to_place.coords.col, 'L', ship_to_place.ship.size, master_board) 
    r_coords = check_facing(ship_to_place.coords.row, ship_to_place.coords.col, 'R', ship_to_place.ship.size, master_board) 


    #Automated decision making, when the first choice is not 
    alternate_facings = []
    available_coords = {}    
    if d_coords :
        available_coords["D"] = d_coords 
        alternate_facings.append("D")
    if l_coords :        
        available_coords["L"] = l_coords
        alternate_facings.append("L")
    if u_coords :
        available_coords["U"] = u_coords
        alternate_facings.append("U")
    if r_coords :
        available_coords["R"] = r_coords
        alternate_facings.append("R")
    
    if not available_coords:
        print ("The ship %s location %d,%d, has no suitable facings" % (ship_to_place.ship.name, ship_to_place.coords.row, ship_to_place.coords.col))
        continue

    if ship_to_place.facing in available_coords:
        requested_coords = available_coords[ship_to_place.facing]
        #Check the correct number of coords generated for ship size
    else:
        facing = alternate_facings[randint(0, len(alternate_facings)-1)]
        print("Original facing %s not available selecting facing %s" %(ship_to_place.facing, facing))
        requested_coords = available_coords[facing]
                                          
    ship_to_place.ship.coords = requested_coords    
    battleship_test.check_result(len(ship_to_place.ship.coords), ship_to_place.ship.size, "Coord count check for " + ship_to_place.ship.name)
    place_ship(ship_to_place.ship, master_board)
        #check the ships ID is in the grid where expected
    for coord in ship_to_place.ship.coords:
        row = coord.row
        col = coord.col
        battleship_test.check_grid_pos(master_board, row, col, ship_to_place.ship.ship_id, "Checking grid space for " + ship_to_place.ship.name)

master_board.print_board()

