import wx
import enum
import wx.lib.newevent

AutoResizeEvent, EVT_AUTO_RESIZE = wx.lib.newevent.NewEvent()
CancelImportEvent, EVT_CANCEL_IMPORT = wx.lib.newevent.NewEvent()

class EventIds(enum.IntEnum):
    IMPORT_MEAL_MASTER = wx.NewIdRef().GetId()
