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
        scrolled_window = wx.ScrolledWindow(parent)

        header = wx.Panel(scrolled_window)
        ingredients = wx.Panel(scrolled_window)

        RecipeHeader(header, 'Hello Worlds!', meta_fields)
        IngredientSection(ingredients)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(header, 0, wx.EXPAND|wx.ALIGN_TOP)
        vbox.Add(ingredients, 0, wx.EXPAND|wx.ALIGN_TOP)
        scrolled_window.SetSizer(vbox)
        fontsz = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT).GetPixelSize()
        scrolled_window.SetScrollRate(fontsz.x, fontsz.y)
        scrolled_window.EnableScrolling(True,True)
