import wx

class AutoResizeTextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_auto_width = self.get_width()
        self.Bind(wx.EVT_KEY_UP, self.on_key_up)
        self.add_width = 10

    def on_key_up(self, event):
        if self.auto_resize():
            self.GetParent().Layout()
        event.Skip()

    def has_to_resize(self):
        width = self.get_width()
        fit_width = self.get_fit_width()
        to_small = fit_width + self.add_width > width
        to_big = fit_width + self.add_width < width
        return to_small or to_big

    def auto_resize(self):
        width = self.get_width()
        fit_width = self.get_fit_width()
        to_small = fit_width + self.add_width > width
        to_big = fit_width + self.add_width < width
        if to_small or to_big:
            new_width = max(self.min_auto_width, fit_width + self.add_width)
            self.set_min_width(new_width)
            return True
        return False

    def set_min_width(self, width):
        self.SetMinSize(wx.Size(width, self.GetSize()[1]))

    def get_width(self):
        return self.GetSize()[0]

    def get_fit_width(self):
        border_size = self.GetWindowBorderSize()
        return 2*border_size[0] + self.get_text_width()

    def get_text_extent(self, text = None):
        if not text: text = self.GetValue()
        font = self.GetFont()
        dc = wx.ScreenDC()
        dc.SetFont(font)
        return dc.GetTextExtent(text)

    def get_text_width(self, text = None):
        return self.get_text_extent(text)[0]
