import os
import wx
import pkgutil
import encodings
from recipes.core.util import Arguments
from recipes.gui.form.framework import PaddedBox

class ImportMealMasterDialog(wx.Dialog):
    FILETYPE_MEALMASTER = 'MealMaster file (*.mm;*.mmf)|*.mm;*.mmf;*.MM;*.MMF'
    FILETYPE_ANY        = 'Any File (*)|*'
    ALIGN_ELEMENTS      = wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL
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
        vbox.Add(self.create_path_ctrl(),      0, wx.ALIGN_TOP|wx.EXPAND)
        vbox.Add(self.create_file_ctrl(),      1, wx.ALIGN_TOP|wx.EXPAND)
        vbox.Add(self.create_encoding_combo(), 0, wx.ALIGN_RIGHT)
        vbox.Add(self.create_buttons(),        0, wx.ALIGN_RIGHT)
        self.SetSizerAndFit(vbox)

    def create_path_ctrl(self):
        vbox = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, label='Path:')
        self.path_ctrl = wx.TextCtrl(self)
        vbox.Add(label, 0, self.ALIGN_ELEMENTS|wx.ALL, border=5)
        vbox.Add(self.path_ctrl, 1, self.ALIGN_ELEMENTS|wx.ALL, border=5)

        return vbox
        return PaddedBox(self.path_ctrl, border = 5)

    def create_file_ctrl(self):
        self.fc = wx.FileCtrl(self)
        self.fc.SetMinSize(wx.Size(900, 600))
        self.Bind(wx.EVT_FILECTRL_FILEACTIVATED, self.on_file_activated)
        return self.fc

    def on_file_activated(self, event):
        pass
        #print(event)
        #print(self.fc.GetPath())

    def create_encoding_combo(self):
        encodings = list(self.list_encodings())
        encodings.sort()

        vbox = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, label='Encoding:')
        combo = wx.ComboBox(self, choices=encodings)
        vbox.Add(label, 0, self.ALIGN_ELEMENTS|wx.BOTTOM|wx.RIGHT, border=5)
        vbox.Add(combo, 1, self.ALIGN_ELEMENTS|wx.BOTTOM|wx.RIGHT, border=5)

        return vbox

    def create_buttons(self):
        vbox = wx.BoxSizer(wx.HORIZONTAL)

        cancel = wx.Button(self, label='Cancel')
        accept = wx.Button(self, label='Open')

        vbox.Add(cancel, 0, self.ALIGN_ELEMENTS|wx.ALL, border=5)
        vbox.Add(accept, 1, self.ALIGN_ELEMENTS|wx.ALL, border=5)

        return vbox

    def list_encodings(self):
        false_positives = set(["aliases"])

        found = set(name for imp, name, ispkg in pkgutil.iter_modules(encodings.__path__) if not ispkg)
        found.difference_update(false_positives)
        found.add('auto')
        return found
