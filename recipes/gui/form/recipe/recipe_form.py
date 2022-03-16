import wx

from recipes.gui.form.recipe.header import RecipeHeader
from recipes.gui.form.recipe.ingredients import IngredientSection
from recipes.gui.form.recipe.instructions import InstructionSection

class RecipeForm(wx.ScrolledWindow):
    def __init__(self, parent):
        super().__init__(parent)

        meta_fields = {
            'tags': {'label': 'Tags', 'value': 'tags'},
            'portions': {'label': 'Portions', 'value': 'portions'},
            'author': {'label': 'Author', 'value': 'author'},
        }

        header = wx.Panel(self)
        ingredients = wx.Panel(self)
        instructions = wx.Panel(self)

        RecipeHeader(header, 'Hello Worlds!', meta_fields)
        IngredientSection(ingredients)
        InstructionSection(instructions)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(header, 0, wx.EXPAND|wx.ALIGN_TOP)
        vbox.Add(ingredients, 0, wx.EXPAND|wx.ALIGN_TOP)
        vbox.Add(instructions, 0, wx.EXPAND|wx.ALIGN_TOP)

        self.SetSizer(vbox)
        fontsz = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT).GetPixelSize()
        self.SetScrollRate(fontsz.x, fontsz.y)
        self.EnableScrolling(True,True)
