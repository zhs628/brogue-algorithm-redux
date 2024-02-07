'''
生成房间和走廊
'''


from array2d import array2d
import random
from . import SimpleShapes
import test_tools
import random
from .const import *


# 在本文件中, 完全复刻自brogue的算法将使用 "brogue_<brogue中该函数的原名>" 命名
def clamp(x, low, hi):
    '''
    将x限制在区间[low, hi]内
    '''
    return min(max(x, low), hi)
def is_in_dungeon(x:int, y:int) -> bool:
    return x >= 0 and x < DUNGEON_WIDTH and y >= 0 and y < DUNGEON_HEIGHT



def insert_room_to_grid(grid: array2d, room_grid: array2d, delta_x:int, delta_y:int, start_x:int, start_y:int):
    '''
    复制room_grid的一个相连的图案到grid中, 在room_grid中的点(x,y)将通过(x + delta_x, y + delta_y)映射到grid中
    设置start_x, start_y来选择room_grid中将被复制的相连图案的任意内点
    '''
    fill_value = room_grid[start_x, start_y]
    grid[start_x+delta_x, start_y+delta_y] = fill_value
    edge_neighbor_pos_list = [
        [start_x, start_y - 1],
        [start_x, start_y + 1],
        [start_x - 1, start_y],
        [start_x + 1, start_y],
    ]
    # 注意循环变量所指代的那个坐标一直都是在room_grid中的点
    for next_x, next_y in edge_neighbor_pos_list:
        
        # 判断下一个点是否在room_grid中
        if not room_grid.is_valid(next_x, next_y):
            continue
        # 判断下一个点的目标点是否在grid中
        if not grid.is_valid(next_x+delta_x, next_y+delta_y):
            continue
        # 判断下一个点的目标点是否是已被复制的点
        if grid[next_x+delta_x, next_y+delta_y] == fill_value:
            continue
        
        if room_grid[next_x, next_y] == fill_value:
            insert_room_to_grid(grid, room_grid, delta_x, delta_y, next_x, next_y)




def flood_fill(grid: array2d[int], fill_value, target_value, start_x=0, start_y=0):
    '''
    从指定位置开始向四边填充, 将值为 target_value 的格子填充为 fill_value 最终返回填充的总面积 

    参数列表:
        grid:
            将对该网格就地填充和修改
        fill_value:
            填充的值
        target_value:
            只有值为 target_value 的格子才会被填充并计算面积
        start_x:
            开始填充的横坐标
        start_y:
            开始填充的纵坐标
    '''
    filled_cell_count = 0
    if grid[start_x, start_y] != target_value:
        return filled_cell_count
    filled_cell_count += _flood_fill_inner_func(grid, fill_value, target_value, start_x, start_y)
    return filled_cell_count


