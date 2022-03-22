import textwrap
from recipes.core import util
from .ingredient import Ingredient

class Section(object):
    def __init__(self, title=None):
        self.title = title
        self.ingredients = []
        self.instructions = []

    def get_title(self):
        return self.title

    def get_instructions(self):
        return self.instructions

    def get_ingredients(self):
        return self.ingredients

    def append_ingredient(self, name, amount=None, longunit=None, shortunit=None):
        self.ingredients.append(Ingredient(name, amount, longunit, shortunit))

    def set_instructions(self, instructions):
        self.instructions = instructions

    def str(self, wrap_at=0):
        ingredients_str = self.ingredients_to_str()
        instructions_str = self.instructions_to_str(wrap_at)
        parts = [self.title_to_str(), ingredients_str, instructions_str]
        return '\n\n'.join(filter(lambda part: part, parts))

    def title_to_str(self):
        if not self.title: return ''

        return f'#### {self.title}'

    def ingredients_to_str(self):
        header = ['Amount', 'Unit', 'Ingredient']
        rows = [ingredient.to_list() for ingredient in self.ingredients]

        if not rows: return

        return util.markdown_table_str([header, *rows])

    def instructions_to_str(self, wrap_at):
        paragraphs = self.instructions
        if wrap_at: paragraphs = [textwrap.fill(p) for p in paragraphs]
        return '\n\n'.join(paragraphs)
