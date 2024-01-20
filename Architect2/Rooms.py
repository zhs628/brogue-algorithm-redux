from array2d import array2d
import random
from . import SimpleShapes


# 在本文件中, 完全复刻自brogue的算法将使用 "brogue_<brogue中该函数名>" 命名

def fill_grid(grid: array2d, value=0):
    SimpleShapes.draw_rectangle(grid, value, 0, 0, grid.width, grid.height)
    
    

def flood_fill(grid: array2d, fill_value, target_value, start_x:int=0, start_y:int=0):
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

def _flood_fill_inner_func(grid: array2d, fill_value, target_value, start_x: int = 0, start_y: int = 0):
    filled_cell_count = 0
    grid[start_x, start_y] = fill_value
    edge_neighbor_pos_list = [
        [start_x, start_y + 1],
        [start_x, start_y - 1],
        [start_x + 1, start_y],
        [start_x - 1, start_y],
    ]
    for next_x, next_y in edge_neighbor_pos_list:
        if not grid.is_valid(next_x, next_y):
            break
        if grid[next_x, next_y] == target_value:
            filled_cell_count += _flood_fill_inner_func(grid, fill_value, target_value, next_x, next_y)
    
    return filled_cell_count + 1  # 将递归结果添加到 filled_cell_count 中并返回

def brogue_designCircularRoom(grid: array2d):
    '''
    在grid中央上绘制一个圆形房间, 有大概率生成实心圆, 有小概率生成甜甜圈样式
    
    圆的半径在2~10之间
    '''
    assert grid.width >= 21 and grid.height >= 21 
    
    fill_grid(grid, value=0)  # 以0填充所有的格子

    center_x = grid.width//2
    center_y = grid.height//2
    
    
    # 确定房间的半径
    if random.random() < 0.5:
        room_radius = random.randint(4, 10)
    else:
        room_radius = random.randint(2, 4)
    
    # 绘制房间
    SimpleShapes.draw_circle(grid, 1, center_x, center_y, room_radius)
    
    # 绘制房间中的空洞
    if room_radius > 6 and random.random() < 0.5:
        hole_radius = random.randint(3, room_radius-3)
        fill_value = 0
        SimpleShapes.draw_circle(grid, fill_value, center_x, center_y, hole_radius)


def brogue_designSmallRoom(grid: array2d):
    '''
    在grid中央上绘制一个矩形房间
    
    矩形宽度在3~6之间, 高度在2~4之间
    '''
    assert grid.width >= 6 and grid.height >= 4 
    
    fill_grid(grid, value=0)  # 以0填充所有的格子
    
    room_width = random.randint(3, 6)
    room_height = random.randint(2, 4)
    room_x = (grid.width - room_width) // 2  # 确保房间的中心和grid中心对齐
    room_y = (grid.height - room_height) // 2
    
    fill_value=1
    SimpleShapes.draw_rectangle(grid, fill_value, room_x, room_y, room_width, room_height)
    
    
def brogue_designCrossRoom(grid: array2d):
    '''
    在房间偏左下的位置生成两个矩形交叉而成的房间
    '''
    assert grid.width >= 30 and grid.height >= 15
    fill_grid(grid, value=0)  # 以0填充所有的格子

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
    fill_value = 1
    SimpleShapes.draw_rectangle(grid, fill_value, room1_x, room1_y, room1_width, room1_height)
    SimpleShapes.draw_rectangle(grid, fill_value, room2_x, room2_y, room2_width, room2_height)
    
def brogue_designSymmetricalCrossRoom(grid: array2d):
    '''
    在房间中央生成两个矩形交叉而成的房间
    
    将不会生成"L"形房间
    '''
    assert grid.width >= 8 and grid.height >= 5 
    fill_grid(grid, value=0)  # 以0填充所有的格子

    # 确定房间1的规格
    room1_width = random.randint(4, 8)
    room1_height = random.randint(4, 5)
    
    # 根据房间1规格的奇偶性, 确定房间2的规格, 为了避免生成"L"型房间
    room2_width = random.randint(3, 4) - 1 if room1_height % 2 == 0 else random.randint(3, 4)
    room2_height = 3 - 1 if room1_width % 2 == 0 else 3
    
    # 根据两个房间的规格, 确定格子的位置, 为了使得它们落在grid中央
    room1_x = (grid.width - room1_width)//2
    room1_y = (grid.height - room1_height)//2
    room2_x = (grid.width - room2_width)//2
    room2_y = (grid.height - room2_height)//2
    
    # 绘制
    fill_value = 1
    SimpleShapes.draw_rectangle(grid, fill_value, room1_x, room1_y, room1_width, room1_height)
    SimpleShapes.draw_rectangle(grid, fill_value, room2_x, room2_y, room2_width, room2_height)


def brogue_designChunkyRoom(grid: array2d):
    '''
    生成若干连续的小圆(下面称作chunk)拼成的房间, 首个圆生成在grid中央
    '''
    assert grid.width >= 14 and grid.height >= 15
    
    fill_grid(grid, value=0)  # 以0填充所有的格子

    chunk_count = random.randint(2, 8)  # 即将生成的小圆数量
    radius = 2  # 所有小圆的半径
    
    # 定义并绘制首个圆, 并寄存到表示"上一个圆"的变量
    last_circle = {
        'x': grid.width//2, 
        'y': grid.height//2,
        'next_min_x': grid.width//2 - 3,  # 下一个圆的圆心随机生成范围
        'next_max_x': grid.width//2 + 3,
        'next_min_y': grid.height//2 - 3,
        'next_max_y': grid.height//2 + 3,
    }
    fill_value = 1
    SimpleShapes.draw_circle(grid, fill_value, last_circle['x'], last_circle['y'], radius)
    
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
        fill_value = 1
        SimpleShapes.draw_circle(grid, fill_value, circle['x'], circle['y'], radius)


