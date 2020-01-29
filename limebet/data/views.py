from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Country, Bookmaker, Sport, BookmakerTeamName, Team, Handicap, Total, Result, \
    HandicapQuote, TotalQuote, ResultQuote, Quotes, BookmakerUrl, League, Event

from datetime import datetime, timezone, timedelta

from django_filters.views import FilterView
from .forms import TeamParamForm, LeagueParamForm


class CountryListView(ListView):
    model = Country
    paginate_by = 10
    template_name = "data/countries.html"


class BookmakerListView(ListView):
    model = Bookmaker
    paginate_by = 10
    template_name = "data/bookmakers.html"


class SportListView(ListView):
    model = Sport
    paginate_by = 10
    template_name = "data/sports.html"


class TeamListView(FilterView):
    template_name = "data/teams.html"
    filterset_class = TeamParamForm
    paginate_by = 20


class LeagueListView(FilterView):
    template_name = "data/leagues.html"
    filterset_class = LeagueParamForm
    paginate_by = 20


class EventDetailView(DetailView):
    model = Event
    slug_field = "id"
    slug_url_kwarg = "id"
    template_name = "data/event.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quotes = Event().get_max_quotes_by_path(event=self.get_object())

        context['new_max_results_quotes'] = quotes[0]
        context['new_max_handicap_quotes'] = quotes[1]
        context['new_max_total_quotes'] = quotes[2]
        return context


class BetDetailView(DetailView):
    model = Event
    slug_field = "id"
    slug_url_kwarg = "id"
    template_name = "data/bet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        quotes = Event().get_median_quotes_by_path(event=self.get_object())

        context['new_median_results_quotes'] = quotes[0]
        context['new_median_handicap_quotes'] = quotes[1]
        context['new_median_total_quotes'] = quotes[2]
        return context


class EventListView(ListView):
    model = Event
    slug_field = "id"
    slug_url_kwarg = "id"
    template_name = "data/events.html"

    def get_queryset(self):
        now = datetime.now(tz=timezone.utc)
        future = now + timedelta(days=28)
        return Event.objects.filter(start_time__gte=now,
                                    start_time__lte=future).order_by("start_time")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sports = Sport.objects.all()
        leagues = League.objects.all()
        context['sports'] = sports
        context['leagues'] = leagues
        return context


class BetListView(ListView):
    model = Event
    slug_field = "id"
    slug_url_kwarg = "id"
    template_name = "data/bets.html"

    def get_queryset(self):
        now = datetime.now(tz=timezone.utc)
        future = now + timedelta(days=28)
        return Event.objects.filter(start_time__gte=now,
                                    start_time__lte=future).order_by("start_time")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sports = Sport.objects.all()
        leagues = League.objects.all()
        context['sports'] = sports
        context['leagues'] = leagues
        return context


def surebets(request):
    return render(request, 'data/surebets.html')


def valuebets(request):
    return render(request, 'data/valuebets.html')
