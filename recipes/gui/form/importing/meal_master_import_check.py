import wx

class MealMasterImportCheck(wx.Panel):
    def __init__(self, parent, original_recipes, imported_recipes):
        super().__init__(parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        for i, original_recipe in enumerate(original_recipes):
            imported_recipe = str(imported_recipes[i])
            box = self.create_comparison_box(original_recipe, imported_recipe)
            vbox.Add(box, 1, wx.EXPAND|wx.ALIGN_TOP)
        self.SetSizer(vbox)

    def create_comparison_box(self, original_recipe, imported_recipe):
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(self.textfield(original_recipe), 1, wx.EXPAND|wx.ALIGN_TOP)
        vbox.Add(self.textfield(imported_recipe), 1, wx.EXPAND|wx.ALIGN_TOP)
        return vbox


    def textfield(self, value):
        style = wx.TE_READONLY|wx.TE_MULTILINE
        return wx.TextCtrl(self, value=value, style=style)
