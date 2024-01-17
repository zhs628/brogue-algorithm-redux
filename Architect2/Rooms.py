from array2d import array2d
import random
import SimpleShapes


def brogue_designCircularRoom(grid):
    if random.random() < 0.5:
        radius = random.randint(4, 10)
    else:
        radius = random.randint(2, 4)
        
    grid.map1d(lambda _,__:0)
    
    SimpleShapes.draw_circle(grid, value=1, center_x=grid.width // 2, center_y=grid.height // 2, radius=radius)
    
    if radius > 6 and random.random() < 0.5:
        SimpleShapes.draw_circle(grid, value=0, center_x=grid.width // 2, center_y=grid.height // 2, radius=random.randint(3, random.randint(2, 4)))