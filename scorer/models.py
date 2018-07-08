# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)


class Match(models.Model):
    players = models.ManyToManyField(Player)
    starting_score = models.PositiveIntegerField()


class MatchPlayerOrder(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    sequence = models.PositiveIntegerField()


class MatchTurn(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='match_turns')
    sequence = models.PositiveIntegerField()


class PlayerTurn(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match_turn = models.ForeignKey(MatchTurn, on_delete=models.CASCADE, related_name='player_turns')
    score = models.PositiveIntegerField()
