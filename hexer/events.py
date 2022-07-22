class Event:
    def __init__(self):
        self._subscribers = []

    def __iadd__(self, fun):
        self._subscribers.append(fun)
        return self

    def __isub__(self, fun):
        self._subscribers.remove(fun)
        return self

    def __call__(self, *args, **kwargs):
        for fun in self._subscribers:
            fun(*args, **kwargs)