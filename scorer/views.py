# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse
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

        # Redirect to Game with data
        # Set a session variable with match_id
        request.session['match_id'] = match.id
        return redirect('game_no_match_id')


class GameView(View):

    def _get_player_statuses(self, match_turns):
        """
        :param match_turns:
        :return: list of PlayerStatus instances in Player sequence order
        """
        # get the last match turn
        last_match_turn = list(match_turns)[-1]

        # get all the player turns that belong to this match turn
        player_turns = last_match_turn.player_turns.all()

        # add a 'sequence' attribute to each player_turn in player_turns
        for player_turn in player_turns:
            player_turn.sequence = self.player_id_to_sequence[player_turn.player.id]

        # sort the player_turns by the newly added 'sequence' attribute
        last_player_turns_sequence_ordered = sorted(player_turns, key=lambda player_turn: player_turn.sequence)
        # last_player_turns_sequence_ordered is now an ordered list of player turns

        players_statuses = []
        player_turn_determined = False
        for player_turn in last_player_turns_sequence_ordered:

            # determine whether or not if it is this player's turn
            if (not player_turn_determined) and (player_turn.score == -1):
                player_status = PlayerStatus(match=self.match,
                                             player_turn=player_turn,
                                             my_turn=True,
                                             match_turn_id=last_match_turn.id)
                player_turn_determined = True
            else:
                player_status = PlayerStatus(match=self.match,
                                             player_turn=player_turn,
                                             match_turn_id=last_match_turn.id)

            players_statuses.append(player_status)

        return players_statuses

    def get(self, request, match_id=None):
        #Get match_id from session variables if not provided
        if not match_id:
            match_id = request.session.get('match_id')

        try:
            self.match = Match.objects.get(id=match_id)
        except Match.DoesNotExist:
            redirect('scorer')

        # create an index player_id -> sequence
        self.player_id_to_sequence = dict(
            MatchPlayerOrder.objects.filter(match=self.match).values_list('player_id', 'sequence')
        )

        # get all the match turns for this match
        match_turns = self.match.match_turns.all().order_by('sequence')

        # count the number of match turns (determines what match turn we are on)
        match_turn_number = match_turns.count()

        # get the player statuses (list of instances of PlayerStatus in Player sequence order)
        players_statuses = self._get_player_statuses(match_turns)

        template_vars = {
            'match_turn_number': match_turn_number,
            'players_statuses': players_statuses,
            'post_url': reverse('game', kwargs={'match_id': match_id})
        }

        return render(request, 'scorer/game.html', template_vars)

    def post(self, request, match_id):
        # Parse out info in POST Keys request.POST.keys()
        player_key = [key for key in request.POST.keys() if key.startswith('player_')][0]
        player_id = int(player_key.split('_')[1])
        player_score = int(request.POST[player_key])
        match_turn_id = request.POST['match_turn_id']

        # update the specific player turn's score
        self.match = MatchTurn.objects.get(id=match_turn_id).match
        player_turns = PlayerTurn.objects.filter(match_turn_id=match_turn_id)
        player_turn = player_turns.get(player_id=player_id)

        # get all the match turns for this match
        match_turns = self.match.match_turns.all().order_by('sequence')

        # create an index player_id -> sequence
        self.player_id_to_sequence = dict(
            MatchPlayerOrder.objects.filter(match=self.match).values_list('player_id', 'sequence')
        )

        players_statuses = self._get_player_statuses(match_turns)
        current_turn_player_status_list = [player_status for player_status in players_statuses if player_status.id == player_id]
        if current_turn_player_status_list:
            current_turn_player_status = current_turn_player_status_list[0]
        else:
            current_turn_player_status = None

        if current_turn_player_status and ((current_turn_player_status.overall_score - player_score) < 0):
            player_turn.score = 0
            player_turn.save(update_fields=['score'])
        else:
            player_turn.score = player_score
            player_turn.save(update_fields=['score'])

        player_scores = player_turns.values_list('score', flat=True)

        if -1 not in player_scores:
            #If the match_turn is complete, then create a new match_turn
            last_match_turn = MatchTurn.objects.filter(match_id=match_id).order_by('sequence').last()
            next_sequence = last_match_turn.sequence + 1

            # Create a new match turn
            match_turn = MatchTurn.objects.create(
                match_id=match_id,
                sequence=next_sequence
            )

            players = Match.objects.get(id=match_id).players.all()
            # Create player turn for every player
            for player in players:
                PlayerTurn.objects.create(
                    player=player,
                    match_turn=match_turn,
                    score=-1,  # initialize their score to -1 (-1 means the turn has NOT been taken!)
                )

        #Set a session variable with match_id
        request.session['match_id'] = match_id
        return redirect('game_no_match_id')

class LandingPageView(View):

    def get(self, request):
        return render(request, 'scorer/landingpage.html')