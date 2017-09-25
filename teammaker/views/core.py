import wx
from player import ViewPlayer, ViewPlayerSummary
from gap import ViewGap
from info import HelpFrame, AboutFrame
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
import sys
import platform


class Core(wx.Frame):
    def __init__(self, parent, controller, title):
        super(Core, self).__init__(parent=parent, title=title)
        self.controller = controller
        self.panel = Panel(self)
        self.menu_bar = wx.MenuBar()
        self.SetMenuBar(self.menu_bar)
        # Menu definition ------------------------------------------------------
        # PLAYER Menu ----------------------------------------------------------
        player_menu = wx.Menu()
        self.menu_bar.Append(player_menu, "Players")
        self.new_player_menu = player_menu.Append(-1, "New Player")
        self.edit_player_menu = player_menu.Append(-1, "Edit Player")
        player_menu.AppendSeparator()
        self.player_summary_menu = player_menu.Append(-1, "Player Summary")
        player_menu.AppendSeparator()
        self.exit_menu = player_menu.Append(-1, "Exit")
        # GAP Menu ----------------------------------------------------------
        gap_menu = wx.Menu()
        self.menu_bar.Append(gap_menu, "Gap")
        self.change_gap_menu = gap_menu.Append(-1, "change...")
        # INFO Menu ----------------------------------------------------------
        info_menu = wx.Menu()
        self.menu_bar.Append(info_menu, "Info")
        self.about_menu = info_menu.Append(-1, "About...")
        self.help_menu = info_menu.Append(-1, "Help")
        # Menu bindings --------------------------------------------------------
        self.Bind(wx.EVT_MENU, self.quit, self.exit_menu)
        self.Bind(wx.EVT_BUTTON, self.quit, self.panel.btn_quit)
        self.Bind(wx.EVT_MENU, self.new_player, self.new_player_menu)
        self.Bind(wx.EVT_MENU, self.edit_player, self.edit_player_menu)
        self.Bind(wx.EVT_MENU, self.player_summary, self.player_summary_menu)
        self.Bind(wx.EVT_MENU, self.change_gap, self.change_gap_menu)
        self.Bind(wx.EVT_MENU, self.about, self.about_menu)
        self.Bind(wx.EVT_MENU, self.help, self.help_menu)
        self.Bind(wx.EVT_BUTTON, self.generate, self.panel.btn_generate)

        size = (800, 375) if platform.system() == 'Linux' else (1000, 400)
        self.SetSize(size)
        self.Centre()
        self.Show()

    # noinspection PyUnusedLocal
    def quit(self, event):
        self.Destroy()

    # noinspection PyUnusedLocal
    def edit_player(self, event):
        self.Disable()
        ViewPlayer(parent=self, title='Edit Player', is_editor=True)

    # noinspection PyUnusedLocal
    def new_player(self, event):
        self.Disable()
        ViewPlayer(parent=self, title='New Player')

    # noinspection PyUnusedLocal
    def player_summary(self, event):
        self.Disable()
        ViewPlayerSummary(parent=self, title='Players Summary')

    # noinspection PyUnusedLocal
    def change_gap(self, event):
        self.Disable()
        ViewGap(parent=self, title='Change Team GAP')

    # noinspection PyUnusedLocal
    def about(self, event):
        self.Disable()
        AboutFrame(parent=self, title='about teammaker')

    # noinspection PyUnusedLocal
    def help(self, event):
        self.Disable()
        HelpFrame(parent=self, title='Help teammaker')

    def quit_subframe(self, event):
        subframe = event.GetEventObject().GetParent()
        if isinstance(subframe, wx.Panel):
            subframe = subframe.GetParent()
        self.Enable()
        subframe.Destroy()

    @staticmethod
    def show_subframe(child):
        child.Centre()
        child.Show()

    # noinspection PyUnusedLocal
    def generate(self, event):
        self.panel.green_player_list.DeleteAllItems()
        self.panel.yellow_player_list.DeleteAllItems()
        selected_players = self.panel.available_players.GetCheckedStrings()

        if len(selected_players) == 0:
            self.show_message('Please select players!')
        else:
            if len(selected_players) % 2 == 1:
                self.show_message('Odd players: adding a FAKE one!')
                selected_players += ('NULL player 0 0 <>', )
            green, yellow = self.controller.create_teams(selected_players)
            if green and yellow:
                self.update_teams(green, yellow)

    def update_teams(self, green, yellow):
        self.show_message('Team created!')
        for iterable, widget in [(green, self.panel.green_player_list),
                                 (yellow, self.panel.yellow_player_list)]:
            self.fill_player_list(iterable, widget)

    def fill_player_list(self, players, widget):
        widget.DeleteAllItems()
        insert_item = widget.InsertStringItem
        set_item = widget.SetStringItem
        if wx.version().startswith('4'):
            insert_item = widget.InsertItem
            set_item = widget.SetItem

        for player_string in players:
            surname, name, value, health, role = player_string.split(' ')
            player = self.controller.get_player(surname.upper(), name.lower())
            index = insert_item(sys.maxint, str(player.surname))
            set_item(index, 1, player.name)
            set_item(index, 2, str(player.value))
            set_item(index, 3, str(player.health))
            set_item(index, 4, player.role)

    def refresh_gap(self):
        self.panel.gap.SetLabel("Gap: %s" % self.controller.get_gap())

    def refresh_players(self):
        self.panel.available_players.Clear()
        players = self.controller.all_players()
        self.panel.available_players.AppendItems(players)

    @staticmethod
    def show_message(message):
        wx.MessageBox(message, 'core info', wx.OK | wx.ICON_EXCLAMATION)


