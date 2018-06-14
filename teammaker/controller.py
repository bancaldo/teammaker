# noinspection PyUnresolvedReferences
from models import Player
# noinspection PyUnresolvedReferences
from django.contrib import messages
# noinspection PyUnresolvedReferences
from django.utils import timezone
from teammaker.views.core import Core
from model import Model
from random import shuffle


class Controller(object):
    def __init__(self):
        self.model = Model()
        super(Controller, self).__init__()
        self.view = Core(parent=None, controller=self, 
                         title='teammaker v.2.2 by Bancaldo')

    def set_temporary_object(self, obj):
        self.model.set_temporary_object(obj)

    def get_temporary_object(self):
        return self.model.get_temporary_object()

    # PLAYER methods -----------------------------------------------------------
    def get_player(self, surname, name):
        return self.model.get_player(surname, name)

    def update_player(self, name, surname, value, health, role):
        msg = self.model.update_player(name, surname, value, health, role)
        self.view.show_message(msg)

    def new_player(self, surname, name, value, health, role):
        result = self.model.new_player(surname, name, value, health, role)
        self.view.show_message(result)
 
    def all_players(self):
        return ['%s %s %s %s <%s>' % (player.surname, player.name.capitalize(),
                                      player.value, player.health, 
                                      player.role)
                for player in self.model.all_players()]
 
    def delete_player(self, surname, name):
        msg = self.model.delete_player(surname, name)
        self.view.show_message(msg)

    def get_gap(self):
        return self.model.diff
 
    def set_gap(self, value):
        try:
            self.model.diff = int(value)
            return '[INFO] new GAP set!'
        except ValueError:
            return "[ERROR] GAP value must be a number!"
 
    def create_teams(self, iterable):
        # Algorithm
        # 1) Check if player are selected
        # 2) check if players are odd and then a fake player is added
        # 3) create a player list sorted by role and mix it to shuffle players
        # 4) create 2 lists sorted by role with zig-zag method: [::2][1::2]
        selected_players = list(iterable)
        sorted_players = self.filter_by_role(selected_players)
        green, yellow = sorted_players[::2], sorted_players[1::2]
        diff = self.check_gap(green, yellow)
        attempts = 1
        while diff >= self.model.diff:
            print '[INFO] GAP <%s> too high!' % diff
            print '[INFO] Teams are not balanced: recalculating...'
            print '[INFO] Attempt n. %s...' % attempts
            sorted_players = self.filter_by_role(selected_players)
            green, yellow = sorted_players[::2], sorted_players[1::2]
            attempts += 1
            if attempts > 5000:
                green, yellow = [], []
                break
            else:
                diff = self.check_gap(green, yellow)
        if not green and not yellow:
            self.view.show_message("Need higher GAP to "
                                   "calculate balanced teams: choose a GAP > %s"
                                   % diff)
        else:
            print '[INFO] Teams GAP <%s>' % diff
            print '[INFO] Teams done!'
        return green, yellow
 
    @staticmethod
    def filter_by_role(iterable):
        gks = [gk for gk in iterable if gk.split(' ')[4] == '<goalkeeper>']
        defs = [df for df in iterable if df.split(' ')[4] == '<defender>']
        mids = [mid for mid in iterable if mid.split(' ')[4] == '<midfielder>']
        fws = [fw for fw in iterable if fw.split(' ')[4] == '<forward>']
        for role_list in (gks, defs, mids, fws):
            shuffle(role_list)
        return gks + defs + mids + fws
 
    @staticmethod
    def check_gap(green, yellow):
        val_green = sum([int(player.split(' ')[2]) for player in green])
        hdf_green = sum([int(player.split(' ')[3]) for player in green])/2
        val_yellow = sum([int(player.split(' ')[2]) for player in yellow])
        hdf_yellow = sum([int(player.split(' ')[3]) for player in yellow])/2
        return abs((val_green + hdf_green) - (val_yellow + hdf_yellow))

    def get_sorted_players(self, id_c):
        columns = {0: 'surname', 1: 'name', 2: '-value',
                   3: '-health', 4: 'role'}
        players = self.model.get_players_ordered_by_filter(columns.get(id_c))
        return ['%s %s' % (player.surname, player.name) for player in players]
