from array2d import array2d
from Architect2 import SimpleShapes, Rooms, Level, const
import test_tools


# test_tools.test_all_rooms(
#     selected_func_name=["brogue_designRandomRoom"],
#     test_count=100,
#     selection_ratio=1,
#     grid_width_range=(Rooms.DUNGEON_WIDTH, Rooms.DUNGEON_WIDTH),
#     grid_height_range=(Rooms.DUNGEON_HEIGHT, Rooms.DUNGEON_HEIGHT),
#     ignore_assertion_error=False,
#     mulity_process_count=16,
#     print_exception=True
# )



grid = array2d(const.DUNGEON_WIDTH, const.DUNGEON_HEIGHT, None)
Level.brogue_carveDungeon(grid, 5, 10)

# 给grid进行描边，描边数值为6
neighbors = grid.count_neighbors(1)
for i in range(grid.width):
    for j in range(grid.height):
        if grid[i, j] == 0 and neighbors[i, j] > 0:
            grid[i, j] = 6

test_tools.print_grid(grid)