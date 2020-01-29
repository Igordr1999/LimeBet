from django.db import models
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from statistics import median

from datetime import datetime, timedelta, timezone


class Country(models.Model):
    """!
        Countries of the Earth

        This model stores the data of the countries of the Earth.
        @param name simple name of country
        @param alpha2 2-character ISO code
        @param rating limebet rating of country
        @param flag flag of country
    """

    name = models.CharField(max_length=64, unique=True, verbose_name=_('Name'))
    alpha2 = models.CharField(max_length=2, unique=True, verbose_name=_('Alpha2'))
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))
    flag = ProcessedImageField(processors=[ResizeToFill(68, 45)],
                               upload_to='data/country/',
                               format='PNG',
                               options={'quality': 60},
                               null=True,
                               verbose_name=_('Flag'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ["-rating", "name"]


class Bookmaker(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_('Name'))
    url = models.URLField(max_length=64, verbose_name=_('URL'))
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_('Country'))
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))
    logo = ProcessedImageField(upload_to='data/bookmaker/',
                               format='PNG',
                               options={'quality': 60},
                               null=True,
                               verbose_name=_('Logo'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Bookmaker')
        verbose_name_plural = _('Bookmakers')
        ordering = ["-rating", "name"]


class Sport(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_('Name'))
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Sport')
        verbose_name_plural = _('Sports')
        ordering = ["-rating", "name"]


class BookmakerTeamName(models.Model):
    team_name = models.CharField(max_length=64, verbose_name=_('Team name'))
    bookmaker = models.ForeignKey(Bookmaker, on_delete=models.CASCADE, verbose_name=_('Team name'))

    def __str__(self):
        return str("{}, {}".format(self.bookmaker, self.team_name))

    class Meta:
        verbose_name = _('Bookmaker team name')
        verbose_name_plural = _('Bookmaker team names')
        ordering = ["team_name"]


class Team(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('Name'))
    bookmaker_names = models.ManyToManyField(BookmakerTeamName, verbose_name=_('Bookmaker names'))
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, verbose_name=_('Sport'))
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_('Country'))
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))
    logo_url = models.URLField(max_length=256, null=True,
                               verbose_name=_('Logo url'))
    logo = ProcessedImageField(upload_to='data/team/',
                               format='PNG',
                               options={'quality': 60},
                               null=True,
                               verbose_name=_('Logo'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        from django.core.files.temp import NamedTemporaryFile
        import shutil
        import requests
        import uuid

        if self.logo_url is not None:
            self.code = uuid.uuid4().hex
            response = requests.get(self.logo_url, stream=True)
            img_temp = NamedTemporaryFile()
            shutil.copyfileobj(response.raw, img_temp)
            random_name = uuid.uuid4().hex + ".png"
            self.logo.save(random_name, img_temp, save=False)
        super(Team, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')
        ordering = ["name"]


class Handicap(models.Model):
    period_number = models.IntegerField(verbose_name=_('Period number'))
    team_number = models.IntegerField(verbose_name=_('Team number'))
    quote_name = models.FloatField(verbose_name=_('Quote name'))

    def __str__(self):
        return str("{}, {}, {}".format(self.period_number, self.team_number,  self.quote_name))

    class Meta:
        verbose_name = _('Handicap')
        verbose_name_plural = _('Handicaps')
        ordering = ["period_number", "team_number", "quote_name"]


class Total(models.Model):
    period_number = models.IntegerField(verbose_name=_('Period number'))
    team_number = models.IntegerField(verbose_name=_('Team number'))
    under_or_over = models.IntegerField(verbose_name=_('Under or over'))
    quote_name = models.FloatField(verbose_name=_('Quote name'))

    def __str__(self):
        return str("{}, {}, {}, {}".format(self.period_number, self.team_number, self.under_or_over, self.quote_name))

    class Meta:
        verbose_name = _('Total')
        verbose_name_plural = _('Totals')
        ordering = ["period_number", "team_number", "under_or_over", "quote_name"]


class Result(models.Model):
    period_number = models.IntegerField(verbose_name=_('Period number'))
    quote_name = models.IntegerField(verbose_name=_('Quote name'))

    def __str__(self):
        return str("{}, {}".format(self.period_number, self.quote_name))

    class Meta:
        verbose_name = _('Result')
        verbose_name_plural = _('Results')
        ordering = ["period_number", "quote_name"]


class HandicapQuote(models.Model):
    handicap = models.ForeignKey(Handicap, on_delete=models.CASCADE, verbose_name=_('Handicap'))
    quote_value = models.FloatField(verbose_name=_('Quote value'))

    def __str__(self):
        return str("{}, {}, {}, {}".format(self.handicap.period_number, self.handicap.team_number,
                                           self.handicap.quote_name, self.quote_value))

    def get_quote_text(self):
        full_time_text = _('full time')
        period_text = _('period')
        handicap_text = _('Handicap')

        period_number_text = "{} {}".format(period_text, self.handicap.period_number)
        period = full_time_text if self.handicap.period_number == 0 else period_number_text
        answer = str("{}-{} ({}), {}").format(handicap_text, self.handicap.team_number,
                                              self.handicap.quote_name, period)

        return answer

    class Meta:
        verbose_name = _('Handicap quote')
        verbose_name_plural = _('Handicap quotes')
        ordering = ["handicap", "quote_value"]


class TotalQuote(models.Model):
    total = models.ForeignKey(Total, on_delete=models.CASCADE, verbose_name=_('Total'))
    quote_value = models.FloatField(verbose_name=_('Quote value'))

    def __str__(self):
        return str("{}, {}, {}, {}, {}".format(self.total.period_number, self.total.team_number, self.total.under_or_over,
                                               self.total.quote_name, self.quote_value))

    def get_quote_text(self):
        full_time_text = _('full time')
        period_text = _('period')

        total_under = _('Total under')
        total_over = _('Total over')
        all_teams = _('all teams')

        under_or_over_text = total_under if self.total.under_or_over == -1 else total_over
        period_number_text = "{} {}".format(period_text, self.total.period_number)
        period_text = full_time_text if self.total.period_number == 0 else period_number_text
        team_text = all_teams if self.total.team_number == 0 else self.total.team_number
        answer = str("{} ({}), {}, {}").format(under_or_over_text,
                                               self.total.quote_name, team_text, period_text)

        return answer

    class Meta:
        verbose_name = _('Total quote')
        verbose_name_plural = _('Total quotes')
        ordering = ["total", "quote_value"]


class ResultQuote(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, verbose_name=_('Result'))
    quote_value = models.FloatField(verbose_name=_('Quote value'))

    def __str__(self):
        return str("{}, {}, {}".format(self.result.period_number, self.result.quote_name, self.quote_value))

    def get_quote_text(self):
        full_time_text = _('full time')
        period_text = _('period')
        handicap_text = _('Handicap')

        period_number_text = "{} {}".format(period_text, self.handicap.period_number)
        period = full_time_text if self.handicap.period_number == 0 else period_number_text
        answer = str("{}-{} ({}), {}").format(handicap_text, self.handicap.team_number,
                                              self.handicap.quote_name, period)

        return answer

    def get_quote_text(self):
        full_time_text = _('full time')
        period_text = _('period')
        result_text = _('Result')
        d = {
            0: "1",
            1: "X",
            2: "2",
            3: "1X",
            4: "12",
            5: "X2",
            6: "1OT",
            7: "2OT",
        }
        period = full_time_text if self.result.period_number == 0 else self.result.period_number
        answer = "{} {}, {}".format(result_text, d[self.result.quote_name], period)
        return answer

    class Meta:
        verbose_name = _('Result quote')
        verbose_name_plural = _('Result quotes')
        ordering = ["result", "quote_value"]


class Quotes(models.Model):
    handicap_quotes = models.ManyToManyField(HandicapQuote, null=True, verbose_name=_('Handicap quotes'))
    total_quotes = models.ManyToManyField(TotalQuote, null=True, verbose_name=_('Total quotes'))
    result_quotes = models.ManyToManyField(ResultQuote, null=True, verbose_name=_('Result quotes'))
    bookmaker = models.ForeignKey(Bookmaker, on_delete=models.CASCADE, verbose_name=_('Bookmaker'))
    bookmaker_event_url = models.URLField(verbose_name=_('Bookmaker event url'))
    update_time = models.DateTimeField(verbose_name=_('Update time'), auto_now=True)

    def __str__(self):
        return str("{}; {}; {}".format(self.bookmaker, self.update_time, self.bookmaker_event_url))

    class Meta:
        verbose_name = _('Quotes')
        verbose_name_plural = _('Quotes set')
        ordering = ["-update_time"]


class BookmakerUrl(models.Model):
    bookmaker = models.ForeignKey(Bookmaker, on_delete=models.CASCADE, verbose_name=_('Bookmaker'))
    url = models.URLField(verbose_name=_('URL'))

    def __str__(self):
        return str("{}; {}".format(self.bookmaker, self.url))

    class Meta:
        verbose_name = _('Bookmaker url')
        verbose_name_plural = _('Bookmaker urls')
        ordering = ["url"]


class League(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('Name'))
    bookmaker_urls = models.ManyToManyField(BookmakerUrl, verbose_name=_('Bookmaker urls'))
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, verbose_name=_('Sport'))
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, verbose_name=_('Country'))
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))
    logo = ProcessedImageField(upload_to='data/league/logo/',
                               format='PNG',
                               options={'quality': 60},
                               null=True,
                               verbose_name=_('Logo'))
    background = ProcessedImageField(upload_to='data/league/background/',
                                     format='PNG',
                                     options={'quality': 60},
                                     null=True,
                                     verbose_name=_('Background'))
    music = models.FileField(upload_to='data/league/music/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('League')
        verbose_name_plural = _('Leagues')
        ordering = ["-rating", "name"]


class Event(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_team", verbose_name=_('Home team'))
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_team", verbose_name=_('Away team'))
    league = models.ForeignKey(League, on_delete=models.CASCADE, verbose_name=_('League'))
    start_time = models.DateTimeField(verbose_name=_('Start time'))
    period1_team1 = models.IntegerField(default=0, verbose_name=_('Period 1; Team 1'))
    period1_team2 = models.IntegerField(default=0, verbose_name=_('Period 1; Team 2'))
    period2_team1 = models.IntegerField(default=0, verbose_name=_('Period 2; Team 1'))
    period2_team2 = models.IntegerField(default=0, verbose_name=_('Period 2; Team 2'))
    period3_team1 = models.IntegerField(default=0, verbose_name=_('Period 3; Team 1'))
    period3_team2 = models.IntegerField(default=0, verbose_name=_('Period 3; Team 2'))
    period4_team1 = models.IntegerField(default=0, verbose_name=_('Period 4; Team 1'))
    period4_team2 = models.IntegerField(default=0, verbose_name=_('Period 4; Team 2'))
    quotes = models.ManyToManyField(Quotes, null=True, blank=True, verbose_name=_('Quotes'))

    def __str__(self):
        return str("{} - {}; {}".format(self.home_team, self.away_team, self.start_time))

    @classmethod
    def get_upcoming_events(cls):
        now = datetime.now(tz=timezone.utc)
        future = now + timedelta(days=28)
        events = Event.objects.filter(start_time__gte=now,
                                      start_time__lte=future)
        return events

    @classmethod
    def get_upcoming_events_by_league(cls, league):
        now = datetime.now(tz=timezone.utc)
        future = now + timedelta(days=28)
        events = Event.objects.filter(start_time__gte=now,
                                      start_time__lte=future,
                                      league=league)
        return events

    @classmethod
    def get_upcoming_events_by_leagues(cls, leagues):
        events = list()
        for league in leagues:
            events += cls.get_upcoming_events_by_league(league=league)
        return events

    @classmethod
    def get_result_quote(cls, event, bookmaker, result):
        try:
            quote = event.quotes.get(bookmaker=bookmaker, result_quotes__result=result)
            quote_value = quote.result_quotes.get(result=result)
            return quote_value
        except Quotes.DoesNotExist:
            return None

    @classmethod
    def get_result_quote_value(cls, event, bookmaker, result):
        result_quote = cls.get_result_quote(event=event, bookmaker=bookmaker, result=result)
        return result_quote.quote_value if result_quote else None

    @classmethod
    def get_handicap_quote(cls, event, bookmaker, handicap):
        event = cls.objects.get(id=event.id)
        try:
            quote = event.quotes.get(bookmaker=bookmaker, handicap_quotes__handicap=handicap)
            quote_value = quote.handicap_quotes.get(handicap=handicap)
            return quote_value
        except Quotes.DoesNotExist:
            return None

    @classmethod
    def get_handicap_quote_value(cls, event, bookmaker, handicap):
        handicap_quote = cls.get_handicap_quote(event=event, bookmaker=bookmaker, handicap=handicap)
        return handicap_quote.quote_value if handicap_quote else None

    @classmethod
    def get_total_quote(cls, event, bookmaker, total):
        event = cls.objects.get(id=event.id)
        try:
            quote = event.quotes.get(bookmaker=bookmaker, total_quotes__total=total)
            quote_value = quote.total_quotes.get(total=total)
            return quote_value
        except Quotes.DoesNotExist:
            return None

    @classmethod
    def get_total_quote_value(cls, event, bookmaker, total):
        total_quote = cls.get_total_quote(event=event, bookmaker=bookmaker, total=total)
        return total_quote.quote_value if total_quote else None

    @classmethod
    def get_max(cls, couples):
        max_value = 0
        max_bookmaker = None
        for couple in couples:
            value, bookmaker = couple
            if value is not None and value > max_value:
                max_value = value
                max_bookmaker = bookmaker
        if max_value > 0:
            return max_value, max_bookmaker
        else:
            return None, None

    @classmethod
    def get_max_result_quote_by_bookmakers(cls, event, result, bookmakers):
        couples = list()
        for b in bookmakers:
            value = cls.get_result_quote_value(event=event, bookmaker=b, result=result)
            if value is not None:
                couples.append([value, b])
        max_value, max_bookmaker = cls.get_max(couples=couples)
        if max_value and max_bookmaker:
            return max_value, max_bookmaker
        else:
            return None, None

    @classmethod
    def get_max_handicap_quote_by_bookmakers(cls, event, handicap, bookmakers):
        couples = list()
        for b in bookmakers:
            value = cls.get_handicap_quote_value(event=event, bookmaker=b, handicap=handicap)
            if value is not None:
                couples.append([value, b])
        max_value, max_bookmaker = cls.get_max(couples=couples)
        if max_value and max_bookmaker:
            return max_value, max_bookmaker
        else:
            return None, None

    @classmethod
    def get_max_total_quote_by_bookmakers(cls, event, total, bookmakers):
        couples = list()
        for b in bookmakers:
            value = cls.get_total_quote_value(event=event, bookmaker=b, total=total)
            if value is not None:
                couples.append([value, b])
        max_value, max_bookmaker = cls.get_max(couples=couples)
        if max_value and max_bookmaker:
            return max_value, max_bookmaker
        else:
            return None, None

    @classmethod
    def get_max_result_quotes_by_bookmakers(cls, event, bookmakers):
        couples = list()
        results = Result.objects.all()
        for result in results:
            max_value, max_bookmaker = \
                cls.get_max_result_quote_by_bookmakers(event=event, result=result, bookmakers=bookmakers)
            if max_value and max_bookmaker:
                couples.append([result, max_value, max_bookmaker])
        return couples

    @classmethod
    def get_max_handicap_quotes_by_bookmakers(cls, event, bookmakers):
        couples = list()
        handicaps = Handicap.objects.all()
        for handicap in handicaps:
            max_value, max_bookmaker = \
                cls.get_max_handicap_quote_by_bookmakers(event=event, handicap=handicap, bookmakers=bookmakers)
            if max_value and max_bookmaker:
                couples.append([handicap, max_value, max_bookmaker])
        return couples

    @classmethod
    def get_max_total_quotes_by_bookmakers(cls, event, bookmakers):
        couples = list()
        totals = Total.objects.all()
        for total in totals:
            max_value, max_bookmaker = \
                cls.get_max_total_quote_by_bookmakers(event=event, total=total, bookmakers=bookmakers)
            if max_value and max_bookmaker:
                couples.append([total, max_value, max_bookmaker])
        return couples

    @classmethod
    def get_max_quotes_by_bookmakers(cls, event, bookmakers):
        results = cls.get_max_result_quotes_by_bookmakers(event=event, bookmakers=bookmakers)
        handicaps = cls.get_max_handicap_quotes_by_bookmakers(event=event, bookmakers=bookmakers)
        totals = cls.get_max_total_quotes_by_bookmakers(event=event, bookmakers=bookmakers)
        return results, handicaps, totals

    @classmethod
    def get_max_quotes(cls, event):
        bookmakers = Bookmaker.objects.all()
        results = cls.get_max_result_quotes_by_bookmakers(event=event, bookmakers=bookmakers)
        handicaps = cls.get_max_handicap_quotes_by_bookmakers(event=event, bookmakers=bookmakers)
        totals = cls.get_max_total_quotes_by_bookmakers(event=event, bookmakers=bookmakers)
        return [results, handicaps, totals]

    @classmethod
    def get_max_result_quote_value_by_all_bookmakers(cls, event, result):
        bookmakers = Bookmaker.objects.all()
        return cls.get_max_result_quote_by_bookmakers(event=event, result=result, bookmakers=bookmakers)

    @classmethod
    def get_max_handicap_quote_value_by_all_bookmakers(cls, event, handicap):
        bookmakers = Bookmaker.objects.all()
        return cls.get_max_handicap_quote_by_bookmakers(event=event, handicap=handicap, bookmakers=bookmakers)

    @classmethod
    def get_max_total_quote_value_by_all_bookmakers(cls, event, total):
        bookmakers = Bookmaker.objects.all()
        return cls.get_max_total_quote_by_bookmakers(event=event, total=total, bookmakers=bookmakers)

    @classmethod
    def get_max_quotes_by_path(cls, event):
        quotes = Event().get_max_quotes(event=event)

        max_results_quotes_period_0 = list()
        max_results_quotes_period_1 = list()
        max_results_quotes_period_2 = list()
        max_results_quotes_period_3 = list()
        max_results_quotes_period_4 = list()

        max_handicap_quotes_period_0 = list()
        max_handicap_quotes_period_1 = list()
        max_handicap_quotes_period_2 = list()
        max_handicap_quotes_period_3 = list()
        max_handicap_quotes_period_4 = list()

        max_total_quotes_period_0 = list()
        max_total_quotes_period_1 = list()
        max_total_quotes_period_2 = list()
        max_total_quotes_period_3 = list()
        max_total_quotes_period_4 = list()

        for quote in quotes[0]:
            if quote[0].period_number == 0:
                max_results_quotes_period_0.append(quote)
            elif quote[0].period_number == 1:
                max_results_quotes_period_1.append(quote)
            elif quote[0].period_number == 2:
                max_results_quotes_period_2.append(quote)
            elif quote[0].period_number == 3:
                max_results_quotes_period_3.append(quote)
            elif quote[0].period_number == 4:
                max_results_quotes_period_4.append(quote)
        new_max_results_quotes = [max_results_quotes_period_0,
                                  max_results_quotes_period_1,
                                  max_results_quotes_period_2,
                                  max_results_quotes_period_3,
                                  max_results_quotes_period_4]

        for quote in quotes[1]:
            if quote[0].period_number == 0:
                max_handicap_quotes_period_0.append(quote)
            elif quote[0].period_number == 1:
                max_handicap_quotes_period_1.append(quote)
            elif quote[0].period_number == 2:
                max_handicap_quotes_period_2.append(quote)
            elif quote[0].period_number == 3:
                max_handicap_quotes_period_3.append(quote)
            elif quote[0].period_number == 4:
                max_handicap_quotes_period_4.append(quote)
        new_max_handicap_quotes = [max_handicap_quotes_period_0,
                                   max_handicap_quotes_period_1,
                                   max_handicap_quotes_period_2,
                                   max_handicap_quotes_period_3,
                                   max_handicap_quotes_period_4]

        for quote in quotes[2]:
            if quote[0].period_number == 0:
                max_total_quotes_period_0.append(quote)
            elif quote[0].period_number == 1:
                max_total_quotes_period_1.append(quote)
            elif quote[0].period_number == 2:
                max_total_quotes_period_2.append(quote)
            elif quote[0].period_number == 3:
                max_total_quotes_period_3.append(quote)
            elif quote[0].period_number == 4:
                max_total_quotes_period_4.append(quote)
        new_max_total_quotes = [max_total_quotes_period_0,
                                max_total_quotes_period_1,
                                max_total_quotes_period_2,
                                max_total_quotes_period_3,
                                max_total_quotes_period_4]
        return new_max_results_quotes, new_max_handicap_quotes, new_max_total_quotes

    @classmethod
    def get_median_result_quote(cls, event, result):
        quote_values = list()
        bookmakers = Bookmaker.objects.all()
        for bookmaker in bookmakers:
            value = cls.get_result_quote_value(event=event, bookmaker=bookmaker, result=result)
            if value is not None:
                quote_values.append(value)
        return median(quote_values) if len(quote_values) > 0 else None

    @classmethod
    def get_median_handicap_quote(cls, event, handicap):
        quote_values = list()
        bookmakers = Bookmaker.objects.all()
        for bookmaker in bookmakers:
            value = cls.get_handicap_quote_value(event=event, bookmaker=bookmaker, handicap=handicap)
            if value is not None:
                quote_values.append(value)
        return median(quote_values) if len(quote_values) > 0 else None

    @classmethod
    def get_median_total_quote(cls, event, total):
        quote_values = list()
        bookmakers = Bookmaker.objects.all()
        for bookmaker in bookmakers:
            value = cls.get_total_quote_value(event=event, bookmaker=bookmaker, total=total)
            if value is not None:
                quote_values.append(value)
        return median(quote_values) if len(quote_values) > 0 else None

    @classmethod
    def get_median_result_quotes(cls, event):
        results = Result.objects.all()
        quotes = list()
        for result in results:
            value = cls.get_median_result_quote(event=event, result=result)
            if value is not None:
                quotes.append([result, round(value, 2)])
        return quotes

    @classmethod
    def get_median_handicap_quotes(cls, event):
        handicaps = Handicap.objects.all()
        quotes = list()
        for handicap in handicaps:
            value = cls.get_median_handicap_quote(event=event, handicap=handicap)
            if value is not None:
                quotes.append([handicap, round(value, 2)])
        return quotes

    @classmethod
    def get_median_total_quotes(cls, event):
        totals = Total.objects.all()
        quotes = list()
        for total in totals:
            value = cls.get_median_total_quote(event=event, total=total)
            if value is not None:
                quotes.append([total, round(value, 2)])
        return quotes

    @classmethod
    def get_median_quotes(cls, event):
        results = cls.get_median_result_quotes(event=event)
        handicaps = cls.get_median_handicap_quotes(event=event)
        totals = cls.get_median_total_quotes(event=event)
        return results, handicaps, totals

    @classmethod
    def get_median_quotes_by_path(cls, event):
        quotes = Event().get_median_quotes(event=event)

        median_results_quotes_period_0 = list()
        median_results_quotes_period_1 = list()
        median_results_quotes_period_2 = list()
        median_results_quotes_period_3 = list()
        median_results_quotes_period_4 = list()

        median_handicap_quotes_period_0 = list()
        median_handicap_quotes_period_1 = list()
        median_handicap_quotes_period_2 = list()
        median_handicap_quotes_period_3 = list()
        median_handicap_quotes_period_4 = list()

        median_total_quotes_period_0 = list()
        median_total_quotes_period_1 = list()
        median_total_quotes_period_2 = list()
        median_total_quotes_period_3 = list()
        median_total_quotes_period_4 = list()

        for quote in quotes[0]:
            if quote[0].period_number == 0:
                median_results_quotes_period_0.append(quote)
            elif quote[0].period_number == 1:
                median_results_quotes_period_1.append(quote)
            elif quote[0].period_number == 2:
                median_results_quotes_period_2.append(quote)
            elif quote[0].period_number == 3:
                median_results_quotes_period_3.append(quote)
            elif quote[0].period_number == 4:
                median_results_quotes_period_4.append(quote)
        new_median_results_quotes = [median_results_quotes_period_0,
                                     median_results_quotes_period_1,
                                     median_results_quotes_period_2,
                                     median_results_quotes_period_3,
                                     median_results_quotes_period_4]

        for quote in quotes[1]:
            if quote[0].period_number == 0:
                median_handicap_quotes_period_0.append(quote)
            elif quote[0].period_number == 1:
                median_handicap_quotes_period_1.append(quote)
            elif quote[0].period_number == 2:
                median_handicap_quotes_period_2.append(quote)
            elif quote[0].period_number == 3:
                median_handicap_quotes_period_3.append(quote)
            elif quote[0].period_number == 4:
                median_handicap_quotes_period_4.append(quote)
        new_median_handicap_quotes = [median_handicap_quotes_period_0,
                                      median_handicap_quotes_period_1,
                                      median_handicap_quotes_period_2,
                                      median_handicap_quotes_period_3,
                                      median_handicap_quotes_period_4]

        for quote in quotes[2]:
            if quote[0].period_number == 0:
                median_total_quotes_period_0.append(quote)
            elif quote[0].period_number == 1:
                median_total_quotes_period_1.append(quote)
            elif quote[0].period_number == 2:
                median_total_quotes_period_2.append(quote)
            elif quote[0].period_number == 3:
                median_total_quotes_period_3.append(quote)
            elif quote[0].period_number == 4:
                median_total_quotes_period_4.append(quote)
        new_median_total_quotes = [median_total_quotes_period_0,
                                   median_total_quotes_period_1,
                                   median_total_quotes_period_2,
                                   median_total_quotes_period_3,
                                   median_total_quotes_period_4]

        return new_median_results_quotes, new_median_handicap_quotes, new_median_total_quotes

    @classmethod
    def check_surebet_by_shoulders(cls, shoulder_a, shoulder_b, shoulder_c=None):
        if not (shoulder_a[0] and shoulder_a[1] and shoulder_b[0] and shoulder_b[1]):
            return False
        try:
            if shoulder_c:
                my_sum = 1 / shoulder_a[0] + 1 / shoulder_b[0] + 1 / shoulder_c[0]
            else:
                my_sum = 1 / shoulder_a[0] + 1 / shoulder_b[0]
        except ZeroDivisionError:
            return False
        print(my_sum, shoulder_a, shoulder_b, shoulder_c)
        if my_sum >= 1.05:
            return False
        return True

    @classmethod
    def get_surebet_value_by_shoulders(cls, shoulder_a, shoulder_b, shoulder_c=None):
        if shoulder_c:
            my_sum = 1 / shoulder_a[0] + 1 / shoulder_b[0] + 1 / shoulder_c[0]
        else:
            my_sum = 1 / shoulder_a[0] + 1 / shoulder_b[0]
        answer = -1 * (my_sum-1)
        return round(answer, 2)

    @classmethod
    def opposite_results(cls):
        surebets = list()

        r_0_1 = Result.objects.get(period_number=0, quote_name=0)
        r_0_x = Result.objects.get(period_number=0, quote_name=1)
        r_0_2 = Result.objects.get(period_number=0, quote_name=2)
        r_0_1x = Result.objects.get(period_number=0, quote_name=3)
        r_0_12 = Result.objects.get(period_number=0, quote_name=4)
        r_0_x2 = Result.objects.get(period_number=0, quote_name=5)

        r_1_1 = Result.objects.get(period_number=1, quote_name=0)
        r_1_x = Result.objects.get(period_number=1, quote_name=1)
        r_1_2 = Result.objects.get(period_number=1, quote_name=2)
        r_1_1x = Result.objects.get(period_number=1, quote_name=3)
        r_1_12 = Result.objects.get(period_number=1, quote_name=4)
        r_1_x2 = Result.objects.get(period_number=1, quote_name=5)

        r_2_1 = Result.objects.get(period_number=2, quote_name=0)
        r_2_x = Result.objects.get(period_number=2, quote_name=1)
        r_2_2 = Result.objects.get(period_number=2, quote_name=2)
        r_2_1x = Result.objects.get(period_number=2, quote_name=3)
        r_2_12 = Result.objects.get(period_number=2, quote_name=4)
        r_2_x2 = Result.objects.get(period_number=2, quote_name=5)

        surebets = [
            [r_0_1, r_0_x2, None],
            [r_0_x, r_0_12, None],
            [r_0_2, r_0_1x, None],
            [r_0_1, r_0_x, r_0_2],

            [r_1_1, r_1_x2, None],
            [r_1_x, r_1_12, None],
            [r_1_2, r_1_1x, None],
            [r_1_1, r_1_x, r_1_2],

            [r_2_1, r_2_x2, None],
            [r_2_x, r_2_12, None],
            [r_2_2, r_2_1x, None],
            [r_2_1, r_2_x, r_2_2],
        ]

        return surebets

    @classmethod
    def opposite_handicaps(cls):
        surebets = list()
        handicaps = Handicap.objects.all()
        for handicap in handicaps:
            if handicap.quote_name > 0:
                try:
                    reverse = Handicap.objects.get(period_number=handicap.period_number,
                                                   team_number=1 if handicap.team_number == 2 else 2,
                                                   quote_name=(handicap.quote_name * (-1)))
                except Handicap.DoesNotExist:
                    continue
                surebets.append([handicap, reverse])
        return surebets

    @classmethod
    def opposite_totals(cls):
        surebets = list()
        totals = Total.objects.all()
        for total in totals:
            if total.quote_name > 0:
                try:
                    reverse = Total.objects.get(period_number=total.period_number,
                                                team_number=total.team_number,
                                                quote_name=total.quote_name,
                                                under_or_over=-1 if total.under_or_over == 1 else 1,
                                                )
                except Handicap.DoesNotExist:
                    continue
                surebets.append([total, reverse])
        return surebets

    @classmethod
    def check_surebet_results(cls, event, bookmakers):
        real_surebets = list()
        potential_surebets = cls.opposite_results()

        for surebet in potential_surebets:
            shoulder_a, shoulder_b, shoulder_c = surebet

            a = cls.get_max_result_quote_by_bookmakers(event=event, result=shoulder_a, bookmakers=bookmakers)
            b = cls.get_max_result_quote_by_bookmakers(event=event, result=shoulder_b, bookmakers=bookmakers)

            max_value_a, max_bookmaker_a = a
            max_value_b, max_bookmaker_b = b

            if shoulder_c:
                c = cls.get_max_result_quote_by_bookmakers(event=event, result=shoulder_c, bookmakers=bookmakers)
                is_surebet = cls.check_surebet_by_shoulders(a, b, c)
                if is_surebet:
                    surebet_value = cls.get_surebet_value_by_shoulders(a, b, c)
                max_value_c, max_bookmaker_c = c
            else:
                is_surebet = cls.check_surebet_by_shoulders(a, b)
                if is_surebet:
                    surebet_value = cls.get_surebet_value_by_shoulders(a, b)

            if is_surebet and shoulder_c:
                q_a = cls.get_result_quote(event=event, bookmaker=max_bookmaker_a, result=shoulder_a)
                q_b = cls.get_result_quote(event=event, bookmaker=max_bookmaker_b, result=shoulder_b)
                q_c = cls.get_result_quote(event=event, bookmaker=max_bookmaker_c, result=shoulder_c)
                real_surebets.append([
                    [q_a, a[1]],
                    [q_b, b[1]],
                    [q_c, c[1]],
                    surebet_value,
                ]
                )
            elif is_surebet:
                q_a = cls.get_result_quote(event=event, bookmaker=max_bookmaker_a, result=shoulder_a)
                q_b = cls.get_result_quote(event=event, bookmaker=max_bookmaker_b, result=shoulder_b)
                real_surebets.append([
                    [q_a, a[1]],
                    [q_b, b[1]],
                    None,
                    surebet_value,
                ]
                )

        return real_surebets

    @classmethod
    def check_surebet_handicaps(cls, event, bookmakers):
        real_surebets = list()
        potential_surebets = cls.opposite_handicaps()

        for surebet in potential_surebets:
            shoulder_a, shoulder_b = surebet
            a = cls.get_max_handicap_quote_by_bookmakers(event=event, handicap=shoulder_a, bookmakers=bookmakers)
            b = cls.get_max_handicap_quote_by_bookmakers(event=event, handicap=shoulder_b, bookmakers=bookmakers)

            is_surebet = cls.check_surebet_by_shoulders(a, b)

            max_value_a, max_bookmaker_a = a
            max_value_b, max_bookmaker_b = b

            if is_surebet:
                q_a = cls.get_handicap_quote(event=event, bookmaker=max_bookmaker_a, handicap=shoulder_a)
                q_b = cls.get_handicap_quote(event=event, bookmaker=max_bookmaker_b, handicap=shoulder_b)
                surebet_value = cls.get_surebet_value_by_shoulders(a, b)
                real_surebets.append([
                    [q_a, a[1]],
                    [q_b, b[1]],
                    None,
                    surebet_value,
                    ]
                )
        return real_surebets

    @classmethod
    def check_surebet_totals(cls, event, bookmakers):
        real_surebets = list()
        potential_surebets = cls.opposite_totals()

        for surebet in potential_surebets:
            shoulder_a, shoulder_b = surebet
            a = cls.get_max_total_quote_by_bookmakers(event=event, total=shoulder_a, bookmakers=bookmakers)
            b = cls.get_max_total_quote_by_bookmakers(event=event, total=shoulder_b, bookmakers=bookmakers)

            is_surebet = cls.check_surebet_by_shoulders(a, b)

            max_value_a, max_bookmaker_a = a
            max_value_b, max_bookmaker_b = b

            if is_surebet:
                q_a = cls.get_total_quote(event=event, bookmaker=max_bookmaker_a, total=shoulder_a)
                q_b = cls.get_total_quote(event=event, bookmaker=max_bookmaker_b, total=shoulder_b)
                surebet_value = cls.get_surebet_value_by_shoulders(a, b)
                real_surebets.append([
                    [q_a, a[1]],
                    [q_b, b[1]],
                    None,
                    surebet_value,
                ]
                )
        return real_surebets

    @classmethod
    def check_surebets_by_event(cls, event, bookmakers):
        surebet_results = cls.check_surebet_results(event=event, bookmakers=bookmakers)
        surebet_handicaps = cls.check_surebet_handicaps(event=event, bookmakers=bookmakers)
        surebet_totals = cls.check_surebet_totals(event=event, bookmakers=bookmakers)
        if surebet_results or surebet_handicaps or surebet_totals:
            return surebet_results, surebet_handicaps, surebet_totals, event
        else:
            return None

    @classmethod
    def check_surebets_by_events(cls, events, bookmakers):
        answer = list()
        for event in events:
            a = cls.check_surebets_by_event(event=event, bookmakers=bookmakers)
            if a[0] or a[1] or a[2]:
                answer.append(a)
        return answer

    @classmethod
    def check_surebets_by_leagues(cls, leagues, bookmakers):
        events = cls.get_upcoming_events_by_leagues(leagues=leagues)
        surebets = cls.check_surebets_by_events(events=events, bookmakers=bookmakers)
        return surebets

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ["-start_time"]
