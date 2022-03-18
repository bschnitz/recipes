import wx
import pkgutil
import encodings
from recipes.core.util import Arguments

class ImportMealMasterDialog(wx.Dialog):
    FILETYPE_MEALMASTER = 'MealMaster file (*.mm;*.mmf)|*.mm;*.mmf;*.MM;*.MMF'
    FILETYPE_ANY        = 'Any File (*)|*'
    def __init__(self, parent):
        super().__init__(parent, title='Import MealMaster file')
        self.add_elements()

    def run(self):
        self.ShowModal()
        #path = self.GetPath()
        self.Destroy()
        #return path

    def add_elements(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.create_file_ctrl(), 1, wx.ALIGN_TOP|wx.EXPAND)
        vbox.Add(self.create_encoding_combo(), 0, wx.ALIGN_RIGHT)
        vbox.Add(self.create_buttons(), 0, wx.ALIGN_RIGHT)
        self.SetSizerAndFit(vbox)

    def create_file_ctrl(self):
        fc = wx.FileCtrl(self)
        fc.SetMinSize(wx.Size(900, 600))
        return fc

    def create_encoding_combo(self):
        encodings = list(self.list_encodings())
        encodings.sort()

        vbox = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, label='Encoding:')
        combo = wx.ComboBox(self, choices=encodings)
        vbox.Add(label, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.RIGHT, border=5)
        vbox.Add(combo, 1, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.RIGHT, border=5)

        return vbox

    def create_buttons(self):
        vbox = wx.BoxSizer(wx.HORIZONTAL)

        cancel = wx.Button(self, label='Cancel')
        accept = wx.Button(self, label='Open')

        vbox.Add(cancel, 0,
                 wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.RIGHT|wx.LEFT|wx.TOP,
                 border=5)
        vbox.Add(accept, 1,
                 wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.RIGHT|wx.LEFT|wx.TOP,
                 border=5)

        return vbox

    def add_dropdown_encoding(self):
        encodings = self.list_encodings()

        panel = wx.Panel(self)
        #vbox = wx.BoxSizer(wx.HORIZONTAL)
        #label = wx.StaticText(panel, label='Encoding:')
        #combo = wx.ComboBox(panel, choices=list(encodings))
        #vbox.Add(label, 1, wx.ALIGN_LEFT|wx.EXPAND)
        #vbox.Add(combo, 1, wx.ALIGN_LEFT|wx.EXPAND)
        #panel.SetSizer(vbox)
        panel.SetBackgroundColour(wx.BLUE)

    def list_encodings(self):
        false_positives = set(["aliases"])

        found = set(name for imp, name, ispkg in pkgutil.iter_modules(encodings.__path__) if not ispkg)
        found.difference_update(false_positives)
        found.add('auto')
        return found
