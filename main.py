from array2d import array2d
from Architect2 import SimpleShapes, Rooms
import test_tools


test_tools.test_all_rooms(
    selected_func_name=["brogue_designRandomRoom"],
    test_count=100,
    selection_ratio=1,
    grid_width_range=(Rooms.DUNGEON_WIDTH, Rooms.DUNGEON_WIDTH),
    grid_height_range=(Rooms.DUNGEON_HEIGHT, Rooms.DUNGEON_HEIGHT),
    ignore_assertion_error=False,
    mulity_process_count=16,
    print_exception=True
)