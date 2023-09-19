from random import random

class Binary_Tree:
    
    def on(grid):
        for cell in grid.each_cell():
            if cell.is_allowed_direction("north") and cell.is_allowed_direction("east"):
                if random() > 0.5:
                    cell.create_link("east")
                else:
                    cell.create_link("north")
            else:
                if cell.is_allowed_direction("north"):
                    cell.create_link("north")
                else:
                    cell.create_link("east")