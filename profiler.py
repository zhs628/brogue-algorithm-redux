from array2d import array2d

from dungeon.brogue.levels import brogue_carveDungeon, brogue_attachRooms, try_map_room_to_grid_
from dungeon.brogue.rooms import brogue_designRandomRoom
from dungeon.brogue import const
from dungeon import test_tools

from line_profiler import LineProfiler

grid = array2d(const.DUNGEON_WIDTH, const.DUNGEON_HEIGHT, default=None)

lp = LineProfiler()

lp.add_function(brogue_carveDungeon)
lp.add_function(brogue_attachRooms)
lp.add_function(try_map_room_to_grid_)

lp.runcall(brogue_carveDungeon, grid, 5, 10)

test_tools.print_grid(grid)

lp.print_stats()