from .stat import Stat
from .aspect import PermanentAspect, TemporaryAspect, Aspect, AspectList


class CharacterAspects:
    def __init__(self,
                 core: PermanentAspect,
                 other: AspectList = None):
        self.core: PermanentAspect = core
        self.other: AspectList = other if other is not None else AspectList()


class CharacterApproaches:
    def __init__(self, careful: int, clever: int, flashy: int, forceful: int, quick: int, sneaky: int):
        self.careful = Stat("Careful", careful)
        self.clever = Stat("Clever", clever)
        self.flashy = Stat("Flashy", flashy)
        self.forceful = Stat("Forceful", forceful)
        self.quick = Stat("Quick", quick)
        self.sneaky = Stat("Sneaky", sneaky)


class Character:
    def __init__(self, aspects: CharacterAspects, approaches: CharacterApproaches, player):
        self.aspects: CharacterAspects = aspects
        self.approaches: CharacterApproaches = approaches
        self.player = player


class CharacterList(list):
    def played_by(self, player) -> "CharacterList":
        return CharacterList([character for character in self if character.player == player])
