# 用以生成各类房间的地皮
import random
from .ShapeDrawer import ShapeDrawer

class RoomDesigner:
    BROGUE_MODE = 'brogue_mode'
    def __init__(self, mode) -> None:
        self.mode = mode
    
    def design_circular_room(self, grid) -> None:
        
        def brogue_designCircularRoom(grid):
            if random.random() < 0.5:
                radius = random.randint(4, 10)
            else:
                radius = random.randint(2, 4)
                
            grid.map1d(lambda _,__:0)
            
            ShapeDrawer.draw_circle(grid, value=1, center_x=grid.width // 2, center_y=grid.height // 2, radius=radius)
            
            if radius > 6 and random.random() < 0.5:
                ShapeDrawer.draw_circle(grid, value=0, center_x=grid.width // 2, center_y=grid.height // 2, radius=random.randint(3, random.randint(2, 4)))

        if self.mode == RoomDesigner.BROGUE_MODE:
            brogue_designCircularRoom(grid)