import wx

from recipes.gui.form.recipe.header import RecipeHeader
from recipes.gui.form.recipe.ingredients import IngredientSection

class RecipeForm:
    def __init__(self, parent):
        meta_fields = {
            'tags': {'label': 'Tags', 'value': 'tags'},
            'portions': {'label': 'Portions', 'value': 'portions'},
            'author': {'label': 'Author', 'value': 'author'},
        }

        header = wx.Panel(parent)
        ingredients = wx.Panel(parent)

        RecipeHeader(header, 'Hello Worlds!', meta_fields)
        IngredientSection(ingredients)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(header, 1, wx.EXPAND)
        vbox.Add(ingredients, 1, wx.EXPAND)
        parent.SetSizer(vbox)
