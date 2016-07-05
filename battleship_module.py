class battleship (object):

    def __init__ (self,  name, size, ship_id='F'):
        self.name = name
        self.size = size
        self.hits = 0
        self.coords=[]
        self.ship_id=ship_id

    #If a boat is hit return true if destroyed
    def ship_hit(self):
        self.hits += 1
        if (self.hits >= self.size):
            return True
        else:
            return False
    
