
from array2d import array2d


def draw_circle(grid: array2d, value, center_x: int, center_y: int, radius) -> None:
    # 逐行扫描圆的外接正方形, 并对距离圆心为 sqrt( r^2 + r) 的点填充为 value

    
    x_scan_range = range(max(0, center_x - radius - 1), min(grid.width, center_x + radius)+1)
    y_scan_range = range(max(0, center_y - radius - 1), min(grid.height, grid.height + radius)+1)
    
    for x in x_scan_range:
        for y in y_scan_range:
            if not grid.is_valid(x,y):
                continue
            is_in_circle = (x-center_x)*(x-center_x) + (y-center_y)*(y-center_y) < radius * radius + radius
            if is_in_circle:
                grid[x, y] = value




def draw_rectangle(grid: array2d, value, conor_x: int, conor_y: int, width: int, height: int) -> None:
    x_scan_range = range(conor_x, conor_x+width)
    y_scan_range = range(conor_y, conor_y+height)
    
    for x in x_scan_range:
        for y in y_scan_range:
            if not grid.is_valid(x,y):
                continue
            grid[x, y] = value

