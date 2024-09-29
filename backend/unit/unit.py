from linalg import vec2i
from typing import Any, Generator

class Command:
    def __init__(self, invoker: 'Unit') -> None:
        self.invoker = invoker

    def execute(self) -> Generator[None, Any, int]:
        raise NotImplementedError

class Unit:
    PRIORITY_VFX = 100          # visual effects take priority
    PRIORITY_HERO = 0           # positive is before hero, negative after
    PRIORITY_BLOB = -10         # blobs act after hero, before mobs
    PRIORITY_MOB = -20          # mobs act between buffs and blobs
    PRIORITY_BUFF = -30         # buffs act last in a turn
    PRIORITY_DEFAULT = -100     # if no priority is given, act after all else

    def __init__(self) -> None:
        self.time = 0              # 时间轴计数
        self.time_scale = 100      # 时间轴缩放（百分比定点数）
        self.priority = Unit.PRIORITY_DEFAULT   # 回合优先级

    def get_input(self) -> Command | None:
        return
    
    def get_input_async(self) -> Generator[None, Any, Command]:
        raise NotImplementedError
    
    def is_ready(self) -> bool:
        return True


class Actor(Unit):
    def __init__(self) -> None:
        super().__init__()

        self.pos = vec2i(0, 0)      # 左上角坐标
        self.size = vec2i(1, 1)     # 尺寸
        self.hp = vec2i(100, 100)   # 生命值
        self.mp = vec2i(0, 0)       # 法力值

        self.is_entity = False      # 是否实体，实体将被视为碰撞体