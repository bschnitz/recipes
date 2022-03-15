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
