from .ladder import Ladder


class Stat:
    def __init__(self, name: str, score: int):
        self.name = name
        self.score = Ladder(score)