def _flood_fill_inner_func(grid: array2d[int], fill_value, target_value, start_x: int = 0, start_y: int = 0):
    filled_cell_count = 0
    grid[start_x, start_y] = fill_value
    edge_neighbor_pos_list = [
        [start_x, start_y - 1],
        [start_x, start_y + 1],
        [start_x - 1, start_y],
        [start_x + 1, start_y],
    ]
    for next_x, next_y in edge_neighbor_pos_list:
        if not grid.is_valid(next_x, next_y):
            break
        if grid[next_x, next_y] == target_value:
            filled_cell_count += _flood_fill_inner_func(grid, fill_value, target_value, next_x, next_y)
    
    return filled_cell_count + 1  # 将递归结果添加到 filled_cell_count 中并返回


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
                            ? ■ ?
                              +     问号可以是任意格子,加号是(door_X,door_Y), 实心方块是房间格子(值为1), 此时门的朝向为(door_x, door_y)的下方, 函数将返回1
    下面的情况都无法生成门:
        1. 2个及以上邻边都有打开门的条件:
                ■ ■
                + ■   此处因为下侧和左侧都符合打开门的条件, 因此这一格不能生成门, 必须仅有一侧能够打开门, 才符合最终条件
                
        2. 门的打开方向是地图边界:
            \\|   ■
            \\| + ■ <-- 此处因为其对称点在地图边界外, 因此不能生成门
            \\|   ■
    
    '''
    
    # 门不能生成在房间内,而至少是房间边缘的外侧一格
    if grid[door_x, door_y] == ONE:
        return -1 # no direction
    
    edge_neighbor_pos_list = [
        [door_x, door_y - 1],
        [door_x, door_y + 1],
        [door_x - 1, door_y],
        [door_x + 1, door_y],
    ]
    
    # -1  no direction
    direction_index_list = [
        0,  # up
        1,  # down
        2,  # left
        3   # right
    ]
    
    
    selected_direction_index = -1
    for direction, neighbor_pos in list(zip(direction_index_list, edge_neighbor_pos_list)):
        neighbor_x, neighbor_y = neighbor_pos
        
        # 以(door_x, door_y)为中心, 计算其对称点的坐标
        opposite_x = door_x - (neighbor_x - door_x)
        opposite_y = door_y - (neighbor_y - door_y)
        
        # 无法满足这些条件的方位, 将不能打开门, 因此跳过
        if not grid.is_valid(neighbor_x, neighbor_y) or not grid.is_valid(opposite_x, opposite_y):
            continue
        # 如果对称点不是房间格子, 则不能打开门, 因此跳过
        if grid[opposite_x, opposite_y] != ONE:
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









# 下面是生成房间的逻辑-------------------------------------------

def brogue_designCircularRoom(grid: array2d[int]):
    '''
    在grid中央上绘制一个圆形房间, 有大概率生成实心圆, 有小概率生成甜甜圈样式
    
    圆的半径在2~10之间
    '''
    assert grid.width >= 21 and grid.height >= 21 
    
    grid.fill_(0)  # 以0填充所有的格子

    center_x = grid.width//2
    center_y = grid.height//2
    
    # 确定房间的半径
    if random.random() < 0.5:
        room_radius = random.randint(4, 10)
    else:
        room_radius = random.randint(2, 4)
    
    # 绘制房间
    SimpleShapes.draw_circle(grid, ONE, center_x, center_y, room_radius)
    
    # 绘制房间中的空洞
    if room_radius > 6 and random.random() < 0.5:
        hole_radius = random.randint(3, room_radius-3)
        SimpleShapes.draw_circle(grid, ZERO, center_x, center_y, hole_radius)


def brogue_designSmallRoom(grid: array2d[int]):
    '''
    在grid中央上绘制一个矩形房间
    
    矩形宽度在3~6之间, 高度在2~4之间
    '''
    assert grid.width >= 6 and grid.height >= 4 
    
    grid.fill_(ZERO)  # 以0填充所有的格子
    
    room_width = random.randint(3, 6)
    room_height = random.randint(2, 4)
    room_x = (grid.width - room_width) // 2  # 确保房间的中心和grid中心对齐
    room_y = (grid.height - room_height) // 2
    
    SimpleShapes.draw_rectangle(grid, ONE, room_x, room_y, room_width, room_height)
    
    
def brogue_designCrossRoom(grid: array2d[int]):
    '''
    在房间偏左下的位置生成两个矩形交叉而成的房间
    '''
    assert grid.width >= 30 and grid.height >= 15
    grid.fill_(ZERO)  # 以0填充所有的格子

    # 确定两个房间的x坐标和宽度
    room1_width = random.randint(3, 12)
    room1_x =                                           \
        random.randint(
            max(0, grid.width//2 - (room1_width - 1)),
            grid.width//2
        )
    
    room2_width = random.randint(4, 20)
    room2_x =                                           \
        random.choice([-1, 0,0, 1,1,1, 2,2, 3]) +       \
        room1_x +                                       \
        (room1_width - room2_width)//2
    
    
    # 确定两个房间的y坐标和高度
    room1_height = random.randint(3, 7)
    room1_y = grid.height//2 - room1_height
    
    room2_height = random.randint(2, 5)
    room2_y =                                           \
        grid.height//2 -                                \
        room2_height -                                  \
        random.choice([0, -1,-1, -2,-2, -3])            
    
    # 将房间整体向左下角偏移
    room1_x -= 5
    room2_x -= 5
    room1_y += 5
    room2_y += 5
    
    # 绘制
    SimpleShapes.draw_rectangle(grid, ONE, room1_x, room1_y, room1_width, room1_height)
    SimpleShapes.draw_rectangle(grid, ONE, room2_x, room2_y, room2_width, room2_height)


def brogue_designSymmetricalCrossRoom(grid: array2d[int]):
    '''
    在房间中央生成两个矩形交叉而成的房间
    
    将不会生成"L"形房间
    '''
    assert grid.width >= 8 and grid.height >= 5 
    grid.fill_(ZERO)  # 以0填充所有的格子

    # 确定房间1的规格
    room1_width = random.randint(4, 8)
    room1_height = random.randint(4, 5)
    
    # 根据房间1规格的奇偶性, 确定房间2的规格, 为了避免生成"L"型房间
    room2_width = random.randint(3, 4) - 1 if room1_height % 2 == 0 else random.randint(3, 4)
    room2_height = 3 - 1 if room1_width % 2 == 0 else 3
    
    # 根据两个房间的规格, 确定格子的位置, 为了使得它们落在grid中央
    room1_x = (grid.width - room1_width) // 2
    room1_y = (grid.height - room1_height) // 2
    room2_x = (grid.width - room2_width) // 2
    room2_y = (grid.height - room2_height) // 2
    
    # 绘制
    SimpleShapes.draw_rectangle(grid, ONE, room1_x, room1_y, room1_width, room1_height)
    SimpleShapes.draw_rectangle(grid, ONE, room2_x, room2_y, room2_width, room2_height)


def brogue_designChunkyRoom(grid: array2d[int]):
    '''
    生成若干连续的小圆(下面称作chunk)拼成的房间, 首个圆生成在grid中央
    '''
    assert grid.width >= 14 and grid.height >= 15
    
    grid.fill_(ZERO) # 以0填充所有的格子

    chunk_count = random.randint(2, 8)  # 即将生成的小圆数量
    radius = 2  # 所有小圆的半径
    
    # 定义并绘制首个圆, 并寄存到表示"上一个圆"的变量
    last_circle = {
        'x': grid.width // 2, 
        'y': grid.height // 2,
        'next_min_x': grid.width // 2 - 3,  # 下一个圆的圆心随机生成范围
        'next_max_x': grid.width // 2 + 3,
        'next_min_y': grid.height // 2 - 3,
        'next_max_y': grid.height // 2 + 3,
    }
    SimpleShapes.draw_circle(grid, ONE, last_circle['x'], last_circle['y'], radius)
    
    for _ in range(chunk_count):
        # 确定圆的位置, 必须让所有的圆的圆心落在已绘制的区域上
        while True:
            x = random.randint(last_circle['next_min_x'], last_circle['next_max_x'])
            y = random.randint(last_circle['next_min_y'], last_circle['next_max_y'])
            if grid[x,y] == 1:
                break
            
        
        # 确定当前的圆
        circle = {
            'x': x, 
            'y': y,
            'next_min_x': max(1, min(x-3, last_circle['next_min_x'])),
            'next_max_x': min(grid.width-2, max(x+3, last_circle['next_max_x'])),
            'next_min_y': max(1, min(y-3, last_circle['next_min_y'])),
            'next_max_y': min(grid.height-2, max(y+3, last_circle['next_max_y']))
        }
        
        last_circle = circle

        #绘制
        SimpleShapes.draw_circle(grid, ONE, circle['x'], circle['y'], radius)


def brogue_designEntranceRoom(grid: array2d[int]):
    assert grid.width >= 22 and grid.height >= 12 
    
    grid.fill_(ZERO)
    
    room1_width = 8
    room1_height = 10
    room2_width = 20
    room2_height = 5
    room1_x = grid.width // 2 - room1_width // 2 - 1
    room1_y = grid.height - room1_height - 2
    room2_x = grid.width // 2 - room2_width // 2 - 1
    room2_y = grid.height - room2_height - 2

    fill_value = ONE
    SimpleShapes.draw_rectangle(grid, ONE, room1_x, room1_y, room1_width, room1_height)
    SimpleShapes.draw_rectangle(grid, ONE, room2_x, room2_y, room2_width, room2_height)
    

# ---------------------------------洞穴---------------------------------
# 关于洞穴的生成算法, 程序将不断尝试在max_width, max_height内随机生成块, 而直到块的规格符合要求时才会停止
# 根据经验, 它们的规格多数集中在max_width/2, max_height/2附近, 因此当块的下限min_width, min_height大于max_width/2, max_height/2时, 将很难在短时间内生成洞穴
# 因此对于下列预设的函数, 传入的grid的规格需要尽可能大(我已经基于大量测试设定了合适的assert限制), 以防止生成速度变慢, 甚至是超出1000次的重新生成限制报AssertionError

def brogue_design_compat_cavern(grid: array2d):
    _brogue_designCavern(grid, 3, 12, 4, 8)

def brogue_design_large_north_south_cavern(grid: array2d):
    assert grid.width >= 4 and grid.height >= 18
    _brogue_designCavern(grid, 3, 12, 15, grid.height-2)

def brogue_design_large_east_west_cavern(grid: array2d):
    assert grid.width >= 22 and grid.height >= 22
    _brogue_designCavern(grid, 20, grid.height-2, 4, 8)

def brogue_design_cave(grid: array2d):
    assert grid.width >= CAVE_MIN_WIDTH and grid.height >= CAVE_MIN_HEIGHT
    _brogue_designCavern(grid, CAVE_MIN_WIDTH, grid.width-2, CAVE_MIN_HEIGHT, grid.height-2)



# ----------- _brogue_designCavern 为原作函数, 以上为原作中调用该函数的四个地方
def _brogue_designCavern(
    grid: array2d[int],      
    min_width: int,  # 房间的生成限宽和限高
    max_width: int, 
    min_height: int, 
    max_height: int \
    ):
    '''
    使用元胞自动机生成限定规格的一块洞穴样式的房间
    '''
    assert min_width <= max_width and min_height <= max_height
    
    grid.fill_(ZERO)
    
    blob_grid = array2d(grid.width, grid.height, default=None)  # 用来生成块的网格, 规格与grid一致
    round_count = 2  # 当它被设定地很高时, 生成将非常耗时, 当它越大, 房间越大,但是边缘越粗糙, 反之, 当它越小,房间越小,边缘越光滑
    noise_probability = 0.55
    birth_parameters = "ffffffttt"
    survival_parameters = "ffffttttt"
    blob_x, blob_y, blob_w, blob_h = _brogue_createBlobOnGrid(blob_grid, min_width, max_width, min_height, max_height, round_count, noise_probability, birth_parameters, survival_parameters)
    
    
    # 下面将生成的块从blob_grid中复制到grid中
    
    # 遍历块的外接矩形, 寻找块中的一个内点
    inside_x, inside_y = None, None
    for y in range(blob_y, blob_y + blob_h):
        has_found = False
        for x in range(blob_x, blob_x + blob_w):
            if blob_grid[x,y] == 1:
                inside_x, inside_y = x, y
                has_found = True
                break
        if has_found:
            break
    
    # 移动块的中心点到grid的中心点
    delta_x = (grid.width - blob_w)//2 - blob_x
    delta_y = (grid.height - blob_h)//2 - blob_y
    insert_room_to_grid(grid, blob_grid, delta_x, delta_y, inside_x, inside_y)



# _brogue_designCavern 的一部分, 用于构造房间, _brogue_designCavern会将该房间插入到大的grid
def _brogue_createBlobOnGrid(
    grid: array2d[int], 
    blob_min_width: int, 
    blob_max_width: int, 
    blob_min_height: int,  
    blob_max_height: int,  
    round_count = 5, 
    noise_probability = 0.55, 
    birth_parameters = 'ffffffttt',  
    survival_parameters = 'ffffttttt' \
    ):
    '''
    本函数利用细胞自动机按照培育参数在给定的空网格之内生成图案, 并返回最大的块在网格中的位置和规格
    
    参数列表:
        grid:  
            用于培育块的网格
        blob_min_width:  
            用于限制块的规格
        blob_max_width:  
            用于限制块的规格
        blob_min_height:  
            用于限制块的规格
        blob_max_height:   
            用于限制块的规格
        round_count = 10:  
            细胞自动机的迭代次数
        noise_probability = 0.55 :
            初始噪声的生成率 
        birth_parameters = 'ffffffttt' :
            长度为9的字符串, 表示当前格子附近3x3区域内存在index个细胞时, birth_parameters[index]的值(t/f)将决定本格子是否在下一轮迭代时生成细胞, 或使本格子细胞存活
        survival_parameters = 'ffffttttt' :
            同上, 假如本格子不会诞生新细胞, 那么这个参数将判定周围细胞的密度以决定下一轮迭代时本格子的细胞是否会被销毁, 't'表示存活, 'f'表示销毁
    
    返回值:
        四元组, 其中每个元素分别表示最大块外接矩形的 (左上角x坐标, 左上角y坐标, 宽度, 高度)
    '''
    
    survival_value, dead_value = -1, -2
    neighbor_cell_delta_list = [
        [-1,-1], [ 0,-1], [ 1,-1],
        [-1, 0],          [ 1, 0],
        [-1, 1], [ 0, 1], [ 1, 1]
    ]
    
    TIME_OUT_LOOP = 10000
    loop_count = 0
    while True:
        loop_count += 1
        assert loop_count <= TIME_OUT_LOOP
        
        grid.fill_(0)
        # ---- 生成初始噪声
        for x in range(blob_max_width):
            for y in range(blob_max_height):
                if not grid.is_valid(x, y):
                    continue
                if random.random() < noise_probability:
                    grid[x,y] = survival_value
                else:
                    grid[x,y] = dead_value
        
        # ---- 细胞自动机开始数轮迭代
        for _ in range(round_count):

            # 每轮迭代遍历并修改 blob_grid 所有格子
            last_grid = grid.copy()  # 记录上一轮迭代的最终结果, 接下来将就地修改blob_grid

            # 计算当前格子的周围中存在活细胞的数量
            live_neighbors = grid.count_neighbors(survival_value)
            
            for cell_x in range(grid.width):
                for cell_y in range(grid.height):
                    # 计算本轮迭代中该格子的细胞的命运
                    nb_count = live_neighbors[cell_x, cell_y]
                    last_value = last_grid[cell_x, cell_y]
                    # 原作实现：
                    # if (!buffer2[i][j] && birthParameters[nbCount] == 't') {
                    #     grid[i][j] = 1; // birth
                    # } else if (buffer2[i][j] && survivalParameters[nbCount] == 't') {
                    #     // survival
                    # } else {
                    #     grid[i][j] = 0; // death
                    # }
                    if last_value == dead_value and birth_parameters[nb_count] == 't':
                        grid[cell_x, cell_y] = survival_value   # birth
                    elif last_value == survival_value and survival_parameters[nb_count] == 't':
                        pass    # survival
                    else:
                        grid[cell_x, cell_y] = dead_value
        
        now_id = 0  # 每个块的新填充值, 每找到一个块,就加一
        blob_list = []  
        # [
        #     {
        #         "id": int,
        #         "size": int,
        #     },
        #     ...
        # ]
        
        # 为每个块填上新的表示编号的填充值, 并记录每个块的尺寸
        for x in range(grid.width):
            for y in range(grid.height):
                
                # 剔除被赋予blob_id的格子, 以及细胞死亡的格子, 只留下细胞存活的, 没有被赋予blob_id的格子
                # 注意: 每当一个块首次被遍历时, 它内部所有格子都将被赋予编号
                if grid[x,y] != survival_value :
                    continue 
                
                
                fill_value = now_id
                target_value = survival_value
                blob_size = flood_fill(grid, fill_value, target_value, start_x=x, start_y=y)
                blob_list.append(
                    {
                        "id": now_id,
                        "size": blob_size,
                    }
                )
                
                now_id += 1
        
        
        # 假如啥也没有生成, 就从头来过
        if not blob_list:
            continue
        
        # 下面开始计算最大的块的外接矩形
        blob_size_list = []  # [size, size, ...]
        for dic in blob_list:
            blob_size_list.append(dic["size"])
            
        biggest_blob = {
            "id": blob_size_list.index(max(blob_size_list)),
            "size": max(blob_size_list),
            "min_x": None,
            "max_x": None,
            "min_y": None,
            "max_y": None,
            "width": None,
            "height": None
        }
        
        scan_loops = [
        #   outer loop                 inner loop          scan target      x,y/y,x
            ((0, grid.height, 1), (grid.width,),  "min_y",         "y,x"),
            ((0, grid.width, 1),  (grid.height,), "min_x",         "x,y"),
            ((grid.height-1, 0-1, -1),(grid.width,),  "max_y",         "y,x"),
            ((grid.width-1, 0-1, -1), (grid.height,), "max_x",         "x,y"),
        ]
        
        # 从四个方向自外向内搜索块的边界
        for outer_loop, inner_loop, scan_target, x_y in scan_loops:

            # 扫描线从grid的边缘开始向内推进
            for scan_line_index in range(*outer_loop):

                # 遍历当前正在扫描的行或列
                has_found_scan_target = False
                for scan_cell_index in range(*inner_loop):
                    # 确定正在扫描的格子坐标
                    if x_y == "x,y":
                        x, y = scan_line_index, scan_cell_index
                    else:
                        y, x = scan_line_index, scan_cell_index

                    
                    # 首次发现时记录当前的扫描线的推进距离 scan_line 这就是块的边界
                    if grid[x, y] == biggest_blob["id"]:
                        biggest_blob[scan_target] = scan_line_index
                        has_found_scan_target = True
                        break
                
                # 首次发现块后, 结束当前方向上的扫描
                if has_found_scan_target:
                    break
        
        # 计算规格
        biggest_blob["width"] = biggest_blob["max_x"] - biggest_blob["min_x"] + 1
        biggest_blob["height"] = biggest_blob["max_y"] - biggest_blob["min_y"] + 1
        
        # 检测是否满足对块的规格限制
        if (blob_min_width <= biggest_blob['width'] <= blob_max_width)  and  (blob_min_height < biggest_blob['height'] <= blob_max_height):
            
            # 设置最大块之外的地方填充为0, 并设置最大块的填充值为1
            for x in range(grid.width):
                for y in range(grid.height):
                    if grid[x, y] == biggest_blob['id']:
                        grid[x, y] = ONE
                    else:
                        grid[x, y] = ZERO
            
            # 终止外层while循环, 返回最大块的信息
            # print("loop_count:", loop_count)
            return (biggest_blob["min_x"], biggest_blob["min_y"], biggest_blob["width"], biggest_blob["height"])
        
        # else:
        #     import test_tools
        #     test_tools.print_grid(grid, symbols=' ')



# 以上所有房间生成算法的调用者, 将从以上房间中随机选择一个生成, 并生成走廊并返回走廊出口----------------------------
def brogue_designRandomRoom(grid:array2d[int], room_type_frequencies:list[float]=(1,1,1,1,1,1,1,1), has_doors:bool=True, has_hallway:bool=True):
    '''
    在grid中就地生成一个随机的房间, 附加上走廊并返回走廊出口
    
    Args:
        grid (array2d[int]): 二维数组表示地图的网格，应当为地牢的总地图尺寸。
        has_doors (bool): 是否生成门
        has_hallway (bool): 是否生成走廊(只有当有has_doors为True时才有效)
        room_type_frequencies (list[float, ROOM_TYPE_COUNT]): 一个长度为ROOM_TYPE_COUNT的列表, 表示每种房间的生成概率权重, 每个权重的值大于等于0即可
    Returns:
        (list[list[int, 2], 4]): 表示 走廊出口/门 的位置
    '''
    # 根据 room_type_frequencies 采用轮盘赌选择房间类型
    assert len(room_type_frequencies) == ROOM_TYPE_COUNT
    room_type_func_index = -1
    #     累加权重以创建权重累积列表
    cumulative_weights = []
    total_sum = 0
    for w in room_type_frequencies:
        assert w >= 0  # 每一个权重必须是非负数
        total_sum += w
        cumulative_weights.append(total_sum)

    #     生成一个0到总权重累积之间的随机数
    r = random.uniform(0, total_sum)

    #     找到随机数所在的权重区间
    for index, cumulative_weight in enumerate(cumulative_weights):
        if r < cumulative_weight:
            room_type_func_index = index
            break  # 返回该区间对应的原始权重列表的索引
    
    # 必须找到一个合法的房间类型索引
    assert room_type_func_index >= 0 and room_type_func_index < ROOM_TYPE_COUNT
    
    # 生成房间
    room_type_func_list = [
        brogue_designCrossRoom,
        brogue_designSymmetricalCrossRoom,
        brogue_designSmallRoom,
        brogue_designCircularRoom,
        brogue_designChunkyRoom,
        [
            brogue_design_compat_cavern,
            brogue_design_large_north_south_cavern,
            brogue_design_large_east_west_cavern,
        ],
        brogue_design_cave,
        brogue_designEntranceRoom
    ]
    selected_element = room_type_func_list[room_type_func_index]
    if isinstance(selected_element, list):  # 选中了cavern, 那么进一步选择生成什么cavern
        room_type_func = random.choice(selected_element)
    else:
        room_type_func = selected_element
    
    # 生成房间
    room_type_func(grid)
    
    # 生成门
    door_positions = [[-1,-1], [-1,-1], [-1,-1], [-1,-1]]
    if has_doors:
        door_positions = brogue_chooseRandomDoorSites(grid)
        
        # 生成走廊
        if has_hallway:
            door_positions = brogue_attachHallwayTo(grid, door_positions)
            
    return door_positions