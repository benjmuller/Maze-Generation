from random import randint

class Aldous_Broder:
    
    def on(grid):
        cell = grid.random_cell()
        unvisited = grid.size() - 1
        visited = [cell]
        while unvisited > 0:
            rand_int = randint(0, len(cell.allowed_directions) - 1)
            direction = cell.allowed_directions[rand_int]
            cell = cell.get_direction(direction)
            if cell not in visited:
                cell.create_link(cell.get_opposite_direction(direction))
                visited.append(cell)
                unvisited -= 1
                            
            