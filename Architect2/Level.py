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


def room_fits_at(grid: array2d[int], room_grid: array2d[int], delta_x:int, delta_y:int):
    '''
    判断 room_grid 中的房间在被映射到 grid 中后, 是否不与其他房间重叠并距离边界大于一格的距离
    映射规则: 设(x,y)是房间格子在 room_grid 中的位置, 那么它被映射到grid中的位置是(x+delta_x, y+delta_y)
    '''
    for room_x in range(room_grid.width):
        for room_y in range(room_grid.height):
            
            # 我们只需要挑出属于房间的格子并进行判断, 以保证房间在被移动到 grid 时是完整的并距离边界保持一格的距离
            if not room_grid[room_x,room_y] == ONE:
                continue
            
            grid_x = room_x + delta_x
            grid_y = room_y + delta_y
            
            neighboor_delta_list = [
                [-1,-1], [0,-1], [1,-1],
                [-1,0], [0,0], [1,0],
                [-1,1], [0,1], [1,1]
            ]
            
            # 判断房间格子附近有没有地图边界
            for neighboor_delta in neighboor_delta_list:
                neighboor_x = grid_x + neighboor_delta[0]
                neighboor_y = grid_y + neighboor_delta[1]
                
                # 但凡找到一个附近有地图边界的房间格子, 那么就不符合本函数的要求
                if not grid.is_valid(neighboor_x,neighboor_y):
                    return False
                
                # 如果发现和其他房间重叠, 那么也不符合本函数的要求
                if not grid[neighboor_x,neighboor_y] == ZERO:
                    return False

    
    return True
    

def brogue_attachRooms(grid:array2d[int], room_profile:DungeonProfile, attempt_count:int, max_count:int):
    
    attemped_time = 0
    built_room_num = 0
    # 不断尝试生成房间, 直到达到房间数量上限或尝试次数上限
    while attemped_time < attempt_count and built_room_num < max_count:
        
        # 生成一个房间并暂存在 roomMap 中
        roomMap = array2d(DUNGEON_WIDTH, DUNGEON_HEIGHT, 0)
        has_hallway = attemped_time <= attempt_count-5  and  random.random() < room_profile.corridor_chance
        #    door_positions 是一个 list[list[int,2], 4], 其中每个元素是 [x,y], 表示朝一个方向上打开的门的位置, 门打开的方向取决于[x,y]在 door_positions 中的位置
        door_positions = Rooms.brogue_designRandomRoom(
            roomMap, 
            room_type_frequencies = room_profile.room_frequencies, 
            has_hallway=has_hallway,
            has_doors=True
            )
        
        random_sequence_for_grid = [ i for i in range(grid.width * grid.height)]
        random.shuffle(random_sequence_for_grid)
        # 将房间在地图上滑动，直到与墙壁对齐
        for i in random_sequence_for_grid:
            # 无序遍历grid, 此处的(x,y)指的是两个房间相互接壤的门的位置
            x = random_sequence_for_grid[i] // grid.height
            y = random_sequence_for_grid[i] % grid.height
            
            # 关于 direction_index 的取值说明:
            #  -1: (X,y)无法生成门
            #   0: 可以生成门, 将朝向上     
            #   1: 可以生成门, 将朝向下     
            #   2: 可以生成门, 将朝向左     
            #   3: 可以生成门, 将朝向右
            direction_index = Rooms.brogue_directionOfDoorSite(grid, x, y)
            if direction_index == -1:
                # 确保 grid(x,y) 可以生成门
                continue
            
            opposite_direction_index = {0:1, 1:0, 2:3, 3:2}[direction_index]
            opposite_door_position = door_positions[opposite_direction_index]
            if opposite_door_position == [-1, -1]:
                # 确保新的房间的门的对面的位置可以生成门
                continue
            
            delta_x_for_opposite_door = x-opposite_door_position[0]
            delta_y_for_opposite_door = y-opposite_door_position[1]
            if not room_fits_at(grid, roomMap, delta_x_for_opposite_door, delta_y_for_opposite_door):
                continue


            # 满足上述条件, 则将暂存在 roomMap 中的房间插入到地图
            Rooms.insert_room_to_grid(
                grid, 
                roomMap, 
                delta_x_for_opposite_door, delta_y_for_opposite_door, 
                opposite_door_position[0], opposite_door_position[1]
                )


            # 并将位置(x,y)标记为房间的门, 使用2表示门
            grid[x,y] = 2
            built_room_num += 1
            
            # 已经经被放置了房间, 那么就不想需要继续搜索适合放置该房间的位置了
            break

        test_tools.print_grid_debug(grid)
        
        # 总尝试次数+1
        attemped_time += 1




def brogue_carveDungeon(grid:array2d[int], depth_level:int, amulet_level:int):
    
    basic_room_profile = DungeonProfileForBasicRooms(depth_level, amulet_level)
    first_room_profile = DungeonProfileForFirstRooms(depth_level, amulet_level)
    
    # 生成第一个房间
    Rooms.brogue_designRandomRoom(
        grid, 
        room_type_frequencies = first_room_profile.room_frequencies, 
        has_doors=False, 
        has_hallway=False
        )
    
    test_tools.print_grid_debug(grid)

    
    # 接着不断生成其余的房间
    brogue_attachRooms(grid, basic_room_profile, ATTACH_ROOMS_ATTEMPT_COUNT, ATTACH_ROOMS_MAX_COUNT)