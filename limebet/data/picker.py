from .models import League, Event, Team, Handicap, HandicapQuote, Total, TotalQuote, Result, ResultQuote, Quotes, \
    Bookmaker, BookmakerUrl
from .parsers.baltbet import Baltbet
from .parsers.fonbet import Fonbet
from .parsers.leon import Leon
from .parsers.mbet import Mbet
from .parsers.parimatch import Parimatch
from .parsers.winline import Winline
from .parsers.xbet import Xbet
from multiprocessing import Pool
import threading
import asyncio

from datetime import datetime, timezone, timedelta


class Picker(object):
    sport_dict = {
        "Football": 1,
    }

    bookmaker_dict = {
        "Baltbet": 1,
        "Fonbet": 2,
        "Leon": 3,
        "MarathonBet": 4,
        "Parimatch": 5,
        "Winline": 6,
        "1XBET": 7,
    }

    d_dict = {
        "Baltbet Football": Baltbet,
        "Fonbet Football": Fonbet,
        "Leon Football": Leon,
        "MarathonBet Football": Mbet,
        "Parimatch Football": Parimatch,
        "Winline Football": Winline,
        "1XBET Football": Xbet,
    }

    football_obj = {
        "Baltbet": Baltbet,
        "Fonbet": Fonbet,
        "Leon": Leon,
        "MarathonBet": Mbet,
        "Parimatch": Parimatch,
        "Winline": Winline,
        "1XBET": Xbet,
    }

    def get_upcoming_event(self, home_team, away_team):
        now = datetime.now(tz=timezone.utc)
        future = now + timedelta(days=28)
        event = Event.objects.get(home_team=home_team,
                                  away_team=away_team,
                                  start_time__gte=now,
                                  start_time__lte=future)
        return event

    def get_bookmakers_urls(self, league):
        urls = list()
        bookmakers = Bookmaker.objects.all()
        for bookmaker in bookmakers:
            b_url = BookmakerUrl.objects.get(league=league, bookmaker=bookmaker).url
            urls.append([bookmaker, b_url])
        print(urls)
        return urls

    def get_bookmaker_obj(self, bookmaker_name, sport_name="Football"):
        mask = "{} {}".format(bookmaker_name, sport_name)
        obj = self.d_dict[mask]()
        return obj

    def get_all_data(self, league_ids):
        futures = [self.get_data(id=i) for i in league_ids]
        return True

    def get_data(self, id):
        league = League.objects.get(id=id)
        bookmaker_url_couples = self.get_bookmakers_urls(league=league)
        for couple in bookmaker_url_couples:
            bookmaker, url = couple
            bookmaker_obj = self.get_bookmaker_obj(bookmaker_name=bookmaker.name_en, sport_name="Football")
            event_urls = bookmaker_obj.get_events_urls_by_leagues_urls(urls=[url])
            pages = list()
            for league in event_urls:
                pages += league[0]
            compressed_data = bookmaker_obj.get_all_quotes_by_urls(urls=pages)
            self.create_new_quotes(compressed_data=compressed_data, bookmaker=bookmaker)

    def create_new_quotes(self, compressed_data, bookmaker):
        for one_row in compressed_data:
            results, handicaps, totals, teams, url = one_row
            try:
                home_team = Team.objects.get(bookmaker_names__bookmaker=bookmaker,
                                             bookmaker_names__team_name=teams[0])
                away_team = Team.objects.get(bookmaker_names__bookmaker=bookmaker,
                                             bookmaker_names__team_name=teams[1])
                event = self.get_upcoming_event(home_team=home_team, away_team=away_team)
                quotes = None
                result_objects = self.get_results(results)
                handicaps_objects = self.get_handicaps(handicaps)
                totals_objects = self.get_totals(totals)
                event_url = url
                try:
                    quotes = Quotes.objects.get(event=event, bookmaker=bookmaker)
                    quotes.delete()
                except Quotes.DoesNotExist:
                    pass
                quotes = Quotes.objects.create(bookmaker=bookmaker,
                                               bookmaker_event_url=event_url)
                quotes.handicap_quotes.add(*handicaps_objects)
                quotes.total_quotes.add(*totals_objects)
                quotes.result_quotes.add(*result_objects)

                event.quotes.add(quotes)
            except Event.DoesNotExist:
                continue
            except Team.DoesNotExist:
                continue
    """
        Result
    """
    def get_result_quote_value(self, event, bookmaker, result):
        try:
            quote = event.quotes.get(bookmaker=bookmaker, result_quotes__result=result)
        except Quotes.DoesNotExist:
            return 0
        except Quotes.MultipleObjectsReturned:
            return 0
        quote_value = quote.result_quotes.get(result=result).quote_value
        return quote_value

    def get_max_result_quote_value(self, event, result, bookmakers):
        max_value = 0
        max_bookmaker = None
        for b in bookmakers:
            value = self.get_result_quote_value(event=event, bookmaker=b, result=result)
            if value > max_value:
                max_value = value
                max_bookmaker = b
        return max_value, max_bookmaker

    """
        Handicaps
    """
    def get_handicap_quotes_value(self, event, bookmaker, handicap):
        try:
            quote = event.quotes.get(bookmaker=bookmaker, handicap_quotes__handicap=handicap)
        except Quotes.DoesNotExist:
            return 0
        except Quotes.MultipleObjectsReturned:
            return 0
        quote_value = quote.handicap_quotes.get(handicap=handicap).quote_value
        return quote_value

    def get_max_handicap_quote_value(self, event, handicap, bookmakers):
        max_value = 0
        max_bookmaker = None
        for b in bookmakers:
            value = self.get_handicap_quotes_value(event=event, bookmaker=b, handicap=handicap)
            if value > max_value:
                max_value = value
                max_bookmaker = b
        return max_value, max_bookmaker

    """
        Totals
    """
    def get_total_quotes_value(self, event, bookmaker, total):
        try:
            quote = event.quotes.get(bookmaker=bookmaker, total_quotes__total=total)
        except Quotes.DoesNotExist:
            return 0
        except Quotes.MultipleObjectsReturned:
            return 0
        quote_value = quote.total_quotes.get(total=total).quote_value
        return quote_value

    def get_max_total_quotes_value(self, event, total, bookmakers):
        max_value = 0
        max_bookmaker = None
        for b in bookmakers:
            value = self.get_total_quotes_value(event=event, bookmaker=b, total=total)
            if value > max_value:
                max_value = value
                max_bookmaker = b
        return max_value, max_bookmaker

    def check_vilka_handicaps(self, event):
        bookmakers = list()
        for i in Bookmaker.objects.all():
            bookmakers.append(i)
        vilki = list()
        handicaps = Handicap.objects.all()
        for handicap in handicaps:
            if handicap.quote_name > 0:
                try:
                    reverse = Handicap.objects.get(period_number=handicap.period_number,
                                                   team_number=1 if handicap.team_number == 2 else 2,
                                                   quote_name=(handicap.quote_name*(-1)))
                except Handicap.DoesNotExist:
                    continue
                vilki.append([handicap, reverse])

        for vilka in vilki:
            vilka_a, vilka_b = vilka
            a = self.get_max_handicap_quote_value(event=event, handicap=vilka_a, bookmakers=bookmakers)
            b = self.get_max_handicap_quote_value(event=event, handicap=vilka_b, bookmakers=bookmakers)

            try:
                my_sum = 1/a[0] + 1/b[0]
            except ZeroDivisionError:
                continue
            if my_sum < 1:
                print("{} - {}. Sum: {}. Bookmaker names {} - {}".format(
                    vilka_a, vilka_b, my_sum, a[1], b[1]))

    def check_vilka_totals(self, event):
        bookmakers = list()
        for i in Bookmaker.objects.all():
            bookmakers.append(i)
        vilki = list()
        totals = Total.objects.all()
        for total in totals:
            if total.quote_name > 0:
                try:
                    reverse = Total.objects.get(period_number=total.period_number,
                                                team_number=total.team_number,
                                                quote_name=total.quote_name,
                                                under_or_over=-1 if total.under_or_over == 1 else 1,
                                                )
                except Total.DoesNotExist:
                    continue
                vilki.append([total, reverse])

        for vilka in vilki:
            vilka_a, vilka_b = vilka
            a = self.get_max_total_quotes_value(event=event, total=vilka_a, bookmakers=bookmakers)
            b = self.get_max_total_quotes_value(event=event, total=vilka_b, bookmakers=bookmakers)

            try:
                my_sum = 1/a[0] + 1/b[0]
            except ZeroDivisionError:
                continue
            if my_sum < 1:
                print("{} - {}. Sum: {}. Bookmaker names {} - {}".format(
                    vilka_a, vilka_b, my_sum, a[1], b[1]))

    def check_vilka(self, event):
        bookmakers = list()
        for i in Bookmaker.objects.all():
            bookmakers.append(i)
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

        vilki = [
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

        for vilka in vilki:
            shoulder1, shoulder2, shoulder3 = vilka
            max_value1, max_bookmaker1 = self.get_max_result_quote_value(event=event,
                                                                         result=shoulder1,
                                                                         bookmakers=bookmakers)
            max_value2, max_bookmaker2 = self.get_max_result_quote_value(event=event,
                                                                         result=shoulder2,
                                                                         bookmakers=bookmakers)
            try:
                sum_vilki = 1 / max_value1 + 1 / max_value2
            except ZeroDivisionError:
                continue

            if shoulder3 is not None:
                max_value3, max_bookmaker3 = self.get_max_result_quote_value(event=event,
                                                                             result=shoulder3,
                                                                             bookmakers=bookmakers)
                sum_vilki = 1 / max_value1 + 1 / max_value2 + 1 / max_value3

            if sum_vilki < 1 and shoulder3 is None:
                print(sum_vilki,
                    vilka, max_value1, max_bookmaker1, max_value2, max_bookmaker2, event.home_team, event.away_team)
            elif sum_vilki < 1:
                print(max_value1, max_bookmaker1, max_value2, max_bookmaker2, max_value3, max_bookmaker3)

    def check_vilka_by_league(self, league):
        now = datetime.now(tz=timezone.utc)
        future = now + timedelta(days=28)
        events = Event.objects.filter(start_time__gte=now,
                                      start_time__lte=future,
                                      league=league)
        for event in events:
            self.check_vilka(event=event)

    def check_vilka_handicap_by_league(self, league):
        now = datetime.now(tz=timezone.utc)
        future = now + timedelta(days=28)
        events = Event.objects.filter(start_time__gte=now,
                                      start_time__lte=future,
                                      league=league)
        for event in events:
            self.check_vilka_handicaps(event=event)

    def check_vilka_total_by_league(self, league):
        now = datetime.now(tz=timezone.utc)
        future = now + timedelta(days=28)
        events = Event.objects.filter(start_time__gte=now,
                                      start_time__lte=future,
                                      league=league)
        for event in events:
            self.check_vilka_totals(event=event)

    def get_results(self, results):
        answer = list()
        for result in results:
            if result is None:
                continue
            period_number, quote_name, quote_value = result
            r, created = Result.objects.get_or_create(period_number=period_number, quote_name=quote_name)
            rq, created = ResultQuote.objects.get_or_create(result=r, quote_value=quote_value)
            answer.append(rq)
        return answer

    def get_handicaps(self, handicaps):
        answer = list()
        for handicap in handicaps:
            if handicap is None:
                continue
            period_number, team_number, quote_name, quote_value = handicap
            h, created = Handicap.objects.get_or_create(period_number=period_number, team_number=team_number,
                                                        quote_name=quote_name)
            hq, created = HandicapQuote.objects.get_or_create(handicap=h, quote_value=quote_value)
            answer.append(hq)
        return answer

    def get_totals(self, totals):
        answer = list()
        for total in totals:
            if total is None:
                continue
            period_number, team_number, under_or_over, quote_name, quote_value = total
            t, created = Total.objects.get_or_create(period_number=period_number, team_number=team_number,
                                                     under_or_over=under_or_over, quote_name=quote_name)
            tq, created = TotalQuote.objects.get_or_create(total=t, quote_value=quote_value)
            answer.append(tq)
        return answer

    def get_quote(self, event_id, bookmaker_id, result_id):
        try:
            a = Event.objects.get(id=event_id)
            b = a.quotes.get(bookmaker_id=bookmaker_id)
            c = b.result_quotes.get(result_id=result_id)
            d = c.quote_value
            return d
        except Quotes.DoesNotExist:
            return None
        except ResultQuote.DoesNotExist:
            return None
