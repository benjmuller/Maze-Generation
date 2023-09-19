# Maze-Generation

This is a simple implementation of 2D maze generation. The mazes can be generated through various algorithms (Aldous Broder, binary treee, and sidewinder), and visualised through various methods (ascii, png, distances between cells, and shortest path between 2 cells).

## Examples
```
from Grid import Grid
from Aldous_Broder import Aldous_Broder

grid = Grid(8,8)
Aldous_Broder.on(grid)
grid.to_s()
```
<p align="center">
<img src="https://github.com/benjmuller/Maze-Generation/assets/17953240/4fa93540-38bc-425c-88f3-498445fc077e" width=40%>
</p>

```
from Grid import Grid
from Aldous_Broder import Aldous_Broder

grid1 = Grid(20,20)
Aldous_Broder.on(grid1)
grid1.distances([0,0])
grid1.to_png_shortest_path_line([19,19])
```
<p align="center">
<img src="https://github.com/benjmuller/Maze-Generation/assets/17953240/bf2d0ec6-913f-4b59-bf95-1c42ace654b6.png" width=40%>
</p>
