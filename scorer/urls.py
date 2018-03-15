from django.conf.urls import url
from . import views
from .views import DartView
from .views import SettingsView

urlpatterns = [
    url(r'^$', DartView.as_view(), name='index'), #Reg Ex means phrase that starts and ends (index)
    url(r'^start_game/', SettingsView.as_view(), name='start_game')
]