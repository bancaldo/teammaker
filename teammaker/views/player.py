import wx
import sys
import platform
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin


FR = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | \
    wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN
ACV = wx.ALIGN_CENTER_VERTICAL
ACH = wx.ALIGN_CENTER_HORIZONTAL | wx.ALL
YN = wx.YES_NO | wx.ICON_WARNING
DD = wx.CB_DROPDOWN
HS = wx.LB_HSCROLL


class ViewPlayer(wx.Frame):
    def __init__(self, parent, title, is_editor=False):
        self.parent = parent
        self.is_editor = is_editor
        super(ViewPlayer, self).__init__(parent=self.parent, title=title,
                                         style=FR)
        self.controller = self.parent.controller
        self.panel = PanelPlayer(parent=self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        size = (600, 600) if platform.system() == 'Linux' else (550, 550)
        self.SetSize(size)

        self.panel.btn_delete.Disable()
        if not self.is_editor:
            self.panel.cb_players.Disable()

        self.Bind(wx.EVT_BUTTON, self.parent.quit_subframe, self.panel.btn_quit)
        self.Bind(wx.EVT_BUTTON, self.on_save, self.panel.btn_save)
        self.Bind(wx.EVT_BUTTON, self.delete_player, self.panel.btn_delete)
        self.Bind(wx.EVT_COMBOBOX, self.on_cb_players, self.panel.cb_players)

        self.parent.show_subframe(self)  # Show and center the frame
        # self.panel.cb_teams.Disable()

    # noinspection PyUnusedLocal
    def on_save(self, event):
        if self.is_editor:
            self.update_player(event)
        else:
            self.new_player(event)

    # noinspection PyUnusedLocal
    def on_cb_players(self, event):
        role = self.panel.roles.GetStringSelection()
        string = self.panel.cb_players.GetStringSelection()
        surname = string.split(' ')[0]
        name = string.split(' ')[1]
        player = self.controller.get_player(surname, name)
        self.controller.set_temporary_object(player)
        self.panel.name.SetValue(player.name)
        self.panel.surname.SetValue(str(player.surname))
        self.panel.value.SetValue(str(player.value))
        self.panel.health.SetValue(str(player.health))
        self.panel.roles.SetValue(str(player.role))
        self.panel.btn_delete.Enable()

    # noinspection PyUnusedLocal
    def new_player(self, event):
        name = self.panel.name.GetValue()
        surname = self.panel.surname.GetValue()
        value = int(self.panel.value.GetValue())
        health = int(self.panel.health.GetValue())
        role = self.panel.roles.GetStringSelection()

        self.controller.new_player(surname, name, value, health, role)
        self.parent.show_message('New Player %s %s saved!'
                                 % (surname.upper(), name.lower()))
        self.clear_fields()
        self.parent.refresh_players()

    def clear_fields(self):
        for w in [w for w in self.panel.GetChildren()
                  if isinstance(w, wx.TextCtrl)]:
            w.SetValue('')
        self.panel.roles.ChangeValue('')

    # noinspection PyUnusedLocal
    def update_player(self, event):
        surname = self.panel.surname.GetValue()
        name = self.panel.name.GetValue()
        value = int(self.panel.value.GetValue())
        health = int(self.panel.health.GetValue())
        role = self.panel.roles.GetStringSelection()
        if not role:
            role = self.panel.roles.GetValue()
        if not role:
            self.parent.show_message('Please select role!')
        else:
            self.controller.update_player(surname, name, value, health, role)
            self.parent.show_message('Player %s %s updated!'
                                     % (surname.upper(), name.lower()))
            self.panel.cb_players.Clear()
            players = self.controller.all_players()
            self.panel.cb_players.AppendItems(players)
            self.parent.refresh_players()

    # noinspection PyUnusedLocal
    def delete_player(self, event):
	string = self.panel.cb_players.GetStringSelection()
	surname, name, value, health, role = string.split(' ')
        choice = wx.MessageBox("Deleting Player %s %s..."
		               "are you sure?" % (surname, name),
                               "warning", YN)
        role = self.panel.roles.GetStringSelection()
        if choice == wx.YES:
            self.controller.delete_player(surname, name)
            players = self.controller.all_players()
            self.fill_combobox(self.panel.cb_players, players)
            self.parent.show_message("Player %s %s deleted!" % (surname, name))
            self.parent.refresh_players()
        else:
            choice.Destroy()

    @staticmethod
    def fill_combobox(combobox, players):
        combobox.Clear()
        combobox.AppendItems(['%s %s' % (player.surname, player.name)
                              for player in players])


class PanelPlayer(wx.Panel):
    def __init__(self, parent):
        super(PanelPlayer, self).__init__(parent)
        # Attributes
        roles = ['goalkeeper', 'defender', 'midfielder', 'forward']
        players = parent.controller.all_players()
        self.cb_players = wx.ComboBox(self, -1, "", choices=players, style=DD)
        self.surname = wx.TextCtrl(self)
        self.name = wx.TextCtrl(self)
        self.value = wx.TextCtrl(self)
        self.health = wx.TextCtrl(self)
        self.roles = wx.ComboBox(self, -1, "", style=DD, choices=roles)

        # Layout
        text_sizer = wx.FlexGridSizer(rows=7, cols=2, hgap=5, vgap=5)
        text_sizer.Add(wx.StaticText(self, label="Player:"), 0, ACV)
        text_sizer.Add(self.cb_players, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="Surname:"), 0, ACV)
        text_sizer.Add(self.surname, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="Name:"), 0, ACV)
        text_sizer.Add(self.name, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="Value:"), 0, ACV)
        text_sizer.Add(self.value, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="Health:"), 0, ACV)
        text_sizer.Add(self.health, 0, wx.EXPAND)
        text_sizer.Add(wx.StaticText(self, label="role:"), 0, ACV)
        text_sizer.Add(self.roles, 0, wx.EXPAND)
        text_sizer.AddGrowableCol(1)

        button_sizer = wx.FlexGridSizer(rows=1, cols=3, hgap=5, vgap=5)
        self.btn_save = wx.Button(self, wx.ID_SAVE)
        self.btn_delete = wx.Button(self, wx.ID_DELETE)
        self.btn_quit = wx.Button(self, wx.ID_CANCEL, label="Quit")
        self.btn_quit.SetDefault()
        button_sizer.Add(self.btn_save, 0, ACV)
        button_sizer.Add(self.btn_delete, 0, ACV)
        button_sizer.Add(self.btn_quit, 0, ACV)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text_sizer, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(button_sizer, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(sizer)


class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)


