'''
生成整层
'''
from array2d import array2d
import random
from . import SimpleShapes
import test_tools
import random
from .const import *
from . import Rooms

    
    
    
    
def generate_room_frequencies(depth_level, amulet_level, room_frequencies):
    """
    生成并返回房间生成概率列表
    
    Args:
        depth_level: int, 地牢深度
        amulet_level: int, level on which the amulet appears (used in signed arithmetic)
        room_frequencies: list, 房间生成概率列表
    """
    interpreted_depth = 100 * (depth_level - 1) / amulet_level if depth_level > 1 else 0
    descent_percent = 100 if interpreted_depth > 100 else interpreted_depth
    room_freq = room_frequencies[:]

    room_freq[0] += 20 * (100 - descent_percent) / 100
    room_freq[1] += 10 * (100 - descent_percent) / 100
    room_freq[3] +=  7 * (100 - descent_percent) / 100
    room_freq[5] += 10 * descent_percent / 100
    
    return room_freq

def generate_corridor_chance(depth_level, amulet_level, corridor_chance):
    """返回生成走廊的概率"""
    interpreted_depth = 100 * (depth_level - 1) / amulet_level if depth_level > 1 else 0
    descent_percent = 100 if interpreted_depth > 100 else interpreted_depth

    # Update corridor chance
    return corridor_chance + 80 * (100 - descent_percent) / 100
