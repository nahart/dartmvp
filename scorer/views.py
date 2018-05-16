# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from .models import Player, Match

# Create your views here.
# def index(request):
#     return render(request, 'scorer/home.html')

class DartView(View):
    # template_name = 'home.html'

    def get(self, request):
        Player.objects.filter(name='Noah').values("name") #ORM Call
        # MatchTurn.objects.filter(match__player__name__in=[])
        template_vars = {
            'double': 'x2'
        }
        return render(request, 'scorer/home.html', template_vars)

    def post(self, request):
        print request.POST.keys()
        return redirect('scorer')


class SettingsView(View):

    def get(self, request):
        return render(request, 'scorer/start_game.html')

    def post(self, request):
        player_1_first_name = request.POST.get("player_1_first_name")
        player_2_first_name = request.POST.get("player_2_first_name")
        player_1_last_name = request.POST.get("player_1_last_name")
        player_2_last_name = request.POST.get("player_2_last_name")

        players = (
            Player.objects.create(
                name="{} {}".format(player_1_first_name, player_1_last_name),
                email=''
            ),
            Player.objects.create(
                name="{} {}".format(player_2_first_name, player_2_last_name),
                email='',
            )
        )

        match = Match.objects.create()
        for player in players:
            match.players.add(player)
        match.save()
        return redirect('game')

class GameView(View):

    def get(self, request):
        return render(request, 'scorer/game.html')

    def post(self, request):
        pass

class LandingPageView(View):

    def get(self, request):
        return render(request, 'scorer/landingpage.html')