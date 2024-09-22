from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..unit import Unit

class Game:
    def __init__(self) -> None:
        self.step_count = 0

    def begin(self) -> None:
        pass

    def step(self) -> None:
        # determine the next unit to act
        # 1. the unit with the smallest time acts first
        # 2. if multiple units have the same time, the unit with the highest priority acts first
        all_units: list[Unit] = []
        unit = min(all_units, key=lambda u: (u.time, -u.priority))
        cmd = unit.get_input()
        self.step_count += 1

    def end(self) -> None:
        pass