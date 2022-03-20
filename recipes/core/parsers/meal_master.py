import re
import json
import itertools
from charset_normalizer import from_path

from recipes.core.util.recipe import Recipe
from chardet.universaldetector import UniversalDetector

class FileLineIterator(object):
    def __init__(self, path, encoding='utf-8'):
        self.encoding = encoding
        self.path = path
        self.file = None
    def __enter__(self):
        if self.encoding == 'auto':
            return iter(str(from_path(self.path).best()).splitlines())
        else:
            self.file = open(self.path,'r', encoding=self.encoding)
            return self.file
    def __exit__(self, type, value, traceback):
        if self.file != None:
            self.file.close()

class MealMaster(object):
    RE_BLOCK_START    = re.compile(r'^(-----|MMMMM).*Meal-Master')
    RE_TITLE          = re.compile(r'Title:\s*(.*\S)\s*')
    RE_CATEGORIES     = re.compile(r'Categories:\s*(.*\S)\s*')
    RE_SERVINGS       = re.compile(r'(Servings|Yield|Portions):\s*(\d+){1}\s*(.*\S){0,1}')
    RE_SECTION_TITLE  = re.compile(r'([^-].*[^-\s])[\s-]*$')
    RE_BLANK_LINE     = re.compile(r'^\s*$')
    RE_INGREDIENT     = re.compile(r'^\s*([ \d./]{7}) ([a-zA-Z ]{2}) \s*(.*\S).*')
    RE_INGREDIENT_SECOND_COLUMN = re.compile(r'(.*)([ \d./]{7}) ([a-zA-Z ]{2}) \s*([^\-\s].*\S).*')
    RE_INGREDIENT_CONTINUATIONS = re.compile(r'^\s* {11}-+(.*)')
    RE_INGREDIENT_CONTINUATION_SECOND_COLUMN = re.compile(r'(.*) {11}-+(.*)')

    def __init__(self):
        self.separator = None
        self.original_recipes = []
        self.recipes = []

    def parse_file(self, path, encoding='utf-8'):
        with FileLineIterator(path, encoding) as lines:
            while (recipe := self.read_recipe(lines)):
                self.recipes.append(recipe)

    def read_recipe(self, line_iterator):
        lines = self.read_recipe_lines(line_iterator)
        if lines: self.original_recipes.append('\n'.join(lines))
        return self.parse_recipe_lines(lines)

    def read_recipe_lines(self, line_iterator):
        first_line = self.read_until_block_start(line_iterator)
        if not first_line: return []

        lines = [first_line]

        while True:
            line = next(line_iterator, None)

            if line == None or self.is_block_end(line): break

            lines.append(line)

        return lines

    def read_until_block_start(self, line_iterator):
        while (line := next(line_iterator, None)):
            self.separator = self.block_start(line)
            if self.separator:
                return line

    def parse_recipe_lines(self, recipe_lines):
        if not recipe_lines: return

        header, rest              = self.parse_header(recipe_lines)
        ingredient_sections, rest = self.parse_ingredient_sections(rest)
        instruction_sections      = self.parse_instruction_sections(rest)
        return self.create_recipe(header, ingredient_sections, instruction_sections)

    def parse_header(self, lines):
        _, title, rest      = self.split_lines(lines, self.title)
        _, categories, rest = self.split_lines(rest,  self.categories)
        _, portions, rest   = self.split_lines(rest,  self.portions)
        if not portions: portions = { 'unit': 'portions', 'amount': 0 }

        header = { 'title': title,
                   'categories': categories,
                   portions['unit']: portions['amount'] }

        return [header, rest]

    def parse_ingredient_sections(self, lines):
        sections = []

        while True:
          section, rest = self.parse_ingredient_section(lines)

          if not section: break

          lines = rest
          sections.append(section)

        return [sections, lines]

    def parse_ingredient_section(self, lines):
        title, lines = self.find_ingredient_section_start(lines)

        if not lines: return [None, None]

        ingredients, rest = self.parse_ingredient_lines(lines)

        return [{ 'title': title, 'ingredients': ingredients }, rest]

    def find_ingredient_section_start(self, lines):
        lines = self.skip_blank_lines(lines)

        if not lines: return [None, None]

        title = self.section_title(lines[0])
        if title: lines = self.skip_blank_lines(lines[1:])

        if not self.ingredient(lines[0]): return [None, None]

        return title, lines

    def parse_ingredient_lines(self, lines):
        ingredient_columns, rest = self.collect_ingredient_columns(lines)
        ingredients = self.merge_ingredient_columns(ingredient_columns)
        return [ingredients, rest]

    def merge_ingredient_columns(self, columns):
        ingredient_lines = columns[0] + columns[1]
        ingredients = []
        ingredient = ingredient_lines.pop(0)
        for line in ingredient_lines:
            if line.get('continuation'):
                ingredient['name'] += ' ' + line['continuation']
            else:
                ingredients.append(ingredient)
                ingredient = line
        ingredients.append(ingredient)
        return ingredients


    def collect_ingredient_columns(self, lines):
        columns = [[], []]
        for index, line in enumerate(lines):
            if self.is_blank(line): continue

            ingredient_columns = self.ingredient_columns(line)

            if not ingredient_columns: return [columns, lines[index:]]

            for icol in [0, 1]:
                if ingredient_columns[icol]:
                    columns[icol].append(ingredient_columns[icol])

        return [columns, []]

    def ingredient_columns(self, line):
        first, rest = self.ingredient_first_column(line)

        if first == None: return None

        name, second = self.ingredient_second_column(rest)

        if len(first) == 0: first['continuation'] = name
        else:               first['name']         = name

        return [first, second]

    def ingredient_first_column(self, line):
        continuation = self.ingredient_continuation(line)
        if continuation: return [{}, continuation]

        ingredient = self.ingredient(line)

        if ingredient == None: return [None, None]

        amount, unit, rest = ingredient

        return [{'amount': amount, 'shortunit': unit}, rest]

    def ingredient_second_column(self, string):
        first, continuation = self.ingredient_continuation_second_column(string)
        if continuation != None: return [first, {'continuation': continuation}]

        match = re.search(self.RE_INGREDIENT_SECOND_COLUMN, string)
        if not match: return [string, None]

        second = { 'amount': match[2].strip(),
                   'shortunit': match[3].strip(),
                   'name': match[4] }
        return [ match[1].strip(), second ]

    def parse_instruction_sections(self, lines):
        lines = self.skip_blank_lines(lines)

        if not lines: return []

        title = self.section_title(lines[0])
        title and lines.pop(0)

        instructions, rest = self.partition_until(lines, self.section_title)
        instructions = self.parse_instructions(instructions)

        section = [{ 'title': title, 'instructions': instructions }]
        return section + self.parse_instruction_sections(rest)

    def parse_instructions(self, instructions):
        instructions.reverse
        instructions = self.skip_blank_lines(instructions)
        itertools.dropwhile(self.is_block_end, instructions)
        instructions.reverse
        return self.merge_split_instructions(instructions)

    def merge_split_instructions(self, instructions):
        merged_instructions = []
        paragraph = ''
        for line in instructions:
            line = line.strip(' \n\t')
            if self.is_blank(line):
                merged_instructions.append(paragraph)
                paragraph = ''
                continue
            paragraph = paragraph + ' ' + line if paragraph else line
        if paragraph: merged_instructions.append(paragraph)
        return merged_instructions

    # ---- function for detecting and extracting from Meal-Master syntax

    def ingredient_continuation_second_column(self, text):
        match = re.search(self.RE_INGREDIENT_CONTINUATION_SECOND_COLUMN, text)

        if match: return [match[1].strip(), match[2].strip()]

        return [None, None]

    def ingredient(self, line):
        match = re.search(self.RE_INGREDIENT, line)

        if not match: return None

        return [match[1].strip(), match[2].strip(), match[3].strip()]

    def ingredient_continuation(self, line):
        match = re.search(self.RE_INGREDIENT_CONTINUATIONS, line)

        if match: return match[1]

        return None

    # start of a recipe block (block = one whole recipe) returns the separator
    def block_start(self, line):
        match = re.match(self.RE_BLOCK_START, line)
        if match: return match[1]

    # end of a recipe block (block = one whole recipe)
    def is_block_end(self, line):
        if not line.startswith(self.separator): return

        return re.match(rf"{re.escape(self.separator)}\s*$", line)

    def title(self, line):
        match = re.search(self.RE_TITLE, line)
        if match: return match[1]

    def categories(self, line):
        match = re.search(self.RE_CATEGORIES, line)
        if match: return [c.strip() for c in match[1].split(',')]

    def portions(self, line):
        portions = re.search(self.RE_SERVINGS, line)

        if portions: return { 'amount': portions[2], 'unit': portions[1] }

    def section_title(self, line):
        if not line.startswith(self.separator): return

        match = re.search(self.RE_SECTION_TITLE, line[len(self.separator):])
        if match: return match[1].strip()

    def check_ingredient_section_start(self, line):
        return self.section_title(line) or self.ingredient(line)

    def is_blank(self, line):
        return re.search(self.RE_BLANK_LINE, line)

    # ---- utility functions

    def split_lines(self, lines, splitter):
        for index, item in enumerate(lines):
            result = splitter(item)
            if result:
                return [lines[0:index], result, lines[index+1:]]
        return [None, None, None]

    def partition_until(self, items, condition_callback):
        before = []
        for index, item in enumerate(items):
            if condition_callback(item): return [before, items[index:]]
            before.append(item)

        return [before, []]

    def skip_blank_lines(self, lines):
        return list(itertools.dropwhile(self.is_blank, lines))

    def find_index(self, haystack, needle_callback):
        for index, item in enumerate(haystack):
            if needle_callback(item): return index

    def create_recipe(self, header, ingredient_sections, instruction_sections):
        title = header.pop('title')
        recipe = Recipe(title)

        recipe.set_meta_fields(header)

        for ingredient_section in ingredient_sections:
            section = recipe.append_section(ingredient_section['title'])
            for ingredient in ingredient_section['ingredients']:
                section.append_ingredient(**ingredient)

        for instruction_section in instruction_sections:
            section = recipe.append_section(instruction_section['title'])
            section.set_instructions(instruction_section['instructions'])

        return recipe
