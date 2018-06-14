# noinspection PyUnresolvedReferences
from models import Player


class Model(object):
    def __init__(self):
        super(Model, self).__init__()
        self.temporary_object = None
        self._diff = 25
        self._player = None

    def set_temporary_object(self, obj):
        print "[DEBUG] %s in-memory object setting..." % type(obj)
        self.temporary_object = obj

    def get_temporary_object(self):
        print "[DEBUG] %s in-memory object retrieving..." % \
              type(self.temporary_object)
        return self.temporary_object

    @property
    def diff(self):
        return self._diff

    @diff.setter
    def diff(self, value):
        self._diff = value

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, obj):
        self._player = obj

    @staticmethod
    def new_player(surname, name, value, health, role):
        player = Player.objects.filter(name=name.lower(),
                                       surname=surname.upper()).first()
        if not player:
            Player.objects.create(name=name.lower(), surname=surname.upper(),
                                  value=int(value), health=int(health),
                                  role=role.lower())
            msg = 'INFO: Player <%s %s> CREATED!' % (name.lower(),
                                                     surname.upper())
        else:
            msg = 'WARNING: Player <%s %s> already exists' % (name.lower(),
                                                              surname.upper())
        return msg

    @staticmethod
    def get_player(surname, name):
        return Player.objects.filter(name=name.lower(), 
                                     surname=surname.upper()).first()

    @staticmethod
    def all_players():
        goalkeepers = [g for g in
                       Player.objects.filter(role='goalkeeper').all()]
        defenders = [g for g in Player.objects.filter(role='defender').all()]
        midfielders = [g for g in
                       Player.objects.filter(role='midfielder').all()]
        forwards = [g for g in Player.objects.filter(role='forward').all()]
        return goalkeepers + defenders + midfielders + forwards

    def update_player(self, *args):
        name, surname, value, health, role = args
        player = self.get_player(surname, name)
        if not player:
            player = self.get_temporary_object()
        player.name = name.strip().lower()
        player.surname = surname.strip().upper()
        player.value = int(value)
        player.health = int(health)
        player.role = role.lower()
        player.save()
        return 'INFO: Player <%s %s> UPDATED!' % (player.name, player.surname)

    def delete_player(self, surname, name):
        player = self.get_player(surname, name)
        player.delete()
        return 'INFO: Player <%s %s> DELETED!' % (surname, name)

    @staticmethod
    def get_players_ordered_by_filter(filter_name):
        return Player.objects.order_by(filter_name).all()
