import wx

from recipes.gui.form.recipe.header import RecipeHeader

class RecipeForm:
    def __init__(self, parent):
        meta_fields = {
            'tags': {'label': 'Tags'},
            'portions': {'label': 'Portions'},
            'author': {'label': 'Author'},
        }
        RecipeHeader(wx.Panel(parent), 'Hello Worlds!', meta_fields)

    def old(self):
        panel = wx.Panel(parent)
        fgs = wx.FlexGridSizer(3, 2, 10,10)

        title = wx.StaticText(panel, label = "Title")
        author = wx.StaticText(panel, label = "Name of the Author")
        review = wx.StaticText(panel, label = "Review")

        tc1 = wx.TextCtrl(panel)
        tc2 = wx.TextCtrl(panel)
        tc3 = wx.TextCtrl(panel, style = wx.TE_MULTILINE)

        fgs.AddMany([(title), (tc1, 1, wx.EXPAND),
                     (author), (tc2, 1, wx.EXPAND),
                     (review, 1, wx.EXPAND), (tc3, 1, wx.EXPAND)])
        fgs.AddGrowableRow(2, 1)
        fgs.AddGrowableCol(1, 1)
