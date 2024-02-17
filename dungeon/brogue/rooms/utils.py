from array2d import array2d
import random

from dungeon.algorithm.grid import count_connected_components
from dungeon.brogue.const import *

'''
utils.py 包含了生成房间的小部分相关算法
'''

# 在本文件中, 完全复刻自brogue的算法将使用 "brogue_<brogue中该函数的原名>" 命名
def clamp(x, a, b):
    if a > b: a, b = b, a
    if x < a: return a
    if x > b: return b
    return x


"""
. . . .
. 1 1 .
. 1 . .
. . . .
"""



def insert_room_to_grid(grid: array2d, room_grid: array2d, delta_x: int, delta_y: int, x: int, y: int):
    '''
    复制`room_grid`的一个连通的图案到`grid`中, 在`room_grid`中的点`(x, y)`将通过`(x + delta_x, y + delta_y)`映射到`grid`中
    设置`(x, y)`来选择`room_grid`中将被复制的图案的内点或相邻点
    '''
    # room_grid有且仅有一个连通分量
    assert count_connected_components(room_grid, ONE) == 1
    grid[x+delta_x, y+delta_y] = ONE
    for dir_x, dir_y in DIRS_4:
        # room_grid中的下一个点
        next_x = x + dir_x
        next_y = y + dir_y

        # 判断下一个点是否在room_grid中，且为房间格子
        if room_grid.get(next_x, next_y) != ONE:
            continue

        # grid中的目标点
        target_x = next_x + delta_x
        target_y = next_y + delta_y

        # 目标点必须是空的合法点
        if grid.get(target_x, target_y) == ZERO:
            insert_room_to_grid(grid, room_grid, delta_x, delta_y, next_x, next_y)


"""
? 1 ?
. 2 .
? 1 ?
"""

# 下面是生成门的逻辑---------------------------------------------------
def brogue_directionOfDoorSite(grid:array2d[int], door_x:int, door_y:int):
    '''
    以(door_X, door_Y)为中心, 搜索邻近的4个格子是否有且仅有一个符合"能够让位于(door_x, door_y)的门打开"条件
    
    返回值: Int 
        -1: (door_X,door_y)附近无法生成门
        0:  可以生成门, 将朝向上
        1:  可以生成门, 将朝向下
        2:  可以生成门, 将朝向左
        3:  可以生成门, 将朝向右
    
    我们希望生成于(door_x,door_y)的门能够不被阻挡地向一个空的方向打开, 并保证门的背后就是房间, 还需保证一个门仅有唯一的可选打开方向
    
    本算法在理论上, 只有这一种情况是可以生成门的:  
                            ? 1 ?
                            . 2 .   问号可以是任意格子,加号是(door_X,door_Y), 实心方块是房间格子(值为1), 此时门的朝向为(door_x, door_y)的下方, 函数将返回1
    下面的情况都无法生成门:
        1. 2个及以上邻边都有打开门的条件:
              . 1 1
              . 2 1   此处因为下侧和左侧都符合打开门的条件, 因此这一格不能生成门, 必须仅有一侧能够打开门, 才符合最终条件
              . . .
        2. 门的打开方向是地图边界:
            \\| . 1
            \\| 2 1 <-- 此处因为其对称点在地图边界外, 因此不能生成门
            \\| . 1
    
    '''
    
    # 门不能生成在房间内，而至少是房间边缘的外侧一格
    if grid[door_x, door_y] == ONE:
        return -1 # no direction
    
    edge_neighbor_pos_list = [
        (door_x, door_y - 1),       # 上
        (door_x, door_y + 1),       # 下
        (door_x - 1, door_y),       # 左
        (door_x + 1, door_y),       # 右
    ]
    
    selected_direction_index = -1
    for direction in [0, 1, 2, 3]:
        neighbor_x, neighbor_y = edge_neighbor_pos_list[direction]
        # TODO: grid[neighbor_x, neighbor_y] 需要满足什么条件？
        if not grid.is_valid(neighbor_x, neighbor_y):
            continue
        # 以(door_x, door_y)为中心, 计算其对称点的坐标
        opposite_x = door_x - (neighbor_x - door_x)
        opposite_y = door_y - (neighbor_y - door_y)
        # 如果对称点不是房间格子, 则不能打开门, 因此跳过
        if grid.get(opposite_x, opposite_y) != ONE:
            continue
        # 发现不止一处可以打开门的方向, 则无法生成门
        if selected_direction_index != -1:
            return -1 # no direction
        selected_direction_index = direction
    return selected_direction_index

