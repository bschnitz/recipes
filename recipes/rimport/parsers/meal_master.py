import re
import itertools

class MealMaster(object):
    RE_BLOCK_START   = re.compile(r'^(-----|MMMMM).*Meal-Master')
    RE_TITLE         = re.compile(r'Title:\s*(.*\S)\s*')
    RE_CATEGORIES    = re.compile(r'Categories:\s*(.*\S)\s*')
    RE_SERVINGS      = re.compile(r'(Servings|Yield|Portions):\s*(\d+){1}\s*(.*\S){0,1}')
    RE_SECTION_TITLE = re.compile(r'([^-].*[^-])[\s-]*$')
    RE_BLANK_LINE    = re.compile(r'^\s*$')
    RE_INGREDIENTS   = re.compile(r'^\s*([ \d./]{7}) ([a-zA-Z ]{2}) \s*([^\-].*\S).*')
    RE_INGREDIENT_SECOND_COLUMN = re.compile(r'(.*)([ \d./]{7}) ([a-zA-Z ]{2}) \s*([^\-\s].*\S).*')
    RE_INGREDIENT_CONTINUATIONS = re.compile(r'^\s* {11}-+(.*)')
    RE_INGREDIENT_CONTINUATION_SECOND_COLUMN = re.compile(r'(.*) {11}-+(.*)')

    def __init__(self):
        self.separator = None
        self.recipes = []

    def parse_file(self, path):
        with open(path,'r') as file:
            while (recipe := self.read_recipe(file)):
                self.recipes.append(recipe)

    def read_recipe(self, line_iterator):
        self.parse_recipe_lines(self.read_recipe_lines(line_iterator))

    def read_recipe_lines(self, line_iterator):
        first_line = self.read_until_block_start(line_iterator)
        if not first_line: return []

        lines = [first_line]

        while (line := next(line_iterator)) and not self.is_block_end(line):
            lines.append(line)

        return lines

    def read_until_block_start(self, line_iterator):
        while (line := next(line_iterator)):
            self.separator = self.block_start(line)
            if self.separator:
                return line

    def parse_recipe_lines(self, recipe_lines):
        if not recipe_lines: return

        header, rest              = self.parse_header(recipe_lines)
        ingredient_sections, rest = self.parse_ingredient_sections(rest)
        instruction_sections      = self.parse_instruction_sections(rest)
        print(header)
        print(ingredient_sections)
        print(instruction_sections)
        exit(1) # TODO
        #recipe(header, ingredient_sections, instruction_sections)

    def parse_header(self, lines):
        _, title, rest      = self.split_lines(lines, self.title)
        _, categories, rest = self.split_lines(rest,  self.categories)
        _, servings, rest   = self.split_lines(rest,  self.servings)

        header = { 'title': title,
                   'categories': categories,
                   'servings': servings }

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
        i_section_start = self.find_index(lines, self.ingredient_section_start)

        if not i_section_start: return [None, None]

        section_start_line = lines[i_section_start]
        title = self.section_title(section_start_line)

        # found a section title, but it actually was no ingredient section
        if title and not self.find_index(lines, self.ingredients):
            return [None, None]

        # found an ingredient section title, ingredient lines will follow
        if title: _, title, lines = self.split_lines(lines, self.section_title)

        ingredients, rest = self.parse_ingredient_lines(lines)

        return [{ title: title, ingredients: ingredients }, rest]

    def parse_ingredient_lines(self, lines):
        ingredients = []

        while True:
            lines = self.skip_blank_lines(lines)
            ingredient, lines = self.parse_ingredient_line_and_continuations(lines)

            if not ingredient: break

            ingredients.append(ingredient)

        return [ingredients, lines]

    def parse_ingredient_line_and_continuations(self, lines):
        _, ingredients, rest = self.split_lines(lines, self.ingredients)

        if not ingredients: return [None, lines]

        continuations, rest = self.parse_ingredient_continuations(rest)
        ingredients = self.merge_ingredients_with_continuations(ingredients, continuations)
        return [ingredients, rest]

    def parse_ingredient_continuations(self, lines):
        continuations = []

        index = 0
        for index, line in enumerate(lines):
            continuation = self.ingredient_continuations(line)
            if not continuation: break
            continuations.append(continuation)

        return [continuations, lines[index:]]

    def merge_ingredients_with_continuations(self, ingredients, continuations):
        for continuation in continuations:
            for index, ingredient in enumerate(ingredients):
                ingredient['ingredient'] += ' ' + continuation[index]

        return ingredients

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
        return [i.strip() for i in instructions]

    # ---- function for detecting and extracting from Meal-Master syntax

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

    def servings(self, line):
        servings = re.search(self.RE_SERVINGS, line)

        if servings: return { 'amount': servings[2], 'unit': servings[3] }

    def section_title(self, line):
        if not line.startswith(self.separator): return

        match = line[len(self.separator):].search(self.RE_SECTION_TITLE)
        if match: return match[1].strip()

    def ingredient_second_column(self, text):
        match = re.search(self.RE_INGREDIENT_SECOND_COLUMN, text)

        if match:
            second = { 'amount': match[2].strip(),
                       'unit': match[3].strip(),
                       'ingredient': match[4] }
            return [ match[1], second ]
        return [None, None]

    def ingredients(self, line):
        match = re.search(self.RE_INGREDIENTS, line)

        if not match: return

        rest, second = self.ingredient_second_column(match[3])

        first = { 'amount': match[1].strip,
                  'unit': match[2].strip,
                  'ingredient': rest or match[3] }

        return [first, second]

    def ingredient_section_start(self, line):
        return self.section_title(line) or self.ingredients(line)

    def ingredient_continuations(self, line):
        match = re.search(self.RE_INGREDIENT_CONTINUATIONS, line)

        if match:
            continuation = self.ingredient_continuation_second_column(match[1])
            return  continuation or [match[1].strip()]

    def ingredient_continuation_second_column(self, text):
        match = re.search(self.RE_INGREDIENT_CONTINUATION_SECOND_COLUMN, text)

        if match: return [match[1].strip(), match[2].strip()]

    def is_blank(self, line):
        re.search(self.RE_BLANK_LINE, line)

    # ---- utility functions

    def split_lines(self, lines, splitter):
        for index, item in enumerate(lines):
            result = splitter(item)
            if result:
                return [lines[0:index], result, lines[index+1:]]
        return [None, None, None]

    def partition_until(self, items, condition_callback):
        before = []
        index = 0
        for index, item in enumerate(items):
            if condition_callback(item): break
            before.append(item)

        return [before, items[index:]]

    def skip_blank_lines(self, lines):
        return list(itertools.dropwhile(self.is_blank, lines))

    def find_index(self, haystack, needle_callback):
        for index, item in enumerate(haystack):
            if needle_callback(item): return index
