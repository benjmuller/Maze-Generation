import numpy as np

class Cell:
    
    def __init__(self, row, column):
        
        self.row = row
        self.column = column
        
        self.allowed_directions = np.array(["north", "south", "east", "west"])
        
        self.links = {}
        
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        
        self.distance = None

        
        
    def create_link(self, direction):
        """Creates a link between a Cell in the given cardinal direction"""
        if self.is_allowed_direction(direction):
            if self.get_direction(direction) != None:
                self.links[direction] = True
                self.get_direction(direction).links[self.get_opposite_direction(direction)] = True
    
    def create_links(self, directions):
        """Creates links between Cells in the given cardinal directions"""
        for direction in directions:
            if self.is_allowed_direction(direction):
                if self.get_direction(direction) != None:
                    self.links[direction] = True
                    self.get_direction(direction).links[self.get_opposite_direction(direction)] = True
    
    def delete_link(self, direction):
        """Deletes a link between a Cell in the given cardinal direction"""
        if direction in self.links.keys():
            del(self.links[direction])
            del(self.get_direction(direction).links[self.get_opposite_direction(direction)])
        
    def delete_links(self, directions):
        """Creates links between Cells in the given cardinal directions"""
        for direction in directions:
            if direction in self.links.keys():
                del(self.links[direction])
                del(self.get_direction(direction).links[self.get_opposite_direction(direction)])
                
    def get_opposite_direction(self, direction):
        """Returns the string of the opposite cardinal direction"""
        opposite_direction = {
            "north":"south",
            "south":"north",
            "east":"west",
            "west":"east"
            }
        return opposite_direction[direction]
                
    def delete_all_links(self):
        """Deletes all adjacent links to the cell"""
        self.links.clear()
        del(self.north.links["south"])
        del(self.south.links["north"])
        del(self.west.links["east"])
        del(self.east.links["west"])
    
    def is_allowed_direction(self, direction):
        """Checks if string is valid direction"""
        if self.get_direction(direction) == None:
            return False
        else:
            return True
    
    def get_direction(self, direction):
        directions = {
            "north":0,
            "south":1,
            "east":2,
            "west":3
            }
        if directions[direction] == 0:
            return self.get_north()
        elif directions[direction] == 1:
            return self.get_south()
        elif directions[direction] == 2:
            return self.get_east()
        elif directions[direction] == 3:
            return self.get_west()
    
    def is_linked(self, direction):
        """Returns bool if directions are linked"""
        if direction in self.links.keys():
            return True
        else:
            return False
    
    def get_links(self):
        return self.links
    
    def get_row(self):
        return self.row
    
    def get_column(self):
        return self.column
    
    def get_north(self):
        return self.north
    
    def get_south(self):
        return self.south
    
    def get_west(self):
        return self.west
    
    def get_east(self):
        return self.east
    
    def get_distance(self):
        return self.distance
    
    def is_north(self, cell):
        if self.column == cell.get_column() and self.row - cell.get_row() == -1:
            return True
        else:
            return False
    
    def is_south(self, cell):
        if self.column == cell.get_column() and self.row - cell.get_row() == 1:
            return True
        else:
            return False
        
    def is_east(self, cell):
        if self.row == cell.get_row() and self.column - cell.get_column() == -1:
            return True
        else:
            return False
        
    def is_west(self, cell):
        if self.row == cell.get_row() and self.column - cell.get_column() == 1:
            return True
        else:
            return False
    
    