def brogue_chooseRandomDoorSites(grid: array2d[int]):
    '''
    #### 对于上下左右四个方向, 在提供的房间grid中, 分别寻找1个能够满足"可以向本方向打开门"的格子的位置, 当某个方向找不到符合要求的格子时, 将使用[-1, -1]表示
    
    - 对于"可以向本方向打开门"的判断标准:
        - 1. 需要首先满足 brogue_directionOfDoorSite 中对格子的要求
        - 2. 其次需要保证向门打开的方向上延伸10格, 不能遇到房间格子
    
    - 返回值:
        
    ```
        (list[list[int, 2], 4]): 
        [
            [int, int], # 1个可以向上打开门的格子的位置
            [int, int], # 1个可以向下打开门的格子的位置
            [int, int], # 1个可以向左打开门的格子的位置
            [int, int]  # 1个可以向右打开门的格子的位置
        ]
    ```
    '''
    
    buffer_grid = grid.copy()
    
    direction_symbols = [
        2,  # up
        3,  # down
        4,  # left
        5   # right
    ]
    
    direction_delta_list = [
        [0, -1],
        [0, 1],
        
    [-1, 0], [1, 0]
    ]

    
    for x in range(buffer_grid.width):
        for y in range(buffer_grid.height):
            
            # 首先判断本格是否满足"可以向本方向打开门"的判断标准的第一点
            direction_index = brogue_directionOfDoorSite(buffer_grid, x, y)
            if direction_index == -1:  # no direction  表示本格无法满足条件
                continue
            
            # 下面的循环会判断是否满足标准的第二点
            direction_delta = direction_delta_list[direction_index]
            direction_delta_x = direction_delta[0]
            direction_delta_y = direction_delta[1]
            
            can_open = True
            for detect_length in range(10):
                # 将门打开的方向(通过第一重判断得到的direction_index)作为探测方向依次延申10格
                detect_x = x + detect_length * direction_delta_x
                detect_y = y + detect_length * direction_delta_y
                # 忽略出界的探测点
                if not buffer_grid.is_valid(detect_x, detect_y):
                    continue
                # 如果发现探测途中遇到了房间格子, 则说明无法向该方向打开门
                if buffer_grid[detect_x, detect_y] == ONE:
                    can_open = False
                    break
            
            # 标记完全符合判断标准的位置为可以打开门的方向的标签
            if can_open:
                buffer_grid[x, y] = direction_symbols[direction_index]
    
    # test_tools.print_grid(buffer_grid, symbols=".#")  # 调试用, 可供查看所有可以生成门的区域以及开口方向
    result = [
        [-1, -1],
        [-1, -1],
        [-1, -1],
        [-1, -1]
    ]
    for direction_index, direction_symbol in enumerate(direction_symbols):
        
        # 找到所有能够朝向 direction_symbol 打开门的格子
        optional_pos_list = []
        for x in range(buffer_grid.width):
            for y in range(buffer_grid.height):
                if buffer_grid[x,y] == direction_symbol:
                    optional_pos_list.append([x,y])
        
        # 选择一个作为结果
        if len(optional_pos_list) > 0:
            result[direction_index] = random.choice(optional_pos_list)
        
        # 否则让 result[direction_index] 维持[-1,-1]表示不存在能够在该方向上打开门的格子

    return result




