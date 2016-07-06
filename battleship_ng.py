#class to hold row/col
class coords (object):
    def __init__ (self, row = 0, col = O) :
        self.row = row
        self.col = col

class player_piece (object):
    def __init__ (self, row, col) :
        self.row = row
        self.col = col

class board_ng (object):
    def __init__ (self, rows, cols, empty_char = '0'):
        self.rows = rows
        self.cols = cols
        self.empty_char = empty_char

    #Take a list of non-empty coords
    #Exoect this to be a dictionary with 
    #Replacement char, coords
    def print_board(self, change_coords):
        output_grid=[]
        #Create empty grid
        for i in range(self.rows):
            output_grid.append([self.empty_char]*self.cols)
        #The key is a char to place into the output grid
        for key in change_coords:
            for i in range(len(change_coords[key])):
                coords = change_coords[key][i]
                print str(coords.row) + " " + str(coords.col) + " " + key
                output_grid[coords.row][coords.col] = key

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
        return True
#modified coords are stored in dictionaries
#Key is the changed char, value a list of coord objects
def find_coords ()
board = board_ng(5,5)

change_coords={}
board.print_board(change_coords)

change_coords={
'A': [coords(0,0),coords(0,1),coords(0,2),coords(0,3)]
}
print change_coords['A'][0].row
board.print_board(change_coords)
    
if coords(0,0) in change_coords['A'] :
    print ("Found 0,0 in dictionary held list")
else:
    print ("Didin't find it lol!")

