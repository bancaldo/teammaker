import wx
import platform


FR = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | \
    wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN
ACV = wx.ALIGN_CENTER_VERTICAL
OK = wx.OK | wx.ICON_EXCLAMATION


class ViewGap(wx.Frame):
    def __init__(self, parent, title):
        self.parent = parent
        super(ViewGap, self).__init__(parent=self.parent, title=title, style=FR)
        self.controller = self.parent.controller
        self.panel = PanelGap(parent=self)
        size = (200, 100) if platform.system() == 'Linux' else (250, 125)
        self.SetSize(size)

        self.Bind(wx.EVT_BUTTON, self.on_change, self.panel.btn_change)
        self.Bind(wx.EVT_BUTTON, self.parent.quit_subframe, self.panel.btn_quit)

        self.parent.show_subframe(self)  # Show and center the frame

    # noinspection PyUnusedLocal
    def on_change(self, event):
        gap = self.panel.gap.GetValue()
        msg = self.controller.set_gap(gap)
        self.parent.refresh_gap()
        wx.MessageBox(msg, 'core info', OK)


class PanelGap(wx.Panel):
    def __init__(self, parent):
        super(PanelGap, self).__init__(parent)
        # Attributes
        gap = parent.controller.get_gap()
        self.gap = wx.TextCtrl(self, value=str(gap))
        # Layout
        self.btn_change = wx.Button(self, wx.ID_SAVE, label="Change")
        self.btn_quit = wx.Button(self, wx.ID_CANCEL, label="Quit")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="Actual GAP:"), 0, ACV)
        sizer.Add(self.gap, 0, wx.EXPAND)
        sizer.Add(self.btn_change, 0, wx.EXPAND)
        sizer.Add(self.btn_quit, 0, wx.EXPAND)
        self.SetSizer(sizer)
