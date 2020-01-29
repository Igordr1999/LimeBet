from rest_framework import serializers

from .models import Country, Bookmaker, Sport, BookmakerTeamName, Team, Handicap, Total, Result, \
    HandicapQuote, TotalQuote, ResultQuote, Quotes, BookmakerUrl, League, Event


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name', 'alpha2', 'rating', 'flag')


class BookmakerSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = Bookmaker
        fields = ('id', 'name', 'url', 'country', 'rating', 'logo')


class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ('id', 'name', 'rating')


class BookmakerTeamNameSerializer(serializers.ModelSerializer):
    bookmaker = BookmakerSerializer()

    class Meta:
        model = BookmakerTeamName
        fields = ('id', 'team_name', 'bookmaker')


class TeamSerializer(serializers.ModelSerializer):
    sport = SportSerializer()
    country = CountrySerializer()

    class Meta:
        model = Team
        fields = ('id', 'name', 'sport', 'country', 'rating', 'logo')


class HandicapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Handicap
        fields = ('id', 'period_number', 'team_number', 'quote_name')


class TotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Total
        fields = ('id', 'period_number', 'team_number', 'under_or_over', 'quote_name')


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('id', 'period_number', 'quote_name')


class HandicapQuoteSerializer(serializers.ModelSerializer):
    handicap = HandicapSerializer()

    class Meta:
        model = HandicapQuote
        fields = ('id', 'handicap', 'quote_value')


class TotalQuoteSerializer(serializers.ModelSerializer):
    total = TotalSerializer()

    class Meta:
        model = TotalQuote
        fields = ('id', 'total', 'quote_value')


class ResultQuoteSerializer(serializers.ModelSerializer):
    result = ResultSerializer()

    class Meta:
        model = ResultQuote
        fields = ('id', 'result', 'quote_value')


class QuotesSerializer(serializers.ModelSerializer):
    handicap_quotes = HandicapQuoteSerializer(many=True)
    total_quotes = TotalQuoteSerializer(many=True)
    result_quotes = ResultQuoteSerializer(many=True)
    bookmaker = BookmakerSerializer()

    class Meta:
        model = Quotes
        fields = ('id', 'handicap_quotes', 'total_quotes', 'result_quotes', 'bookmaker', 'bookmaker_event_url',
                  'update_time')


class BookmakerUrlSerializer(serializers.ModelSerializer):
    bookmaker = BookmakerSerializer()

    class Meta:
        model = BookmakerUrl
        fields = ('id', 'bookmaker', 'url')


class LeagueSerializer(serializers.ModelSerializer):
    sport = SportSerializer()
    country = CountrySerializer()

    class Meta:
        model = League
        fields = ('id', 'name', 'sport', 'country', 'rating', 'logo', 'background', 'music')


class EventSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer()
    away_team = TeamSerializer()
    league = LeagueSerializer()
    quotes = QuotesSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id', 'home_team', 'away_team', 'league', 'start_time', 'period1_team1', 'period1_team2',
                  'period2_team1', 'period2_team2', 'period3_team1', 'period3_team2',
                  'period4_team1', 'period4_team2', 'quotes')


class EventShortSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer()
    away_team = TeamSerializer()
    league = LeagueSerializer()

    class Meta:
        model = Event
        fields = ('id', 'home_team', 'away_team', 'league',
                  'start_time',
                  'period1_team1', 'period1_team2',
                  'period2_team1', 'period2_team2', 'period3_team1', 'period3_team2',
                  'period4_team1', 'period4_team2', 'quotes')
