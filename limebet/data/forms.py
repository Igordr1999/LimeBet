from django import forms
import django_filters
from .models import Team, League


class TeamParamForm(django_filters.FilterSet):
    class Meta:
        model = Team
        fields = ['name', 'sport', 'country']


class LeagueParamForm(django_filters.FilterSet):
    class Meta:
        model = League
        fields = ['name', 'sport', 'country']
