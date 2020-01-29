from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from .models import Country, Bookmaker, Sport, BookmakerTeamName, Team, Handicap, Total, Result, \
    HandicapQuote, TotalQuote, ResultQuote, Quotes, BookmakerUrl, League, Event
from .serializers import CountrySerializer, BookmakerSerializer, SportSerializer, BookmakerTeamNameSerializer, \
    TeamSerializer, HandicapSerializer, TotalSerializer, ResultSerializer, HandicapQuoteSerializer, \
    TotalQuoteSerializer, ResultQuoteSerializer, QuotesSerializer, BookmakerUrlSerializer, LeagueSerializer, \
    EventSerializer, EventShortSerializer


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ('name', 'alpha2', 'rating')
    ordering_fields = ('name', 'alpha2', 'rating')
    search_fields = ('name', 'alpha2', 'rating')


class BookmakerListView(generics.ListAPIView):
    queryset = Bookmaker.objects.all()
    serializer_class = BookmakerSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ('id', 'name', 'url', 'country', 'rating')
    ordering_fields = ('id', 'name', 'url', 'country', 'rating')
    search_fields = ('id', 'name', 'url', 'country', 'rating')


class SportListView(generics.ListAPIView):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ('id', 'name', 'rating')
    ordering_fields = ('id', 'name', 'rating')
    search_fields = ('id', 'name', 'rating')


class BookmakerTeamNameListView(generics.ListAPIView):
    queryset = BookmakerTeamName.objects.all()
    serializer_class = BookmakerTeamNameSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ('id', 'team_name', 'bookmaker')
    ordering_fields = ('id', 'team_name', 'bookmaker')
    search_fields = ('id', 'team_name', 'bookmaker')


class TeamListView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ('id', 'name', 'sport', 'country', 'rating', 'country__alpha2')
    ordering_fields = ('id', 'name', 'sport', 'country', 'rating', 'country__alpha2')
    search_fields = ('id', 'name', 'sport', 'country', 'rating', 'country__alpha2')


class HandicapListView(generics.ListAPIView):
    queryset = Handicap.objects.all()
    serializer_class = HandicapSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ('id', 'period_number', 'team_number', 'quote_name')
    ordering_fields = ('id', 'period_number', 'team_number', 'quote_name')
    search_fields = ('id', 'period_number', 'team_number', 'quote_name')


class TotalListView(generics.ListAPIView):
    queryset = Total.objects.all()
    serializer_class = TotalSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ('id', 'period_number', 'team_number', 'under_or_over', 'quote_name')
    ordering_fields = ('id', 'period_number', 'team_number', 'under_or_over', 'quote_name')
    search_fields = ('id', 'period_number', 'team_number', 'under_or_over', 'quote_name')


class ResultListView(generics.ListAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ('id', 'period_number', 'quote_name')
    ordering_fields = ('id', 'period_number', 'quote_name')
    search_fields = ('id', 'period_number', 'quote_name')


class HandicapQuoteListView(generics.ListAPIView):
    queryset = HandicapQuote.objects.all()
    serializer_class = HandicapQuoteSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ('id', 'handicap', 'quote_value')
    ordering_fields = ('id', 'handicap', 'quote_value')
    search_fields = ('id', 'handicap', 'quote_value')


class TotalQuoteListView(generics.ListAPIView):
    queryset = TotalQuote.objects.all()
    serializer_class = TotalQuoteSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ('id', 'total', 'quote_value')
    ordering_fields = ('id', 'total', 'quote_value')
    search_fields = ('id', 'total', 'quote_value')


class ResultQuoteListView(generics.ListAPIView):
    queryset = ResultQuote.objects.all()
    serializer_class = ResultQuoteSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ('id', 'result', 'quote_value')
    ordering_fields = ('id', 'result', 'quote_value')
    search_fields = ('id', 'result', 'quote_value')


class QuotesListView(generics.ListAPIView):
    queryset = Quotes.objects.all()
    serializer_class = QuotesSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ('id', 'handicap_quotes', 'total_quotes', 'result_quotes', 'bookmaker', 'bookmaker_event_url',
                     'update_time')
    ordering_fields = ('id', 'handicap_quotes', 'total_quotes', 'result_quotes', 'bookmaker', 'bookmaker_event_url',
                       'update_time')
    search_fields = ('id', 'handicap_quotes', 'total_quotes', 'result_quotes', 'bookmaker', 'bookmaker_event_url',
                     'update_time')


class BookmakerUrlListView(generics.ListAPIView):
    queryset = BookmakerUrl.objects.all()
    serializer_class = BookmakerUrlSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ('id', 'bookmaker', 'url')
    ordering_fields = ('id', 'bookmaker', 'url')
    search_fields = ('id', 'bookmaker', 'url')


class LeagueListView(generics.ListAPIView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ('id', 'name', 'sport', 'country', 'rating')
    ordering_fields = ('id', 'name', 'sport', 'country', 'rating')
    search_fields = ('id', 'name', 'sport', 'country', 'rating')


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ('id', 'home_team', 'away_team', 'league', 'league__sport__id', 'league__country__id',
                     'start_time', 'period1_team1', 'period1_team2',
                     'period2_team1', 'period2_team2', 'period3_team1', 'period3_team2',
                     'period4_team1', 'period4_team2', 'quotes')
    ordering_fields = ('id', 'home_team', 'away_team', 'league', 'league__sport__id', 'league__country__id',
                       'start_time', 'period1_team1', 'period1_team2',
                       'period2_team1', 'period2_team2', 'period3_team1', 'period3_team2',
                       'period4_team1', 'period4_team2', 'quotes')
    search_fields = ('id', 'home_team', 'away_team', 'league', 'league__sport__id', 'league__country__id',
                     'start_time', 'period1_team1', 'period1_team2',
                     'period2_team1', 'period2_team2', 'period3_team1', 'period3_team2',
                     'period4_team1', 'period4_team2', 'quotes')


class EventShortListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventShortSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ('id', 'home_team', 'away_team', 'league', 'league__sport__id', 'league__country__id',
                     'start_time', 'period1_team1', 'period1_team2',
                     'period2_team1', 'period2_team2', 'period3_team1', 'period3_team2',
                     'period4_team1', 'period4_team2', 'quotes')
    ordering_fields = ('id', 'home_team', 'away_team', 'league', 'league__sport__id', 'league__country__id',
                       'start_time', 'period1_team1', 'period1_team2',
                       'period2_team1', 'period2_team2', 'period3_team1', 'period3_team2',
                       'period4_team1', 'period4_team2', 'quotes')
    search_fields = ('id', 'home_team', 'away_team', 'league', 'league__sport__id', 'league__country__id',
                     'start_time', 'period1_team1', 'period1_team2',
                     'period2_team1', 'period2_team2', 'period3_team1', 'period3_team2',
                     'period4_team1', 'period4_team2', 'quotes')
