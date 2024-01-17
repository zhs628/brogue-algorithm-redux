import Architect
from array2d import array2d

grid = Architect.Grid(20,10,0)
grid = grid.map2d(lambda y,x,element: element if x != y else 1)
grid = grid.map2d(lambda y,x,element: element if x-1 != y else 2)
grid = grid.map2d(lambda y,x,element: element if x+1 != y else 3)
print(grid)
grid.show()
grid.transpose().show()
grid[3:15, 5:9].show()

print(grid[3, 5])
print(grid[3, 5:9])
print(grid[3, :])
print(grid[3:15, 5])
print(grid[:, 5])
print(grid[3:15, 5:9].shape())

grid = Architect.Grid(20,10,0)
value = 1
Architect.ShapeDrawer.draw_circle(grid, value, 10, 5, 5)
grid.show()

