from random import random, randint

class Sidewinder:
    
    def on(grid):
        for row in grid.each_row():
            last_north = 0
            for cell in row:
                if cell.is_allowed_direction("north") and cell.is_allowed_direction("east"):
                    if random() > 0.5:
                        north_cell_index = randint(last_north, cell.get_column())
                        row[north_cell_index].create_link("north")
                        last_north = cell.get_column() + 1
                    else:
                        cell.create_link("east")
                else:
                    if cell.is_allowed_direction("north"):
                        north_cell_index = randint(last_north, cell.get_column())
                        row[north_cell_index].create_link("north")
                    else:
                        cell.create_link("east")