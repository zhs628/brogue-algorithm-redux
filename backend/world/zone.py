from array2d import array2d
from linalg import vec2i

class CellEx:
    def __init__(self) -> None:
        self.actor = None   # 单位，如NPC、怪物
        self.effects = []   # 气体、火焰等效果

class Zone:
    def __init__(self, width: int, height: int):
        # 地形
        self.m_terrain = array2d[int](width, height, default=0)
        # 地表装饰物
        self.m_deco = array2d[int](width, height, default=0)
        # 房间或走廊索引
        self.m_room = array2d[int](width, height, default=0)

        ####### 稀疏数据 ########
        self.extras = {}    # type: dict[vec2i, CellEx]
