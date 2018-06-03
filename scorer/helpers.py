from .models import PlayerTurn, MatchPlayerOrder


class PlayerStatus(object):
    def __init__(self, match, player_turn):
        self.id = player_turn.player.id
        self.name = player_turn.player.name
        self.sequence = player_turn.sequence
        self.my_turn = False

        # Determine the overall score for this player
        turns_scores = PlayerTurn.objects.filter(player=player_turn.player, match_turn__match_id=match.id).values_list('score', flat=True)

        points_earned = 0
        for turn_score in turns_scores:

            # skip the turn scores that are -1!
            if turn_score == -1:
                continue

            points_earned += turn_score

        self.overall_score = match.starting_score - points_earned
