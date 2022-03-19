import wx
from recipes.gui.form.framework import AutoResizeMultilineText
import recipes.gui.form.framework.events as ev

class MealMasterImportCheck(wx.ScrolledWindow):
    def __init__(self, parent, original_recipes, imported_recipes):
        super().__init__(parent)
        vbox = wx.BoxSizer(wx.VERTICAL)

        for i, original_recipe in enumerate(original_recipes):
            imported_recipe = imported_recipes[i].str(80)
            box = self.create_comparison_box(original_recipe, imported_recipe)
            vbox.Add(box, 0, wx.EXPAND|wx.ALIGN_TOP)
        self.SetSizer(vbox)

        fontsz = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT).GetPixelSize()
        self.SetScrollRate(fontsz.x, fontsz.y)
        self.EnableScrolling(True,True)
        self.update_virtual_size(None)

    def create_comparison_box(self, original_recipe, imported_recipe):
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        flags = wx.EXPAND|wx.ALIGN_TOP|wx.TOP|wx.LEFT
        vbox.Add(self.textfield(original_recipe), 1, flags, border = 10)
        flags = wx.EXPAND|wx.ALIGN_TOP|wx.TOP|wx.RIGHT
        vbox.Add(self.textfield(imported_recipe), 1, flags, border = 10)
        return vbox

    def update_virtual_size(self, event):
        self.SetVirtualSize(self.GetSizer().GetMinSize())

    def textfield(self, value):
        style = wx.TE_MULTILINE|wx.TE_DONTWRAP|wx.TE_READONLY
        textfield = AutoResizeMultilineText(self, value=value, style=style)
        font = wx.Font(wx.FontInfo().Family(wx.FONTFAMILY_MODERN))
        textfield.SetFont(font)
        textfield.Bind(ev.EVT_AUTO_RESIZE, self.update_virtual_size)
        textfield.SetInsertionPoint(0)
        return textfield
