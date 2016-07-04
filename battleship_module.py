class battleship (object):

    def __init__ (self,  name, size, row=0, col=0, facing='n', placed=0):
        self.name = name
        self.size = size
        self.row = row
        self.col = col
        self.placed = placed
        self.facing = facing
        self.destroyed = False
        self.hits = 0

    #If a boat is hit return true if destroyed
    def ship_hit(self):
        self.hits += 1
        if (self.hits >= self.size):
            self.destroyed = True
            print ("Your sunk my %s" %self.name)
            return True
        else:
            return False
    
