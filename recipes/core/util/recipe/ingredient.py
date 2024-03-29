class Ingredient(object):
    def __init__(self, name, amount=None, longunit=None, shortunit=None):
        self.name = name
        self.amount = amount
        self.shortunit = shortunit
        self.longunit = longunit

    def to_list(self, include_shortunit = True, include_longunit = False):
        unit = []
        if include_shortunit: unit.append(self.shortunit or '')
        if include_longunit: unit.append(self.longunit or '')
        return [self.amount or '', *unit, self.name]

    def get_name(self):
        return self.name

    def get_amount(self):
        return self.amount

    def get_shortunit(self):
        return self.shortunit

    def get_longunit(self):
        return self.longunit
