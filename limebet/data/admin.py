from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Country, Bookmaker, Sport, BookmakerTeamName,\
    Team, Handicap, Total, Result, BookmakerUrl, League, Event, Quotes


@admin.register(Country)
class CountryAdmin(TranslationAdmin):
    list_display = ['name_en', 'name_ru', 'name_de', 'alpha2', 'rating']
    list_filter = ['name_en']


@admin.register(Bookmaker)
class BookmakerAdmin(TranslationAdmin):
    list_display = ['name_en', 'name_ru', 'name_de', 'url', 'country', 'rating']
    list_filter = ['name_en']


@admin.register(Sport)
class SportAdmin(TranslationAdmin):
    list_display = ['name_en', 'name_ru', 'name_de', 'name', 'rating']
    list_filter = ['name_en']


@admin.register(BookmakerTeamName)
class BookmakerTeamNameAdmin(admin.ModelAdmin):
    list_display = ['team_name', 'bookmaker']
    list_filter = ['bookmaker']


@admin.register(Team)
class TeamNameAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'name_ru', 'name_de', 'name', 'rating', 'sport', 'country']
    list_filter = ['sport', 'country']


@admin.register(Handicap)
class HandicapAdmin(admin.ModelAdmin):
    list_display = ['period_number', 'team_number', 'quote_name']
    list_filter = ['period_number', 'team_number']


@admin.register(Total)
class TotalAdmin(admin.ModelAdmin):
    list_display = ['period_number', 'team_number', 'under_or_over', 'quote_name']
    list_filter = ['period_number', 'team_number', 'under_or_over']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['period_number', 'quote_name']
    list_filter = ['period_number']


@admin.register(Quotes)
class QuotesAdmin(admin.ModelAdmin):
    list_display = ['bookmaker', 'bookmaker_event_url', 'update_time']
    list_filter = ['bookmaker']


@admin.register(BookmakerUrl)
class BookmakerUrlAdmin(admin.ModelAdmin):
    list_display = ['bookmaker', 'url']
    list_filter = ['bookmaker']


@admin.register(League)
class LeagueAdmin(TranslationAdmin):
    list_display = ['name', 'sport', 'country', 'rating']
    list_filter = ['sport', 'country']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['home_team', 'away_team', 'league', 'start_time']
    list_filter = ['league']
