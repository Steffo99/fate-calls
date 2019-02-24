from enum import IntEnum


class Ladder(IntEnum):
    Atrocious = -4
    Embarassing = -3
    Terrible = -2
    Poor = -1
    Mediocre = 0
    Average = 1
    Fair = 2
    Good = 3
    Great = 4
    Superb = 5
    Fantastic = 6
    Epic = 7
    Legendary = 8
    Impossible = 9

    def telegramify(self):
        return f"<b>{self.name}</b> ({self.number()})"

    def number(self):
        if self.value > 0:
            return f"+{self.value}"
        else:
            return self.value
