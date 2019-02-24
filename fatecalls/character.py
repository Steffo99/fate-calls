from .ladder import Ladder
from .aspect import PermanentAspect, TemporaryAspect, Aspect, AspectList


class CharacterAspects:
    def __init__(self,
                 core: PermanentAspect,
                 other: AspectList = None):
        self.core: PermanentAspect = core
        self.other: AspectList = other if other is not None else AspectList()

    def telegramify(self) -> str:
        string = f"<b>{self.core.telegramify()}</b>\n"
        for aspect in sorted(self.other, key=lambda x: isinstance(x, TemporaryAspect)):
            string += f"{aspect.telegramify()}\n"
        return string


class CharacterApproaches:
    def __init__(self, careful: int, clever: int, flashy: int, forceful: int, quick: int, sneaky: int):
        self.careful = Ladder(careful)
        self.clever = Ladder(clever)
        self.flashy = Ladder(flashy)
        self.forceful = Ladder(forceful)
        self.quick = Ladder(quick)
        self.sneaky = Ladder(sneaky)

    def telegramify(self) -> str:
        return f"Careful: {self.careful.telegramify()}\n" \
            f"Clever: {self.clever.telegramify()}\n" \
            f"Flashy: {self.flashy.telegramify()}\n" \
            f"Forceful: {self.forceful.telegramify()}\n" \
            f"Quick: {self.quick.telegramify()}\n" \
            f"Sneaky: {self.sneaky.telegramify()}\n"


class Character:
    def __init__(self, name: str, aspects: CharacterAspects, approaches: CharacterApproaches):
        self.name: str = name
        self.aspects: CharacterAspects = aspects
        self.approaches: CharacterApproaches = approaches

    def telegramify(self) -> str:
        return f'<b>{self.name}</b>\n{self.aspects.telegramify()}\n{self.approaches.telegramify()}'
