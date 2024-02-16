from array2d import array2d
from collections import deque

def count_connected_components(grid: array2d, value) -> int:
    """计算图的连通分量个数"""
    visited = array2d(grid.width, grid.height, default=False)
    queue = deque()
    count = 0
    DIRS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for y in range(grid.height):
        for x in range(grid.width):
            if visited[x, y] or grid[x, y] != value:
                continue
            count += 1
            queue.append((x, y))
            visited[x, y] = True
            while queue:
                cx, cy = queue.popleft()
                for dx, dy in DIRS_4:
                    nx, ny = cx+dx, cy+dy
                    if grid.is_valid(nx, ny) and not visited[nx, ny] and grid[nx, ny] == value:
                        queue.append((nx, ny))
                        visited[nx, ny] = True
    return count

def trim_bounding_rect(grid: array2d, value):
    x, y, w, h = grid.find_bounding_rect(value)
    return grid[x:x+w, y:y+h]