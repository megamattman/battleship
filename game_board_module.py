class game_board(object):
    def __init__(self, rows, cols, empty_char, filled_char):
        #save all the board information
        self.rows = rows
        self.cols = cols
        #dtermine basic grid states
        self.empty_char = empty_char
        self.filled_char = filled_char
        self.filled_spaces = 0
        #board will contain a grid of chars
        self.board = []
        #initialise board with empty chars
        self.init_board()

    #return false if location is out of range
    def check_range (self,row,col) :
        if (row <= self.rows-1 and row >= 0 and col <= self.cols-1 and col >= 0):
            return True
        else:
            print("coords OOR")
            return False

    #Return true if grid location is empty_char else False
    def is_space_empty(self,row,col):
        if (self.check_range(row,col) == True):
            if (self.get_space(row,col) == self.empty_char) :
                return True
            else:
                return False

    #return True if the state of a grid location changed
    #by default does not modify filled count
    def set_space (self,row,col,char, fill_count_mod=0):     
        if (self.check_range(row,col) == True):
            if (self.get_space(row,col) != char):
                self.board[row][col] = char
                self.filled_spaces += fill_count_mod
                return True
            else:
                return False

    #return the state of a coordinate
    def get_space (self, row, col):
        return (self.board[row][col])

    #fill and empty functions for convienance
    def fill_space(self,row,col):
        return (self.set_space(row, col, self.filled_char, 1))
    
    def empty_space (self,row,col):
        return (self.set_space(row,col, self.empty_char, -1))

    #Output board to console
    def print_board(self):
        for col in range(self.cols):
            if (col == 0):
                print "  " + str(col),
            else:
                print col,
        else:
            print
        row_no = 0
        for row in self.board:
            print  chr(ord('A')+row_no) + " " + " ".join(row)
            row_no += 1
        else :
            print
        
    def init_board(self):
        self.board=[]
        for i in range(self.rows):
            self.board.append([self.empty_char]*self.cols)  
