# noinspection PyUnresolvedReferences
from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=40)
    value = models.IntegerField()
    health = models.IntegerField()
    role = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name
