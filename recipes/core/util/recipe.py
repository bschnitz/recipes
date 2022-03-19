import yaml

class Recipe(object):
    def __init__(self, header, ingredient_sections, instruction_sections):
        self.recipe = {
            'header': header,
            'ingredients': {
                'sections': ingredient_sections
            },
            'instructions': {
                'sections': instruction_sections
            },
        }

    def to_yaml(self):
        return yaml.dump(self.recipe, default_flow_style = False, allow_unicode = True)

    def __str__(self):
        return f'## {self.recipe["header"]["title"]}\n\n' + \
            self.header_to_str() + \
            self.ingredients_to_str() + \
            self.instructions_to_str()

    def header_to_str(self):
        header_str = ''

        for key in self.recipe['header']:
            if key == 'title': continue

            value = self.recipe["header"][key]
            if isinstance(value, list): value = ', '.join(value)
            header_str += f'{key}: {value}\n'

        return header_str + '\n'

    def ingredients_to_str(self):
        ingredients_str = '### Ingredients\n\n'

        for section in self.recipe['ingredients']['sections']:
            ingredients_str += self.ingredient_section_to_str(section)

        return ingredients_str

    def ingredient_section_to_str(self, section):
        section_str = ''

        if section['title']:
            section_str += f'#### {section["title"]}\n\n'


        i_to_list = lambda i: [i['amount'], i['unit'], i['ingredient']]
        ingredients = list(map(i_to_list, section['ingredients']))
        header = ['Amount', 'Unit', 'Ingredient']
        ingredients.insert(0, header)

        return section_str + self.list_to_table_str(ingredients) + '\n\n'

    def list_to_table_str(self, lst):
        if len(lst) == 0: return ''

        ncols = len(lst[0])
        colsizes = [0] * ncols

        for row in lst:
            for icol in range(ncols):
                colsizes[icol] = max(colsizes[icol], len(row[icol]))

        lines = []
        for row in lst:
            line = '|'
            for icol in range(ncols):
                line += row[icol].ljust(colsizes[icol], ' ') + '|'
            lines.append(line)
        header_sep = '|' + '|'.join(map(lambda n: '-'*n, colsizes)) + '|'
        lines.insert(1, header_sep)

        return '\n'.join(lines)

    def instructions_to_str(self):
        instructions_str = '### Instructions\n\n'

        for section in self.recipe['instructions']['sections']:
            instructions_str += self.instruction_section_to_str(section)

        return instructions_str

    def instruction_section_to_str(self, section):
        section_str = ''

        if section['title']:
            section_str += f'#### {section["title"]}\n\n'

        section_str += '\n\n'.join(section["instructions"])

        return section_str
