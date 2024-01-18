from array2d import array2d
import random
from . import SimpleShapes


# 在本文件中, 完全复刻自brogue的算法将使用 "brogue_<brogue中该函数名>" 命名

def fill_grid(grid, value=0):
    SimpleShapes.draw_rectangle(grid, value=value, conor_x=0, conor_y=0, width=grid.width, height=grid.height)

def brogue_designCircularRoom(grid):
    '''
    在grid中央上绘制一个圆形房间, 有大概率生成实心圆, 有小概率生成甜甜圈样式
    
    圆的半径在2~10之间
    '''
    fill_grid(grid, value=0)  # 以0填充所有的格子

    center_x = grid.width//2
    center_y = grid.height//2
    
    
    # 确定房间的半径
    if random.random() < 0.5:
        room_radius = random.randint(4, 10)
    else:
        room_radius = random.randint(2, 4)
    
    # 绘制房间
    SimpleShapes.draw_circle(grid, value=1, center_x=center_x, center_y=center_y, radius=room_radius)
    
    # 绘制房间中的空洞
    if room_radius > 6 and random.random() < 0.5:
        hole_radius = random.randint(3, room_radius-3)
        SimpleShapes.draw_circle(grid, value=0, center_x=center_x, center_y=center_y, radius=hole_radius)


def brogue_designSmallRoom(grid):
    '''
    在grid中央上绘制一个矩形房间
    
    矩形宽度在3~6之间, 高度在2~4之间
    '''
    fill_grid(grid, value=0)  # 以0填充所有的格子
    
    room_width = random.randint(3, 6)
    room_height = random.randint(2, 4)
    room_x = (grid.width - room_width) // 2  # 确保房间的中心和grid中心对齐
    room_y = (grid.height - room_height) // 2
    
    SimpleShapes.draw_rectangle(grid, value=1, conor_x=room_x, conor_y=room_y, width=room_width, height=room_height)
    
    
def brogue_designCrossRoom(grid):
    '''
    在房间偏左下的位置生成两个矩形交叉而成的房间
    '''
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
    SimpleShapes.draw_rectangle(grid, value=1, conor_x=room1_x, conor_y=room1_y, width=room1_width, height=room1_height)
    SimpleShapes.draw_rectangle(grid, value=1, conor_x=room2_x, conor_y=room2_y, width=room2_width, height=room2_height)
    
def brogue_designSymmetricalCrossRoom(grid):
    '''
    在房间中央生成两个矩形交叉而成的房间
    
    将不会生成"L"形房间
    '''
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
    SimpleShapes.draw_rectangle(grid, value=1, conor_x=room1_x, conor_y=room1_y, width=room1_width, height=room1_height)
    SimpleShapes.draw_rectangle(grid, value=1, conor_x=room2_x, conor_y=room2_y, width=room2_width, height=room2_height)


def brogue_designChunkyRoom(grid):
    '''
    生成若干连续的小圆(下面称作chunk)拼成的房间, 首个圆生成在grid中央
    '''
    fill_grid(grid, value=0)  # 以0填充所有的格子

    chunk_count = random.randint(3, 9)  # 即将生成的小圆数量
    radius = 2  # 所有小圆的半径
    
    circles = []
    
    for i in range(chunk_count):
        if i == 0:
        # 确定首个圆
            circle = {
                'x': grid.width//2, 
                'y': grid.height//2,
                'next_min_x': grid.width//2 - 3,
                'next_max_x': grid.width//2 + 3,
                'next_min_y': grid.height//2 - 3,
                'next_max_y': grid.height//2 + 3,
            }
            
        else:
            last_circle = circles[i-1]  # 拿到上一个圆的信息
            # 确定圆的位置, 必须让所有的圆的圆心落在已绘制的区域上
            while True:
                x = random.randint(last_circle['next_min_x'], last_circle['next_max_x'])
                y = random.randint(last_circle['next_min_y'], last_circle['next_max_y'])
                if grid[x,y]:
                    break
                
            
            # 确定后续的圆
            circle = {
                'x': x, 
                'y': y,
                'next_min_x': max(1, min(x-3, last_circle['next_min_x'])),
                'next_max_x': min(grid.width-2, max(x+3, last_circle['next_max_x'])),
                'next_min_y': max(1, min(y-3, last_circle['next_min_y'])),
                'next_max_y': min(grid.height-2, max(y+3, last_circle['next_max_y']))
            }
            
        # 记录本次生成的圆的信息
        circles.append(circle)
        #绘制
        SimpleShapes.draw_circle(grid, value=1, center_x=circle['x'], center_y=circle['y'], radius=radius)
