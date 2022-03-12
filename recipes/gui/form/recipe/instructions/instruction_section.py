import wx

from recipes.gui.fonts import Head2
from recipes.gui.form.framework import TitleBox
from recipes.gui.form.framework import PaddedBox
from recipes.gui.form.framework import AutoResizeMultilineText
from wx.lib.expando import ExpandoTextCtrl, EVT_ETC_LAYOUT_NEEDED

class InstructionSection:
    def __init__(self, parent):
        self.parent = parent
        title = 'Instructions for first meal'
        titled_box = TitleBox(self.form(parent), parent, title, Head2())
        parent.SetSizer(PaddedBox(titled_box))

    def form(self, parent):
        sizer = wx.GridBagSizer(10, 10)

        label = wx.StaticText(parent, label='Section Title')
        input = wx.TextCtrl(parent)
        sizer.Add(label, pos=(0,0), flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(input, pos=(0,1), flag=wx.EXPAND)

        instructions_input = AutoResizeMultilineText(parent)
        sizer.Add(instructions_input, pos=(1,0), span=(1, 2), flag=wx.EXPAND)

        sizer.AddGrowableCol(1)

        return sizer
