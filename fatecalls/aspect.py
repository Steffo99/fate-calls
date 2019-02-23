class Aspect:
    def __init__(self, name):
        self.name = name


class TemporaryAspect(Aspect):
    pass


class PermanentAspect(Aspect):
    pass


class AspectList(list):
    def clean(self):
        for aspect in self.copy():
            if isinstance(aspect, TemporaryAspect):
                self.remove(aspect)