class ViewPlayerSummary(wx.Frame):
    def __init__(self, parent, title):
        self.parent = parent
        super(ViewPlayerSummary, self).__init__(parent=self.parent, title=title)
        self.controller = self.parent.controller
        players = self.controller.all_players()
        self.panel = PanelPlayerSummary(parent=self)
        size = (900, 500) if platform.system() == 'Linux' else (800, 500)
        self.SetSize(size)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_list,
                  self.panel.player_list)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.on_list_column,
                  self.panel.player_list)
        self.Bind(wx.EVT_BUTTON, self.parent.quit_subframe, self.panel.btn_quit)
        self.Bind(wx.EVT_BUTTON, self.on_refresh, self.panel.btn_refresh)
        self.fill_player_list(players)
        self.parent.show_subframe(self)  # Show and center the frame

    # noinspection PyUnusedLocal
    def on_refresh(self, event):
        self.panel.player_list.DeleteAllItems()
        players = self.controller.all_players()
        self.fill_player_list(players)

    # noinspection PyUnusedLocal
    def on_list(self, event):
        item_id = event.GetIndex() if wx.version().startswith('4') else \
            event.m_itemIndex
        surname = self.panel.player_list.GetItemText(item_id)
        name = self.panel.player_list.GetItem(item_id, 1).GetText()
        view_edit = ViewPlayer(self.parent, "Edit Player", is_editor=True)
        player = self.controller.get_player(surname.upper(), name.lower())
        if player:
            view_edit.panel.cb_players.Disable()
            self.controller.set_temporary_object(player)
            view_edit.panel.surname.ChangeValue(player.surname)
            view_edit.panel.name.ChangeValue(player.name)
            view_edit.panel.value.ChangeValue(str(player.value))
            view_edit.panel.health.ChangeValue(str(player.health))
            view_edit.panel.roles.ChangeValue(str(player.role))
            view_edit.panel.btn_delete.Enable()
            view_edit.SetWindowStyle(wx.STAY_ON_TOP)
        else:
            self.parent.show_message('recently modified Object: '
                                     'please click REFRESH')

    def on_list_column(self, event):
        id_column = event.GetColumn()
        players = self.controller.get_sorted_players(id_column)
        self.fill_player_list(players)

    def fill_player_list(self, players):
        self.panel.player_list.DeleteAllItems()
        insert_item = self.panel.player_list.InsertStringItem
        set_item = self.panel.player_list.SetStringItem
        if wx.version().startswith('4'):
            insert_item = self.panel.player_list.InsertItem
            set_item = self.panel.player_list.SetItem

        for string in players:
            surname = string.split(' ')[0]
            name = string.split(' ')[1]
            player = self.controller.get_player(surname, name)
            index = insert_item(sys.maxint, str(player.surname))
            set_item(index, 1, player.name)
            set_item(index, 2, str(player.value))
            set_item(index, 3, str(player.health))
            set_item(index, 4, player.role)


class PanelPlayerSummary(wx.Panel):
    def __init__(self, parent):
        super(PanelPlayerSummary, self).__init__(parent=parent)
        self.player_list = AutoWidthListCtrl(self)
        self.player_list.InsertColumn(0, 'surname', wx.LIST_FORMAT_RIGHT, 100)
        self.player_list.InsertColumn(1, 'name', width=80)
        self.player_list.InsertColumn(2, 'value', width=60)
        self.player_list.InsertColumn(3, 'health', width=60)
        self.player_list.InsertColumn(4, 'role', width=100)

        # BUTTONS sizer
        btn_sizer = wx.FlexGridSizer(rows=1, cols=2, hgap=5, vgap=5)
        self.btn_quit = wx.Button(self, wx.ID_CANCEL, label="Quit")
        self.btn_refresh = wx.Button(self, wx.ID_OK, label="Refresh")
        btn_sizer.Add(self.btn_quit, 0, wx.EXPAND)
        btn_sizer.Add(self.btn_refresh, 0, wx.EXPAND)
        player_list_box = wx.BoxSizer(wx.HORIZONTAL)
        player_list_box.Add(self.player_list, 1, wx.EXPAND)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(player_list_box, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)
