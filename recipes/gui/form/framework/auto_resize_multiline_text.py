import wx
import recipes.gui.form.framework.events as ev

# this works not yet for wrapped text!
class AutoResizeMultilineText(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        kwargs['style'] = kwargs.get('style', 0) | wx.TE_MULTILINE
        self.post_resize = kwargs.get('emit_resize', False)
        super().__init__(*args, **kwargs)

        self.Bind(wx.EVT_KEY_UP, self.on_key_up)
        self.add_height = 10 # avoids scroll effect; TODO: adapt it to font size
        self.min_auto_height = self.get_height()

        self.auto_resize()

    def SetFont(self, *args, **kwargs):
        super().SetFont(*args, **kwargs)
        self.auto_resize()

    def Bind(self, *args, **kwargs):
        if len(args) > 0 and args[0] == ev.EVT_AUTO_RESIZE:
            self.post_resize = True
        super().Bind(*args, **kwargs)

    def on_key_up(self, event):
        if self.auto_resize():
            if self.post_resize: wx.PostEvent(self, ev.AutoResizeEvent())
            else:                self.GetParent().Fit()
        event.Skip()

    def has_to_resize(self):
        height = self.get_height()
        fit_height = self.get_fit_height()
        to_small = fit_height + self.add_height > height
        to_big = fit_height + self.add_height < height
        return to_small or to_big

    def auto_resize(self):
        if self.has_to_resize():
            fit_height = self.get_fit_height()
            new_height = max(self.min_auto_height, fit_height + self.add_height)
            self.set_min_height(new_height)
            return True
        return False

    def set_min_height(self, height):
        self.SetMinSize(wx.Size(self.GetSize()[0], height))

    def get_height(self):
        return self.GetSize()[1]

    def get_fit_height(self):
        border_size = self.GetWindowBorderSize()
        return 2*border_size[1] + self.get_text_height()

    def get_text_extent(self, text = None):
        if not text: text = self.GetValue()
        font = self.GetFont()
        dc = wx.ScreenDC()
        dc.SetFont(font)
        extent = dc.GetTextExtent(text)
        return extent

    def get_text_height(self, text = None):
        return self.get_text_extent(text)[1]
