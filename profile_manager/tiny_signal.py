import weakref

class TinySignal:
    def __init__(self):
        self._slots = []

    def bind(self, slot, _from):
        ref = weakref.WeakMethod(slot) if hasattr(slot, "__self__") else slot
        self._slots.append((ref, _from))

    def emit(self, *args, **kwargs):
        alive = []
        results = {}
        for idx, s in enumerate(self._slots):
            fn = s[0]() if isinstance(s[0], weakref.WeakMethod) else s[0]
            if fn:
                res = fn(*args, **kwargs)
                results[s[1]] = res

                alive.append(s)
        self._slots = alive  
        return results