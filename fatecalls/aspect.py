class Aspect:
    def __init__(self, name):
        self.name = name

    def telegramify(self) -> str:
        raise NotImplementedError()


class TemporaryAspect(Aspect):
    def telegramify(self):
        return f"<i>{self.name}</i>"


class PermanentAspect(Aspect):
    def telegramify(self):
        return f"{self.name}"


class AspectList(list):
    def clean(self):
        for aspect in self.copy():
            if isinstance(aspect, TemporaryAspect):
                self.remove(aspect)
