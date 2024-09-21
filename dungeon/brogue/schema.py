from array2d import array2d
from linalg import vec2i

class GridExtras:
    def __init__(self) -> None:
        self.unit = None            # 单位，如NPC、怪物
        self.decoration = None      # 地表装饰物，如粘液
        self.effects = []           # 气体、火焰等效果

class Dungeon:
    def __init__(self, width: int, height: int):
        # 地形
        self.m_terrain = array2d[int](width, height, default=0)
        # 房间和走廊
        self.m_room = array2d[int](width, height, default=0)

        ####### 稀疏数据 ########
        self.extras = {}    # type: dict[vec2i, GridExtras]
