from Architect2 import Rooms
from array2d import array2d

from line_profiler import LineProfiler
profiler = LineProfiler()

grid = array2d(Rooms.DUNGEON_WIDTH, Rooms.DUNGEON_HEIGHT)

profiler.add_function(Rooms._brogue_designCavern)
profiler.add_function(Rooms._brogue_createBlobOnGrid)
profiler.add_function(Rooms.insert_room_to_grid)

profiler.runcall(Rooms.brogue_design_cave, grid)

profiler.print_stats()
