from .DataEntities import Grid


class ShapeDrawer:
    '''
    调用方法将生成新的grid, 而不是在原来的grid上改动
    '''
    @classmethod
    def _draw_shape(cls, grid: Grid, value, shape:'Shape') -> Grid:
        shape.draw_to_grid(grid, value)

    @classmethod
    def draw_circle(cls, grid: Grid, value, center_x: int, center_y: int, radius) -> None:
        Circle(center_x, center_y, radius).draw_to_grid(grid, value)

    @classmethod
    def draw_rectangle(cls, grid: Grid, value, conor_x: int, conor_y: int, width: int, height: int) -> None:
        Rectangle(conor_x, conor_y, width, height).draw_to_grid(grid, value)



class Shape:
    def __init__(self, x, y, *args) -> None:
        self.x = x
        self.y = y
        self._child_init(*args)
        
    def _child_init(self, *args) -> None:
        raise NotImplementedError()
    
    def draw_to_grid(self, grid: Grid) -> Grid:
        raise NotImplementedError()



class Circle(Shape):
    
    def _child_init(self, radius) -> None:
        # 继承自父类的x,y是圆心
        self.radius = radius
    
    def draw_to_grid(self, grid: Grid, value) -> None:
        # 逐行扫描圆的外接正方形, 并对距离圆心为 sqrt( r^2 + r) 的点填充为 value
        radius = self.radius
        x_center, y_center = self.x, self.y
        n_cols, n_rows = grid.shape()
        
        x_scan_range = range(max(0, x_center - radius - 1), min(n_cols, x_center + radius)+1)
        y_scan_range = range(max(0, y_center - radius - 1), min(n_rows, y_center + radius)+1)
        
        def draw_point_if_in_circle(x,y,old_value):
            if (x-x_center)*(x-x_center) + (y-y_center)*(y-y_center) < radius * radius + radius:
                return value
            return old_value
        
        for x in x_scan_range:
            for y in y_scan_range:
                if not grid.is_valid(x,y):
                    continue
                is_in_circle = (x-x_center)*(x-x_center) + (y-y_center)*(y-y_center) < radius * radius + radius
                if is_in_circle:
                    grid[x, y] = value



class Rectangle(Shape):
    def _child_init(self, width, height) -> None:
        # 继承自父类的x,y是左上角
        self.width = width
        self.height = height
    
    def draw_to_grid(self, grid: Grid, value) -> None:
        x_scan_range = range(self.x, self.x+self.width)
        y_scan_range = range(self.y, self.y+self.height)
        
        for x in x_scan_range:
            for y in y_scan_range:
                if not grid.is_valid(x,y):
                    continue
                grid[x, y] = value


