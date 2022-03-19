import wx
from recipes.gui.fonts.head_1 import Head1
from recipes.gui.form.framework import AutoResizeMultilineText
import recipes.gui.form.framework.events as ev

class MealMasterImportCheck(wx.Panel):
    def __init__(self, parent, original_recipes, imported_recipes):
        super().__init__(parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        buttons = self.create_buttons()
        header = self.create_header()
        panes = self.create_scrolled_panes(original_recipes, imported_recipes)
        vbox.Add(5, 5, 0)
        vbox.Add(buttons, 0, wx.ALIGN_CENTER_HORIZONTAL)
        vbox.Add(header, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL)
        vbox.Add(panes, 1, wx.EXPAND|wx.ALIGN_TOP)
        self.SetSizer(vbox)

    def create_header(self):
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        label_left = self.header_label('Original Recipes')
        label_right = self.header_label('Imported Recipes')
        vbox.Add(label_left, 1, wx.EXPAND|wx.ALL, border=5)
        vbox.Add(label_right, 1, wx.EXPAND|wx.ALL, border=5)
        return vbox

    def header_label(self, label):
        label = wx.StaticText(self, label=label, style=wx.ALIGN_CENTRE)
        label.SetFont(Head1())
        label.SetMinSize(label.GetTextExtent(label.GetLabel()))
        return label

    def create_buttons(self):
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        accept = wx.Button(self, label='Accept and Save')
        cancel = wx.Button(self, label='Cancel and Discard')
        vbox.Add(accept, 1, wx.ALIGN_CENTER|wx.ALL, border=5)
        vbox.Add(cancel, 1, wx.ALIGN_CENTER|wx.ALL, border=5)
        return vbox


    def create_scrolled_panes(self, original_recipes, imported_recipes):
        self.sw = wx.ScrolledWindow(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        for i, original_recipe in enumerate(original_recipes):
            imported_recipe = imported_recipes[i].str(80)
            box = self.create_comparison_box(original_recipe, imported_recipe)
            vbox.Add(box, 0, wx.EXPAND|wx.ALIGN_TOP)
        self.sw.SetSizer(vbox)

        fontsz = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT).GetPixelSize()
        self.sw.SetScrollRate(fontsz.x, fontsz.y)
        self.sw.EnableScrolling(True,True)
        self.update_virtual_size(None)

        return self.sw

    def create_comparison_box(self, original_recipe, imported_recipe):
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        flags = wx.EXPAND|wx.ALIGN_TOP|wx.BOTTOM|wx.LEFT
        vbox.Add(self.textfield(original_recipe), 1, flags, border = 10)
        flags = wx.EXPAND|wx.ALIGN_TOP|wx.BOTTOM|wx.RIGHT
        vbox.Add(self.textfield(imported_recipe), 1, flags, border = 10)
        return vbox

    def update_virtual_size(self, event):
        self.sw.SetVirtualSize(self.sw.GetSizer().GetMinSize())

    def textfield(self, value):
        style = wx.TE_MULTILINE|wx.TE_DONTWRAP|wx.TE_READONLY
        textfield = AutoResizeMultilineText(self.sw, value=value, style=style)
        font = wx.Font(wx.FontInfo().Family(wx.FONTFAMILY_MODERN))
        textfield.SetFont(font)
        textfield.Bind(ev.EVT_AUTO_RESIZE, self.update_virtual_size)
        textfield.SetInsertionPoint(0)
        return textfield
