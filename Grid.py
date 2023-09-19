from Cell import Cell
import numpy as np
import random
from PIL import Image, ImageDraw, ImageFont

class Grid:
    
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = self.make_grid()
        self.configure_cells()
        
        
    def make_grid(self):
        grid = np.empty((self.rows,self.columns), dtype=Cell)
        for i, row in enumerate(grid):
            for j, column in enumerate(row):
                grid[i,j] = Cell(i,j)
        return grid
    
    def configure_cells(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.grid[i,j].north = self.grid[i-1,j] if i-1 >= 0 else None
                self.grid[i,j].south = self.grid[i+1,j] if i+1 < self.rows else None
                self.grid[i,j].west = self.grid[i,j-1] if j-1 >= 0 else None
                self.grid[i,j].east = self.grid[i,j+1] if j+1 < self.columns else None
        
        for cell in self.each_cell():
            self.allowed_directions(cell)
                
                
    def to_s(self):
        output = "+" + "---+" * self.columns + "\n"
        for row in self.each_row():
            top = "|"
            bottom = "+"
            for cell in row:
                body = "   "
                east_boundary = " " if cell.is_linked("east") else "|"
                south_boundary = "   " if cell.is_linked("south") else "---"
                corner = "+"
                top += body + east_boundary
                bottom += south_boundary + corner
            output += top + "\n"
            output += bottom + "\n"
        print(output)
    
    def random_cell(self):
        row = random.randint(0, self.rows - 1)
        col = random.randint(0, self.columns - 1)
        return self.grid[row,col]
    
    def distances(self, root_coords):
        root = self.get_cell(root_coords)
        root.distance = 0
        distance = 1
        frontier = np.asarray([root])
        while len(frontier) != 0:
            new_frontier = np.array([])
            for front_cell in frontier:
                for link in front_cell.get_links().keys():
                    adjacent_link = front_cell.get_direction(link)
                    if adjacent_link.distance == None:
                        adjacent_link.distance = distance
                        new_frontier = np.append(new_frontier, adjacent_link)
                        
            frontier = new_frontier
            distance += 1
    
    def path_to(self, goal):
        current = goal
        path = np.array([goal])
        while current.get_distance() != 0:
            for link in current.get_links().keys():
                adjacent_link = current.get_direction(link)
                if adjacent_link.get_distance() == current.get_distance() - 1:
                    current = adjacent_link
                    path = np.insert(path, 0, adjacent_link)
                    break
        return path
                    
    def to_png(self):
        scalar = int(500 * 2 / (self.rows + self.columns))
        img_height = self.rows * scalar
        img_width = self.columns * scalar
        img = Image.new('RGB', (img_width + 1, img_height + 1), color = (73, 109, 137))
        draw = ImageDraw.Draw(img)
        draw.line([(0,0),(img_width,0)],fill="white",width=0)
        draw.line([(0,0),(0,img_height)],fill="white",width=0)
        for cell in self.each_cell():
            row = cell.get_row() + 1
            column = cell.get_column() + 1
            if "east" not in cell.get_links().keys():
                draw.line([(column * scalar,(row - 1) * scalar),(column * scalar,row * scalar)],fill="white",width=0)
            if "south" not in cell.get_links().keys():
                draw.line([((column - 1) * scalar,row * scalar),(column* scalar,row * scalar)],fill="white",width=0)
                
        return img, draw, scalar, img_height, img_width
    
    def to_png_print(self):
         img = self.to_png()[0]
         img.show()
    
    def to_png_distances(self):
        img, draw, scalar, img_height, img_width = self.to_png()
        column_count = 2 * self.columns
        column_ratio = (img_width + 1) / column_count
        row_count = 2 * self.rows
        row_ratio = (img_height + 1) / row_count
        fnt = ImageFont.truetype("arial.ttf", int(row_ratio / 3.5))
        for cell in self.each_cell():
            draw.text(((1 + 2 * cell.get_column()) * column_ratio,(1 + 2 * cell.get_row()) * row_ratio),str(cell.get_distance()),(255,255,255),font=fnt)
        img.show()
    
    def to_png_shortest_path(self,end_coords):
        position = self.get_cell(end_coords)
        img, draw, scalar, img_height, img_width = self.to_png()
        column_count = 2 * self.columns
        column_ratio = (img_width + 1) / column_count
        row_count = 2 * self.rows
        row_ratio = (img_height + 1) / row_count
        fnt = ImageFont.truetype("arial.ttf", int(row_ratio / 3.5))
        for cell in self.path_to(position):
            draw.text(((1 + 2 * cell.get_column()) * column_ratio,(1 + 2 * cell.get_row()) * row_ratio),str(cell.get_distance()),(255,255,255),font=fnt)
        img.show()
        
    def to_png_shortest_path_line(self,end_coords):
        position = self.get_cell(end_coords)
        img, draw, scalar, img_height, img_width = self.to_png()
        column_count = 2 * self.columns
        column_ratio = (img_width + 1) / column_count
        row_count = 2 * self.rows
        row_ratio = (img_height + 1) / row_count
        path = self.path_to(position)
        i = 0
        for cell in path[:-1]:
            if cell.is_north(path[i+1]):
                draw.line([((1 + 2 * cell.get_column()) * column_ratio,(1 + 2 * cell.get_row()) * row_ratio),
                           ((1 + 2 * cell.get_column()) * column_ratio,(3 + 2 * cell.get_row()) * row_ratio)],
                          fill="red",width=0)
            elif cell.is_south(path[i+1]):
                draw.line([((1 + 2 * cell.get_column()) * column_ratio,(-1 + 2 * cell.get_row()) * row_ratio),
                           ((1 + 2 * cell.get_column()) * column_ratio,(1 + 2 * cell.get_row()) * row_ratio)],
                          fill="red",width=0)
            elif cell.is_east(path[i+1]):
                draw.line([((1 + 2 * cell.get_column()) * column_ratio,(1 + 2 * cell.get_row()) * row_ratio),
                           ((3 + 2 * cell.get_column()) * column_ratio,(1 + 2 * cell.get_row()) * row_ratio)],
                          fill="red",width=0)
            else:
                draw.line([((1 + 2 * cell.get_column()) * column_ratio,(1 + 2 * cell.get_row()) * row_ratio),
                           ((-1 + 2 * cell.get_column()) * column_ratio,(1 + 2 * cell.get_row()) * row_ratio)],
                          fill="red",width=0)
            i += 1
        
        img.show()
        
    def allowed_directions(self, cell):
        if cell.get_row() == 0:
            cell.allowed_directions = cell.allowed_directions[cell.allowed_directions != "north"]
        if cell.get_row() == self.rows - 1:
            cell.allowed_directions = cell.allowed_directions[cell.allowed_directions != "south"]
        if cell.get_column() == 0:
            cell.allowed_directions = cell.allowed_directions[cell.allowed_directions != "west"]
        if cell.get_column() == self.columns - 1:
            cell.allowed_directions = cell.allowed_directions[cell.allowed_directions != "east"]
    
    def each_row(self):
        for row in self.grid:
            yield row
            
    def each_cell(self):
        for row in self.grid:
            for cell in row:
                yield cell
    
    def size(self):
        return self.rows * self.columns
        
    def get_grid(self):
        return self.grid
    
    def get_cell(self, coord):
        return self.grid[coord[0],coord[1]]
        