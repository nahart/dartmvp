# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .models import Player, MatchTurn

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
        print request.POST