import textwrap
from .section import Section

class Recipe(object):
    def __init__(self, title):
        self.title = title
        self.meta_fields = {}
        self.sections = []

    def set_meta_fields(self, meta_fields):
        self.meta_fields = meta_fields

    def get_meta_keys(self):
        return self.meta_fields.keys()

    def get_meta_values(self, key):
        value = self.meta_fields[key]
        return value if isinstance(value, list) else [value]

    def get_meta_key_value_pairs(self):
        pairs = []
        for key in self.get_meta_keys():
            for value in self.get_meta_values(key):
                pairs.append((key, value))
        return pairs

    def append_section(self, title=None):
        section = Section(title)
        self.sections.append(section)
        return section

    def __str__(self):
        return self.str()

    def str(self, wrap_at=0):
        sections_str = '\n\n'.join([s.str(wrap_at) for s in self.sections])
        parts = [self.title_to_str(), self.meta_fields_to_str(), sections_str]
        return '\n\n'.join(filter(lambda part: part, parts))

    def title_to_str(self):
        return f'## {self.title}'

    def meta_fields_to_str(self):
        make_lines = lambda k: self.meta_field_to_str(k, self.meta_fields[k])
        return '\n'.join(map(make_lines, self.meta_fields))

    def meta_field_to_str(self, key, value):
        if isinstance(value, list): value = ', '.join(value)
        return f'{key}: {value}'

    def get_title(self):
        return self.title

    def get_sections(self):
        return self.sections
