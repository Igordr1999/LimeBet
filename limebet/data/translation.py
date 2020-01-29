from modeltranslation.translator import TranslationOptions, translator

from .models import Country, Bookmaker, Sport, Team, League


class CountryTranslationOptions(TranslationOptions):
    fields = ('name',)


class BookmakerTranslationOptions(TranslationOptions):
    fields = ('name',)


class SportTranslationOptions(TranslationOptions):
    fields = ('name',)


class TeamTranslationOptions(TranslationOptions):
    fields = ('name',)


class LeagueTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Country, CountryTranslationOptions)
translator.register(Bookmaker, BookmakerTranslationOptions)
translator.register(Sport, SportTranslationOptions)
translator.register(Team, TeamTranslationOptions)
translator.register(League, LeagueTranslationOptions)
