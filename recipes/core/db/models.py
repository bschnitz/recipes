import peewee as pw

db = pw.SqliteDatabase(None)

# important: enforce foreign_keys for sqlite, otherwise ON DELETE
# behaviour will be ignored
# db = pw.SqliteDatabase('tests.db', pragmas={'foreign_keys': 1})

# one BaseModel ensures, that all other models will have the same Meta class and
# thus the same settings, database
class BaseModel(pw.Model):
    class Meta:
        database = db

        # better table naming (camelcase to underscore)
        legacy_table_names=False

    @classmethod
    def next_auto_increment_id(cls):
        id = cls.select(pw.fn.MAX(cls.id)).scalar()
        return 0 if id == None else id + 1

class Recipe(BaseModel):
    title = pw.CharField()

class MetaKey(BaseModel):
    key = pw.CharField(unique=True)

class MetaField(BaseModel):
    key = pw.ForeignKeyField(MetaKey, backref='fields')
    recipe = pw.ForeignKeyField(Recipe, backref='fields')
    value = pw.CharField()

class Section(BaseModel):
    recipe = pw.ForeignKeyField(Recipe, backref='sections')
    order = pw.SmallIntegerField()

class SectionTitle(BaseModel):
    section = pw.ForeignKeyField(Section, backref='title', primary_key=True)
    title = pw.CharField()

class Ingredient(BaseModel):
    section = pw.ForeignKeyField(Section, backref='ingredients')
    ingredient = pw.CharField()

class Amount(BaseModel):
    ingredient = pw.ForeignKeyField(Ingredient, backref='amount', primary_key=True)
    amount = pw.FloatField()

class UnitName(BaseModel):
    short = pw.FixedCharField(max_length=2)
    long = pw.CharField()

class Unit(BaseModel):
    ingredient = pw.ForeignKeyField(Ingredient, backref='unit', primary_key=True)
    name = pw.ForeignKeyField(UnitName, backref='units')

class Instruction(BaseModel):
    section = pw.ForeignKeyField(Section, backref='instructions')
    order = pw.SmallIntegerField()
    instruction = pw.CharField()

    class Meta:
        primary_key = pw.CompositeKey('section', 'order')

def create_tables():
    db.create_tables([Recipe, MetaKey, MetaField, Section, SectionTitle,
                      Ingredient, Amount, UnitName, Unit, Instruction])