def brogue_attachHallwayTo(grid: array2d[int], door_positions: list[list[int, 2], 4]):
    '''
    在grid上绘制走廊。并返回走廊的出口坐标, 大多数情况下出口坐标会是在走廊方向继续延伸一格的位置, 在小部分情况下(15%)会返回排除走廊延伸方向的对向方向外的其余3个方向上的坐标
    ```
    如算法选择了door_positions中表示向右打开的门,并生成了走廊:  #表示房间, +表示走廊, 实际上它们的存储值都是1,但这里使用不同的符号加以区分
        # #
        # # + + + + + 
        # #
    此时算法将返回的位置绝大多数是:
        # #
        # # + + + + + @ <---- @表示出口,假设此处坐标是(3, 4), 而因为它向右侧延伸,因此返回值是[[-1,-1], [-1,-1], [-1, -1], [3, 4]]
        # #
    有小部分情况下是:
        # #         @
        # # + + + + + @ <---- 返回值是[[2, 3], [2, 5], [3, 4], [-1, -1]]
        # #         @
    ```
    Args:
        grid (array2d[int]): 二维数组表示地图的网格，应当为地牢的总地图尺寸。
        door_positions (list[list[int, 2], 4]): 4个方向的门的位置列表。
            一个包含4个二元列表的列表，每个二元列表分别表示朝向"上,下,左,右"打开的门的位置。
            当门的位置为[-1, -1]时表示没有朝向该方向打开的门。
    Returns:
        (list[list[int, 2], 4]): 4个方向的走廊出口的位置列表。
        
    '''
    # 要求传入的grid的尺寸必须与总的地牢的地图尺寸一致
    assert grid.width == DUNGEON_WIDTH and grid.height == DUNGEON_HEIGHT
    
    direction_delta_list = [
        [0, -1],
        [0, 1],
        [-1, 0],
        [1, 0]
    ]
    
    # 选择一个合适的方向
    enumerated_door_positions = list(enumerate(door_positions))
    random.shuffle(enumerated_door_positions)

    direction_index = -1  # -1表示没有找到合适的方向
    door_pos = None
    for _direction_index, _door_pos in enumerated_door_positions:
        
        door_x, door_y = _door_pos
        
        # 首先排除没有门的方向的坐标
        if door_x == -1 or door_y == -1:
            continue
        
        # 探测当前开门方向上将生成走廊的最远位置,是否超出了地图边界
        direction_delta = direction_delta_list[_direction_index]
        direction_delta_x = direction_delta[0]
        direction_delta_y = direction_delta[1]
        detect_x = door_x + HORIZONTAL_CORRIDOR_MAX_LENGTH * direction_delta_x
        detect_y = door_y + VERTICAL_CORRIDOR_MAX_LENGTH * direction_delta_y
        
        if grid.is_valid(detect_x, detect_y):
            # 该方向上可以生成走廊
            direction_index = _direction_index
            door_pos = _door_pos
            break
    
    # 四个方向的门都不符合条件,那么就返回吧
    if direction_index == -1:
        return [[-1,-1], [-1,-1], [-1,-1], [-1,-1]]
    
    # 生成垂直方向的走廊
    if direction_index in [0, 1]:  # 0,1表示"上,下"方向的direction_index
        corridor_length = random.randint(VERTICAL_CORRIDOR_MIN_LENGTH, VERTICAL_CORRIDOR_MAX_LENGTH)
    
    # 生成水平方向的走廊
    else:
        corridor_length = random.randint(HORIZONTAL_CORRIDOR_MIN_LENGTH, HORIZONTAL_CORRIDOR_MAX_LENGTH)
    
    
    # 绘制和房间相连的走廊, 走廊的地块使用1表示,和房间地块相同
    direction_delta = direction_delta_list[_direction_index]
    direction_delta_x = direction_delta[0]
    direction_delta_y = direction_delta[1]
    
    start_x, start_y = door_pos
    end_x = start_x + direction_delta_x*(corridor_length-1)
    end_y = start_y + direction_delta_y*(corridor_length-1)
    

    step_x = -1 if end_x < start_x else 1
    step_y = -1 if end_y < start_y else 1

    for x in range(start_x, end_x+step_x, step_x):
        for y in range(start_y, end_y+step_y, step_y):
            grid[x,y] = ONE
    
    # 随机决定是否允许拐弯的走廊出口, 并更新走廊结束处的门位信息
    new_door_positions = door_positions.copy()
    end_x = clamp(end_x, 0, DUNGEON_WIDTH-1)
    end_y = clamp(end_y, 0, DUNGEON_HEIGHT-1)
    allow_oblique_hallway_exit = random.random() < 0.15  # 决定走廊出口是否允许拐弯
    
    for dir2, delta in enumerate(direction_delta_list):
        new_x = end_x + delta[0]
        new_y = end_y + delta[1]

        if (dir2 != direction_index and not allow_oblique_hallway_exit) or \
                not grid.is_valid(new_x, new_y) or grid[new_x, new_y] == ONE:
            new_door_positions[dir2] = [-1, -1]
        else:
            new_door_positions[dir2] = [new_x, new_y]

    return new_door_positions 
