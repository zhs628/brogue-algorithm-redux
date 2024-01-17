from .DataEntities import Grid


class ShapeDrawer:
    @classmethod
    def _draw_shape(cls, grid: Grid, value, shape:'Shape') -> Grid:
        shape.draw_to_grid(grid, value)

    @classmethod
    def draw_circle(cls, grid: Grid, value, center_x: int, center_y: int, radius) -> Grid:
        Circle(radius, center_x, center_y).draw_to_grid(grid, value)



class Shape:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def draw_to_grid(self, grid: Grid) -> Grid:
        pass



class Circle(Shape):
    def __init__(self, radius: int, *args):
        # 继承自父类的x,y是圆心
        super(Circle, self).__init__(*args)
        self.radius = radius
    
    def draw_to_grid(self, grid: Grid, value) -> Grid:
        # 逐行扫描圆的外接正方形, 并对距离圆心为 sqrt( r^2 + r) 的点填充为 values
        radius = self.radius
        x_center = self.x
        y_center = self.y
        n_cols, n_rows = grid.shape()
        for x in range(max(0, x_center - radius - 1), min(n_cols, x_center + radius)+1):
            for y in range(max(0, y_center - radius - 1), min(n_rows, y_center + radius)+1):
                if (x-x_center)*(x-x_center) + (y-y_center)*(y-y_center) < radius * radius + radius:
                    if grid.is_valid(x,y):
                        grid[x, y] = value