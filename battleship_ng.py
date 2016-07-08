#globals
debug= 0
game_pieces=[]

#class to hold row/col
class coords (object):
    def __init__ (self, row = 0, col = 0) :
        self.row = row
        self.col = col

class game_piece (object):
    def __init__ (self, name="blank", piece_id='F', coords=[]) :
        self.name = name
        self.piece_id = piece_id
        self.coords = coords

    def add_coord (self, coord):
        assert type(coord) is coords, \
            "Add coord got %s instead of coords object" %type(coord)
        self.coords.append(coord)

class battleship (game_piece):
    def __init__ (self, name='blank', piece_id='F', coords=[], size=0):
        game_piece.__init__(self, name, piece_id, coords)
        self.size = 0
        self.hits = 0

    #return True if board destroyed
    def boat_hit(self):
        self.hits += 1
        if (self.hits >= self.size):
            return True
        else:
            return False   

class board_ng (object):
    def __init__ (self, rows, cols, empty_char = 'O'):
        self.rows = rows
        self.cols = cols
        self.empty_char = empty_char

    #Get a list of all the game pieces and modify an empty board
    def print_board(self, pieces):
        output_grid=[]
        #Create empty grid
        for i in range(self.rows):
            output_grid.append([self.empty_char]*self.cols)
        #The key is a char to place into the output grid
        for piece in pieces:
            for coord in piece.coords:
                row = coord.row
                col = coord.col
                if debug : 
                    print str(row) + " " + str(col) + " " + str(piece.piece_id)
                output_grid[row][col] = piece.piece_id

        for col in range(self.cols):
            if (col == 0):
                print "  " + str(col),
            else:
                print col,
        else:
            print
        row_no = 0
        for row in output_grid:
            print  chr(ord('A')+row_no) + " " + " ".join(row)
            row_no += 1
        else :
            print
        return output_grid


def print_player_board(game_pieces, board, piece_type):
    pieces_to_print = get_piece_type(game_pieces, piece_type)
    return board.print_board(pieces_to_print)

def get_piece_type(game_pieces, piece_type) :
    output_pieces = []
    for piece in game_pieces:
        if type(piece) == piece_type :
            output_pieces.append(piece)
    return output_pieces
        
def search_coord (pieces, player_coord) :
    for piece in pieces :
        for coords in piece.coords :
            if player_coord.row == coords.row and player_coord.col == coords.col :
                return True
    return False


def player_shot(game_pieces, player_coord) :
    #check through the relevant game pieces and 
    #see if this shot has already been fired
    pieces = get_piece_type(game_pieces, game_piece())
    #shot already fired to that location
    if (search_coord(pieces, player_coord) == True) :
        return "FAIL"
    else :
        #get battleship pieces
        pieces = get_piece_type(game_pieces, battleship())
        if (search_coord (pieces, player_coord) == True) :
            return "HIT"
        else :
            return "MISS"
        
        

#modified coords are stored in dictionaries
#Key is the changed char, value a list of coord objects
#def find_coords ()
board = board_ng(5,5)

change_coords={}
board.print_board(change_coords)

change_coords={
'A': [coords(0,0),coords(0,1),coords(0,2),coords(0,3)]
}
game_pieces.append(game_piece("Hit", "H", [coords(0,0),coords(0,1),coords(0,2),coords(0,3)]))
game_pieces.append(game_piece("Miss","X", [coords(0,4),coords(4,1),coords(4,2),coords(3,3)]))
game_pieces.append(battleship("Mattazor","M",[coords(0,0),coords(0,1),coords(0,2),coords(0,3)], 4))
game_pieces.append(battleship("Lukinator","L", [coords(1,0),coords(1,1),coords(1,2),coords(1,3)], 6))
game_pieces.append(battleship("Graydorn","G", [coords(2,0),coords(2,1),coords(2,2),coords(2,3)], 3))

printed_board = print_player_board(game_pieces, board, type(game_piece()))
for i in range(3):
    assert printed_board[0][i] == 'H', "Check location 0,%d is H" %i

printed_board = print_player_board(game_pieces, board, type(battleship()))
for i in range(4):
    assert printed_board[0][i]=='M',  "Check location 0,%d is M" %i
    assert printed_board[1][i]=='L',  "Check location 1,%d is L" %i
    assert printed_board[2][i]=='G',  "Check location 2,%d is G" %i

print player_shot(game_pieces, coords(0,1))

assert player_shot(game_pieces, coords(0,1)) == "FAIL" , "Previous hit"
#assert player_shot(game_pieces, coords(0,1)) == False, "Expect Repeat Shot"
assert player_shot(game_pieces, coords(4,4)) == "MISS", "Missed location"
#assert player_shot(game_pieces, coords(4,4)) == False
assert player_shot(game_pieces, coords(1,0)) == "HIT", "valid boat location"
#assert player_shot(game_pieces, coords(1,0)) == False
#printed_board = print_player_board(game_pieces, board, type(game_piece(0,'0')))
#Lets make some game pieces and add the to the board
#Typically this information would be made bya  config file


