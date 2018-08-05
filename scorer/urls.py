from django.conf.urls import url
from .views import DartView, StartGameView, GameView, LandingPageView

urlpatterns = [
    url(r'^$', DartView.as_view(), name='scorer'),

    url(r'^start_game/(?P<match_id>\d+)', StartGameView.as_view(), name='start_game'),
    url(r'^start_game/', StartGameView.as_view(), name='start_game'),

    url(r'^game/(?P<match_id>\d+)/$', GameView.as_view(), name='game'),
    url(r'^game/$', GameView.as_view(), name='game_no_match_id'),
    url(r'^landingpage/', LandingPageView.as_view(), name='landingPage')
]