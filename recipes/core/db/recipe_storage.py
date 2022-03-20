from recipes import config
import recipes.core.db.models as m
import peewee as pw

class RecipeStorage(object):
    def save(self):
        m.db.init(config.database_path, pragmas={'foreign_keys': 1})
