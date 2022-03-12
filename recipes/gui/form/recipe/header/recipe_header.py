import wx
import math
from recipes.gui.form.framework import RowWiseForm
from recipes.gui.form.framework import TitleBox
from recipes.gui.form.framework import PaddedBox
from recipes.gui.form.recipe.header import RecipeHeaderRowFactory
from recipes.gui.fonts import Head1

class RecipeHeader:
    def __init__(self, parent, title, meta = {}):
        self.parent = parent
        self.form = RowWiseForm(parent, RecipeHeaderRowFactory)
        self.form.append_attribute('Title', title)

        # label and input for all other meta fields
        for key in meta:
            label = meta[key]['label']
            value = meta[key].get('value', '')
            self.form.append_attribute(label, value)

        choices = ['blue', 'yellow', 'green', 'very long option']
        self.form.append_combo(choices, self.onAddMeta)

        titled_box = TitleBox(self.form.create_grid(), parent, title, Head1())
        parent.SetSizer(PaddedBox(titled_box))
        self.form.fgs.AddGrowableCol(1)

    def box(self, title, element):
        font = Head1()
        font_height = font.GetPixelSize()[1]

        title = wx.StaticText(self.parent, label=title)
        title.SetFont(font)

        box = wx.BoxSizer(orient=wx.VERTICAL)
        box.Add(title, flag=wx.BOTTOM|wx.EXPAND, border=math.floor(font_height*0.3))
        box.Add(element, flag=wx.EXPAND)

        return box

    def onAddMeta(self, event, combobox):
        self.form.insert_attribute(-1, combobox.GetValue(), combobox.GetValue())
        self.parent.GetParent().Layout()