def brogue_designEntranceRoom(grid: array2d):
    assert grid.width >= 22 and grid.height >= 12 
    
    fill_grid(grid, value=0)
    
    room1_width = 8
    room1_height = 10
    room2_width = 20
    room2_height = 5
    room1_x = grid.width//2 - room1_width//2 - 1
    room1_y = grid.height - room1_height - 2
    room2_x = grid.width//2 - room2_width//2 - 1
    room2_y = grid.height - room2_height - 2

    fill_value = 1
    SimpleShapes.draw_rectangle(grid, fill_value, room1_x, room1_y, room1_width, room1_height)
    SimpleShapes.draw_rectangle(grid, fill_value, room2_x, room2_y, room2_width, room2_height)
    




# ----------- _brogue_designCavern 为原作函数
def _brogue_designCavern(
    grid: array2d,      
    min_width: int,  # 房间的生成限宽和限高
    max_width: int, 
    min_height: int, 
    max_height: int \
    ):
    '''
    使用元胞自动机生成限定规格的一块洞穴
    '''
    fill_grid(grid, 0)
    
    blob_grid = array2d(max_width, max_height, default=None)
    round_count = 5
    _brogue_createBlobOnGrid(blob_grid, round_count, min_width, max_width, min_height, max_height)
    # TODO


# _brogue_designCavern 的一部分, 用于构造房间, _brogue_designCavern会将该房间插入到大的grid
def _brogue_createBlobOnGrid(
    blob_grid: array2d, 
    round_count: int,  
    blob_min_width: int, 
    blob_max_width: int, 
    blob_min_height: int,  
    blob_max_height: int,  
    noise_probability = 0.55, 
    birth_parameters = 'ffffffttt',  
    survival_parameters = 'ffffttttt' \
    ):
    '''
    本函数利用细胞自动机按照培育参数在给定的空网格之内生成图案, 并返回最大的块在网格中的位置和规格
    
    参数列表:
        blob_grid:  
            用于培育块的网格
        round_count:  
            细胞自动机的迭代次数
        blob_min_width:  
            用于限制块的规格
        blob_max_width:  
            用于限制块的规格
        blob_min_height:  
            用于限制块的规格
        blob_max_height:   
            用于限制块的规格
        noise_probability = 0.55 :
            初始噪声的生成率 
        birth_parameters = 'ffffffttt' :
            长度为9的字符串, 表示当前格子附近3x3区域内存在index个细胞时, birth_parameters[index]的值(t/f)将决定本格子是否在下一轮迭代时生成细胞, 或使本格子细胞存活
        survival_parameters = 'ffffttttt' :
            同上, 假如本格子不会诞生新细胞, 那么这个参数将判定周围细胞的密度以决定下一轮迭代时本格子的细胞是否会被销毁, 't'表示存活, 'f'表示销毁
    
    返回值:
        四元组, 其中每个元素分别表示最大块外接矩形的 (左上角x坐标, 左上角y坐标, 宽度, 高度)
    '''
    
    # ---- 生成初始噪声
    survival_value, dead_value = True, False
    
    blob_grid = blob_grid.map1d(lambda _,__: survival_value if random.random() < noise_probability else dead_value)

    
    neighbor_cell_delta_list = [
        [-1,-1], [ 0,-1], [ 1,-1],
        [-1, 0],          [ 1, 0],
        [-1, 1], [ 0, 1], [ 1, 1]
    ]
    
    
    # ---- 细胞自动机开始数轮迭代
    for _ in range(round_count):

        # 每轮迭代遍历并修改 blob_grid 所有格子
        last_grid = blob_grid.copy()  # 记录上一轮迭代的最终结果, 接下来将就地修改blob_grid
        for cell_x in blob_grid.width:
            for cell_y in blob_grid.height:
                
                # 计算当前格子的周围中存在活细胞的数量
                neighbor_survived_num = sum([                      
                    1 for dx, dy in neighbor_cell_delta_list  
                    if blob_grid.is_valid(cell_x + dx, cell_y + dy) and last_grid[cell_x + dx, cell_y + dy] == survival_value  # 遍历的坐标必须在grid之内, 也必须是活细胞
                    ])
                
                
                # 计算本轮迭代中该格子的细胞的命运
                will_birth = \
                    last_grid[cell_x, cell_y] == dead_value \
                    and birth_parameters[neighbor_survived_num] == 't'
                    
                will_survive = \
                    last_grid[cell_x, cell_y] == survival_value \
                    and survival_parameters[neighbor_survived_num] == 't'
                
                will_die = not will_survive
                
                if will_birth:
                    blob_grid[cell_x, cell_y] = survival_value
                if will_survive:
                    pass
                if will_die:
                    blob_grid[cell_x, cell_y] = dead_value
        
    
    blob_list = []
    blob = {
        "fill_value": 0,
        "size": 0,
    }
    # TODO


# ------------------------------------------------------------------TODO
# def brogue_design_compat_cavern(grid: array2d):
#     _brogue_designCavern(grid, 3, 12, 4, 8)

# def brogue_design_large_north_south_cavern(grid: array2d):
#     _brogue_designCavern(grid, 3, 12, 15, grid.height-2)

# def brogue_design_large_east_west_cavern(grid: array2d):
#     _brogue_designCavern(grid, 20, grid.height-2, 4, 8)

# def brogue_design_min_cavern(grid: array2d):
#     _brogue_designCavern(grid, 50, grid.width-2, 20, grid.height-2)