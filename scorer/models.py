# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)

class Match(models.Model):
    players = models.ManyToManyField(Player)

class MatchTurn(models.Model):
    match = models.ForeignKey(Match)

    @property
    def player_turns(self):
        return PlayerTurn.models.filter(match_turn=self)

class PlayerTurn(models.Model):
    player = models.ForeignKey(Player)
    match_turn = models.ForeignKey(MatchTurn)

class Score(models.Model):
    player_turn = models.ForeignKey(PlayerTurn)
