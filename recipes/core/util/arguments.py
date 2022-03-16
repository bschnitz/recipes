class Arguments(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def soft_set(self, index, key, value):
        if len(self.args) > index: return
        if key in self.kwargs: return
        self.kwargs[key] = value
