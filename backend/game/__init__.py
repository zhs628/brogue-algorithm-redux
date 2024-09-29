from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..unit import Unit

class Game:
    def on_begin(self) -> None:
        pass

    def on_end(self) -> None:
        pass
    
    def on_unit_turn(self, unit: 'Unit') -> None:
        pass

    def on_unit_command(self, unit: 'Unit', cmd: 'Command') -> None:
        pass
    
    def get_units(self) -> list[Unit]:
        raise NotImplementedError

    def __iter__(self):
        return self

    def __next__(self):
        self.on_begin()

        while True:
            # determine the next unit to act
            # 1. the unit with the smallest time acts first
            # 2. if multiple units have the same time, the unit with the highest priority acts first
            unit = min(self.get_units(), key=lambda u: (u.time, -u.priority))

            # wait for the unit to be ready
            while not unit.is_ready():
                yield

            self.on_unit_turn(unit)

            # wait for the unit to submit a command
            cmd = unit.get_input()
            if cmd is None:
                cmd = yield from unit.get_input_async()

            self.on_unit_command(unit, cmd)

            # execute the command
            duration = yield from cmd.execute()
            cmd.invoker.time += duration