class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)


class Panel(wx.Panel):
    def __init__(self, parent):
        super(Panel, self).__init__(parent=parent)
        self.gap = wx.StaticText(self,
                                 label="Gap: %s" % parent.controller.get_gap())
        players = parent.controller.all_players()
        self.available_players = wx.CheckListBox(self, choices=players,
                                                 size=(250, 200))

        self.green_player_list = AutoWidthListCtrl(self)
        self.green_player_list.InsertColumn(0, 'surname',
                                            wx.LIST_FORMAT_RIGHT, 80)
        self.green_player_list.InsertColumn(1, 'name', width=60)
        self.green_player_list.InsertColumn(2, 'value', width=50)
        self.green_player_list.InsertColumn(3, 'health', width=50)
        self.green_player_list.InsertColumn(4, 'role', width=70)

        self.yellow_player_list = AutoWidthListCtrl(self)
        self.yellow_player_list.InsertColumn(0, 'surname',
                                             wx.LIST_FORMAT_RIGHT, 80)
        self.yellow_player_list.InsertColumn(1, 'name', width=60)
        self.yellow_player_list.InsertColumn(2, 'value', width=50)
        self.yellow_player_list.InsertColumn(3, 'health', width=50)
        self.yellow_player_list.InsertColumn(4, 'role', width=70)

        self.btn_quit = wx.Button(self, label='Quit')
        self.btn_generate = wx.Button(self, label='Generate')

        list_sizer = wx.FlexGridSizer(rows=3, cols=3, hgap=5, vgap=5)

        list_sizer.Add(wx.StaticText(self, label="available players"),
                       1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        list_sizer.Add(wx.StaticText(self, label="green team"),
                       1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        list_sizer.Add(wx.StaticText(self, label="yellow team"),
                       1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        list_sizer.Add(self.available_players, 1,
                       wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        list_sizer.Add(self.green_player_list, 1,
                       wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        list_sizer.Add(self.yellow_player_list, 1,
                       wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        list_sizer.Add(self.gap, 1, wx.ALIGN_LEFT | wx.ALL, 5)

        btn_sizer = wx.FlexGridSizer(rows=1, cols=2, hgap=5, vgap=5)
        btn_sizer.Add(self.btn_quit, 0, wx.EXPAND | wx.ALL)
        btn_sizer.Add(self.btn_generate, 0, wx.EXPAND | wx.ALL)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(list_sizer, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        self.SetSizer(sizer)
