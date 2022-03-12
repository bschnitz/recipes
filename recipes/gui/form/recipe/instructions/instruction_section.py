import wx

from recipes.gui.fonts import Head2
from recipes.gui.form.framework import TitleBox
from recipes.gui.form.framework import PaddedBox
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

        instructions_input = ExpandoTextCtrl(parent)
        parent.Bind(EVT_ETC_LAYOUT_NEEDED, self.OnRefit, instructions_input)
        sizer.Add(instructions_input, pos=(1,0), span=(1, 2), flag=wx.EXPAND)

        sizer.AddGrowableCol(1)

        self.sizer = sizer
        self.instructions_i = instructions_input

        return sizer

    def OnRefit(self, evt):
        # The Expando control will redo the layout of the
        # sizer it belongs to, but sometimes this may not be
        # enough, so it will send us this event so we can do any
        # other layout adjustments needed.  In this case we'll
        # just resize the frame to fit the new needs of the sizer.
        print(self.instructions_i.GetSize())
        self.sizer.Fit(self.instructions_i)
        print(self.instructions_i.GetSize())
