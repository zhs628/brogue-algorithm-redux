from array2d import array2d
from Architect2 import SimpleShapes, Rooms
import test_tools


# SimpleShapes

grid = array2d(20, 10, default=0)

SimpleShapes.draw_rectangle(grid, 1, 5, 5, 2, 3)

test_tools.print_grid(grid)

grid = array2d(20, 10, default=0)

SimpleShapes.draw_circle(grid, 1, 5, 5, 2)

test_tools.print_grid(grid)

# Rooms
grid = array2d(30, 30, default=0)
SimpleShapes.draw_circle(grid, 1, 15, 15, 4)
size = Rooms.flood_fill(grid, 2, 1, 15, 15)
print("fill_size =" ,size)
print(grid)
assert size == 61

grid = array2d(41, 30, default=0)

Rooms.brogue_designCircularRoom(grid)

test_tools.print_grid(grid)

Rooms.brogue_designCrossRoom(grid)

test_tools.print_grid(grid)

Rooms.brogue_designSymmetricalCrossRoom(grid)

test_tools.print_grid(grid)

Rooms.brogue_designChunkyRoom(grid)

test_tools.print_grid(grid)

Rooms.brogue_designSmallRoom(grid)

test_tools.print_grid(grid)

print(Rooms._brogue_createBlobOnGrid(grid, 3, 12, 4, 8))
test_tools.print_grid(grid)

# check functions' accuracy in Rooms
test_tools.test_all_rooms(
    # selected_func_name=["brogue_designCrossRoom", "brogue_designChunkyRoom"],
    test_count=10,
    selection_ratio=0.3,
    grid_width_range=(0, 50),
    grid_height_range=(0, 50),
    ignore_assertion_error=True,
)
