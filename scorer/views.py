# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import View

from .helpers import PlayerStatus
from .models import Player, Match, MatchTurn, PlayerTurn, MatchPlayerOrder


class DartView(View):
    # template_name = 'home.html'

    def get(self, request):
        Player.objects.filter(name='Noah').values("name")  # ORM Call
        # MatchTurn.objects.filter(match__player__name__in=[])
        template_vars = {
            'double': 'x2'
        }
        return render(request, 'scorer/home.html', template_vars)

    def post(self, request):
        print(request.POST.keys())
        return redirect('scorer')


class SettingsView(View):

    def get(self, request):
        return render(request, 'scorer/start_game.html')

    def post(self, request):

        # Create Players
        player_numbers = set()
        for player_key in request.POST.keys():
            if player_key.startswith('player_'):
                player_number = player_key.split('_')[1]
                player_numbers.add(player_number)

        players = []
        for player_number in sorted(player_numbers):
            player_first_name = request.POST.get("player_{}_first_name".format(player_number))
            player_last_name = request.POST.get("player_{}_last_name".format(player_number))
            player = Player.objects.create(
                name="{} {}".format(player_first_name, player_last_name),
                email=''
            )
            players.append(player)

        # Create a Match
        match = Match.objects.create(
            starting_score=301
        )

        # Add players to match and create the MatchPlayerOrder objects
        for player_index, player in enumerate(players):
            match.players.add(player)

            MatchPlayerOrder.objects.create(
                match=match,
                player=player,
                sequence=player_index+1  # the player with sequence 1 goes first
            )

        # Save the match (its players were just added!)
        match.save()

        # Create a match turn
        match_turn = MatchTurn.objects.create(
            match=match,
            sequence=0
        )

        # Create player turn for every player
        for player in players:
            PlayerTurn.objects.create(
                player=player,
                match_turn=match_turn,
                score=-1,  # initialize their score to -1 (-1 means the turn has NOT been taken!)
            )

        # Remove Later - Info for Debugging
        print(request.POST.keys())
        print(request.POST.values())

        # Redirect to Game with data
        return redirect('game')


class GameView(View):

    def _get_player_statuses(self, match_turns):
        """
        :param match_turns:
        :return: list of PlayerStatus instances in Player sequence order
        """
        # get the last match turn
        last_match_turn = list(match_turns)[-1]

        # get all the player turns that belong to this match turn
        player_turns = last_match_turn.playerturn_set.all()

        # add a 'sequence' attribute to each player_turn in player_turns
        for player_turn in player_turns:
            player_turn.sequence = self.player_id_to_sequence[player_turn.player.id]

        # sort the player_turns by the newly added 'sequence' attribute
        last_player_turns_sequence_ordered = sorted(player_turns, key=lambda player_turn: player_turn.sequence)
        # last_player_turns_sequence_ordered is now an ordered list of player turns

        players_statuses = []
        player_turn_determined = False
        for player_turn in last_player_turns_sequence_ordered:
            player_status = PlayerStatus(match=self.match, player_turn=player_turn)

            # determine whether or not if it is this player's turn
            if (not player_turn_determined) and (player_turn.score == -1):
                player_status.my_turn = True
                player_turn_determined = True

            players_statuses.append(player_status)

        return players_statuses

    def get(self, request, match_id):
        try:
            self.match = Match.objects.get(id=match_id)
        except Match.DoesNotExist:
            redirect('scorer')

        # create an index player_id -> sequence
        self.player_id_to_sequence = dict(
            MatchPlayerOrder.objects.filter(match=self.match).values_list('player_id', 'sequence')
        )

        # get all the match turns for this match
        match_turns = self.match.matchturn_set.all().order_by('sequence')

        # count the number of match turns (determines what match turn we are on)
        match_turn_number = match_turns.count()

        # get the player statuses (list of instances of PlayerStatus in Player sequence order)
        players_statuses = self._get_player_statuses(match_turns)

        template_vars = {
            'match_turn_number': match_turn_number,
            'players_statuses': players_statuses,
        }

        return render(request, 'scorer/game.html', template_vars)

    def post(self, request):
        pass

class LandingPageView(View):

    def get(self, request):
        return render(request, 'scorer/landingpage.html')