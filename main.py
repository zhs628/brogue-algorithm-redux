from array2d import array2d

from dungeon.brogue.levels import brogue_carveDungeon
from dungeon.brogue import const
from dungeon import test_tools

grid = array2d(const.DUNGEON_WIDTH, const.DUNGEON_HEIGHT, default=None)
brogue_carveDungeon(grid, 5, 10)

test_tools.print_grid(grid)