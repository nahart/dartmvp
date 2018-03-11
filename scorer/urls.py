from django.conf.urls import url
from . import views
from .views import DartView

urlpatterns = [
    url(r'^$', DartView.as_view(), name='index') #Reg Ex means phrase that starts and ends (index)
]