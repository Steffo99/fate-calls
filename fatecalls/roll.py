import random
from .ladder import Ladder


class Roll:
    def __init__(self):
        self.result = random.randint(-1, 1)


class Fate:
    total_rolls = 4

    def __init__(self, bonus: Ladder = Ladder(0)):
        self.rolls = [Roll() for _ in range(self.total_rolls)]
        self.bonus = bonus

    @property
    def rolled(self):
        total = 0
        for roll in self.rolls:
            total += roll.result
        return Ladder(total)

    @property
    def result(self):
        total = self.bonus
        for roll in self.rolls:
            total += roll.result
        return Ladder(total)

    def telegramify(self) -> str:
        string = ""
        for roll in self.rolls:
            if roll.result == -1:
                string += "🔴"
            elif roll.result == 0:
                string += "⚫️"
            else:
                string += "🔵"
        string += f" ({self.rolled.number()}) + {self.bonus.telegramify()} = {self.result.telegramify()}"
        return string
