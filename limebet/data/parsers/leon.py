from .bet import Bet


class Leon(Bet):
    base_url = "https://www.leon.ru"
    matches_teams_selector = ".st-event-name"
    main_quotes_selector = ".price.stn-val"
    matches_links_selector = ".st-name.st-link > a"

    handicap_period_all = "Фора"
    handicap_period_1 = "1-й тайм: Фора"
    total_periods_all = "Тотал"
    total_periods_all_by_team_copy_1 = "Тотал хозяев"
    total_periods_all_by_team_copy_2 = "Тотал гостей"
    total_period_1_by_team = "1-й тайм: Тотал {}"
    result_period_1 = "1-й тайм: 1X2"
    result_period_2 = "2-й тайм: 1X2"
    result_period_all_copy = "Двойной исход"
    result_period_1_copy = "1-й тайм: Двойной исход"
    result_period_2_copy = "2-й тайм: Двойной исход"

    result_team = "{}"
    result_team_X = "X"
    result_team_or_X = "{}X"
    result_team_or_X_copy = "X{}"
    result_team_or_team = "{}{}"

    under_text = "Меньше"

    team1 = "хозяев"
    team2 = "гостей"

    dynamic_team_name = True

    def __init__(self):
        super().__init__()

    def get_main_quotes(self, page):
        main_quotes = page.select(selector=self.main_quotes_selector)
        result = list()
        result.append([0, 0, float(main_quotes[0].text.strip())])
        result.append([0, 1, float(main_quotes[1].text.strip())])
        result.append([0, 2, float(main_quotes[2].text.strip())])
        return result

    def get_quartets(self, page, teams):
        data = list()
        tables = page.select(selector=".bet-market-family")

        for table in tables:
            name = table.select_one(".headline")
            try:
                name = name.text.strip()
            except AttributeError:
                name = "NO"
            quotes = table.select("li")
            for quote in quotes:
                bb = quote.select("span")
                data.append([name, "", bb[0].text.strip(), bb[1].text.strip(), teams])
        return data

    def get_results(self, name, sub_name, q_name, q_value, team1, team2):
        period_number = self.result_period_number[name]
        q_name_dict = {
            "1": team1,
            "X": "X",
            "2": team2,
            "1X": team1 + "X",  # eng 1x
            "1Х": team1 + "X",  # rus 1x
            "X2": "X" + team2,  # eng x2
            "Х2": "X" + team2,  # rus x2
            "2X": "X" + team2,  # eng x2
            "2Х": "X" + team2,  # rus x2
            "12": team1+team2,
        }
        q_name = q_name_dict[q_name]
        print(self.result_team_number)
        team_number = self.result_team_number[q_name]
        q_value = float(q_value)
        return [period_number, team_number, q_value]

    def get_handicap(self, name, sub_name, q_name, q_value, team1, team2):
        period_number = self.handicap_period_number[name]
        team_number, q_name = q_name.split()
        team_number = int(team_number)
        q_name = q_name[1:-1]
        q_name = float(q_name)
        q_value = float(q_value)
        return [period_number, team_number, q_name, q_value]

    def get_total(self, name, sub_name, q_name, q_value, team1, team2):
        word, q_name = q_name.split()
        q_name = q_name[1:-1]
        q_name = float(q_name)
        q_value = float(q_value)

        team_number = self.total_team_number[name]
        under_over_number = -1 if word == self.under_text else 1
        period_number = self.total_period_number[name]
        return [period_number, team_number, under_over_number, q_name, q_value]
