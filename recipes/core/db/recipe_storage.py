from recipes import config
import recipes.core.db.models as m
import peewee as pw

class RecipeStorage(object):
    def save(self, recipes):
        m.db.init(config.database_path, pragmas={'foreign_keys': 1})
        m.create_tables()
        with m.db.atomic():
            recipe_id_structure = self.save_recipes(recipes)
            meta_key_records = self.save_meta_keys(recipe_id_structure)
            self.save_meta_fields(recipe_id_structure, meta_key_records)
            del meta_key_records
            section_structure = self.save_sections(recipe_id_structure)
            self.save_instructions(section_structure)
            ingredient_structure = self.save_ingredients(section_structure)
            del section_structure
            unit_records = self.save_unit_names(ingredient_structure)
            self.save_units(ingredient_structure, unit_records)

    def save_recipes(self, recipes):
        recipe_id_structure = []
        next_recipe_id = m.Recipe.next_auto_increment_id()

        rows = []
        for recipe in recipes:
            rows.append((next_recipe_id, recipe.get_title()))
            recipe_id_structure.append({'recipe': recipe, 'id': next_recipe_id})
            next_recipe_id += 1

        fields = [m.Recipe.id, m.Recipe.title]

        m.Recipe.insert_many(rows, fields=fields).execute()

        return recipe_id_structure

    def save_meta_keys(self, recipe_id_structure):
        meta_key_records = list(m.MetaKey.select().dicts())
        keys = set(record['key'] for record in meta_key_records)
        next_id = max((record['id'] for record in meta_key_records), default=0)

        rows = []
        for el in recipe_id_structure:
            for key in el['recipe'].get_meta_keys():
                if not key in keys:
                    rows.append((next_id, key))
                    keys.add(key)
                    meta_key_records.append({'key': key, 'id': next_id})
                    next_id += 1

        fields = [m.MetaKey.id, m.MetaKey.key]

        m.MetaKey.insert_many(rows, fields=fields).execute()

        return meta_key_records

    def save_meta_fields(self, recipe_id_structure, meta_key_records):
        meta_key_dict = {r['key']: r['id'] for r in meta_key_records}
        next_id = m.MetaField.next_auto_increment_id()

        rows = []
        for el in recipe_id_structure:
            for key, value in el['recipe'].get_meta_key_value_pairs():
                key_id = meta_key_dict[key]
                rows.append((next_id, key_id, el['id'], value))
                next_id += 1


        fields = [m.MetaField.id, m.MetaField.key, m.MetaField.recipe,
                  m.MetaField.value]

        m.MetaField.insert_many(rows, fields=fields).execute()

    def save_sections(self, recipe_id_structure):
        section_structure = []
        next_id = m.Section.next_auto_increment_id()

        rows = []
        title_rows = []
        for el in recipe_id_structure:
            for order, section in enumerate(el['recipe'].get_sections()):
                rows.append((next_id, el['id'], order))
                if section.get_title():
                    title_rows.append((next_id, section.get_title()))
                section_structure.append({'id': next_id, 'section': section})
                next_id += 1

        fields = [m.Section.id, m.Section.recipe, m.Section.order]
        title_fields = [m.SectionTitle.section, m.SectionTitle.title]

        m.Section.insert_many(rows, fields=fields).execute()
        m.SectionTitle.insert_many(title_rows, fields=title_fields).execute()

        return section_structure

    def save_instructions(self, section_structure):
        rows = []
        for el in section_structure:
            instructions = el['section'].get_instructions()
            for order, instruction in enumerate(instructions):
                rows.append((order, el['id'], instruction))

        fields = [m.Instruction.order, m.Instruction.section,
                  m.Instruction.instruction]
        m.Instruction.insert_many(rows, fields=fields).execute()

    def save_ingredients(self, section_structure):
        rows = []
        rows_amount = []
        ingredient_structure = []
        next_id = m.Ingredient.next_auto_increment_id()

        for el in section_structure:
            ingredients = el['section'].get_ingredients()
            for ingredient in ingredients:
                rows.append((next_id, el['id'], ingredient.get_name()))
                amount = ingredient.get_amount()
                if amount != None: rows_amount.append((next_id, amount))
                ingredient_info = {'id': next_id, 'ingredient': ingredient}
                ingredient_structure.append(ingredient_info)
                next_id += 1

        fields = [m.Ingredient.id, m.Ingredient.section, m.Ingredient.ingredient]
        fields_amount = [m.Amount.ingredient, m.Amount.amount]

        m.Ingredient.insert_many(rows, fields=fields).execute()
        m.Amount.insert_many(rows_amount, fields=fields_amount).execute()

        return ingredient_structure

    def save_unit_names(self, ingredient_structure):
        records = list(m.UnitName.select().dicts())
        long_dict = {r['long']: r for r in records}
        short_dict  = {r['short']:  r for r in records}
        next_id = m.UnitName.next_auto_increment_id()

        rows = []
        for el in ingredient_structure:
            short = el['ingredient'].get_shortunit() or ''
            long = el['ingredient'].get_longunit() or ''
            id_short = short and short_dict.get(short, {}).get('id')
            id_long = long and long_dict.get(long, {}).get('id')

            if isinstance(id_short, int) and isinstance(id_long, int): continue
            if isinstance(id_short, int) and not long: continue
            if isinstance(id_long, int) and not short: continue

            record = short_dict.get(short) or long_dict.get(long)
            if record:
                record['short'] = short or ''
                record['long'] = long or ''
                id = id_short or id_long
                m.UnitName.update(record).where(m.UnitName.id == id)
            else:
                record = {'id': next_id, 'long': long, 'short': short}
                if long: long_dict[long] = record
                if short: short_dict[short] = record
                rows.append(record)
                records.append(record)
                next_id += 1

        m.UnitName.insert_many(rows).execute()

        return records

    def save_units(self, ingredient_structure, unit_records):
        long_dict = {r['long']: r for r in unit_records}
        short_dict  = {r['short']:  r for r in unit_records}

        rows = []
        for el in ingredient_structure:
            short = el['ingredient'].get_shortunit() or ''
            long = el['ingredient'].get_longunit() or ''
            id_short = short and short_dict.get(short, {}).get('id')
            id_long = long and long_dict.get(long, {}).get('id')
            rows.append((el['id'], id_short or id_long or 0))

        fields = [m.Unit.ingredient, m.Unit.name]
        m.Unit.insert_many(rows, fields=fields).execute()

