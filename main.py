from array2d import array2d
from Architect2 import SimpleShapes


grid = array2d(20, 10, 0)

SimpleShapes.draw_rectangle(grid, 1, 5, 5, 2, 3)

grid.draw(2)

grid = array2d(20, 10, 0)

SimpleShapes.draw_circle(grid, 1, 5, 5, 2)

grid.draw(2)