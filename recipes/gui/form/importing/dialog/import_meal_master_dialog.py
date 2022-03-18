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

    def get_path(self):
        return self.path_ctrl.GetValue()

    def get_encoding(self):
        return self.encoding_combo.GetValue()

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
        self.path_ctrl.Bind(wx.EVT_KEY_UP, self.path_ctrl_select)
        vbox.Add(label, 0, self.ALIGN_ELEMENTS|wx.ALL, border=5)
        vbox.Add(self.path_ctrl, 1, self.ALIGN_ELEMENTS|wx.ALL, border=5)

        return vbox

    def path_ctrl_select(self, event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            selection = os.path.expanduser(self.path_ctrl.GetValue())
            self.path_ctrl.SetValue(selection)
            if os.path.isdir(selection):
                self.fc.SetDirectory(selection)
            else:
                self.on_accept(event)

    def selected_path_is_valid(self):
        if os.path.isdir(self.path_ctrl.GetValue()): return False

        return os.path.isfile(self.path_ctrl.GetValue())

    def create_file_ctrl(self):
        self.fc = wx.FileCtrl(self)
        self.fc.SetMinSize(wx.Size(900, 600))
        self.Bind(wx.EVT_FILECTRL_FILEACTIVATED, self.on_file_activated)
        self.Bind(wx.EVT_FILECTRL_SELECTIONCHANGED, self.on_selection_changed)
        return self.fc

    def on_selection_changed(self, event):
        path = self.fc.GetPath()

        if not path: path = self.fc.GetDirectory()

        self.path_ctrl.SetValue(path)

    def on_file_activated(self, event):
        self.path_ctrl.SetValue(self.fc.GetPath())
        self.on_accept(event)

    def on_accept(self, event):
        if self.selected_path_is_valid():
            self.Destroy()

    def on_cancel(self, event):
        self.path_ctrl.SetValue('')
        self.Destroy()

    def create_encoding_combo(self):
        encodings = list(self.list_encodings())
        encodings.sort()

        vbox = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, label='Encoding:')
        self.encoding_combo = wx.ComboBox(self, value='auto', choices=encodings)
        borders = wx.BOTTOM|wx.RIGHT
        vbox.Add(label, 0, self.ALIGN_ELEMENTS|borders, border=5)
        vbox.Add(self.encoding_combo, 1, self.ALIGN_ELEMENTS|borders, border=5)

        return vbox

    def create_buttons(self):
        vbox = wx.BoxSizer(wx.HORIZONTAL)

        cancel = wx.Button(self, label='Cancel')
        accept = wx.Button(self, label='Open')

        cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        accept.Bind(wx.EVT_BUTTON, self.on_accept)

        vbox.Add(cancel, 0, self.ALIGN_ELEMENTS|wx.ALL, border=5)
        vbox.Add(accept, 1, self.ALIGN_ELEMENTS|wx.ALL, border=5)

        return vbox

    def list_encodings(self):
        false_positives = set(["aliases"])

        found = set(name for imp, name, ispkg in pkgutil.iter_modules(encodings.__path__) if not ispkg)
        found.difference_update(false_positives)
        found.add('auto')
        return found
