class AgentID(object):
    instance = None
    counter = 0

    def __new__(cls):
        if cls.instance is None:
            obj = object.__new__(cls)
            cls.instance = obj
        return cls.instance

    def generate(self):
        self.counter += 1
        return self.counter

