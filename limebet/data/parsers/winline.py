from .bet import Bet


class Winline(Bet):
    base_url = "https://winline.ru"
    matches_teams_selector = ".football-center__left, .football-center__right, .sport-center__gamer"
    matches_links_selector = ".statistic__wrapper > a"

    handicap_period_all = "Фора (осн. время)"
    handicap_period_1 = "1 тайм фора"
    handicap_period_2 = "2 тайм фора"
    total_periods_all = "Тотал (осн. время)"
    total_periods_all_by_team = "Тотал (осн. время) {}"
    total_period_1 = "1 тайм тотал"
    total_period_2 = "2 тайм тотал"
    total_period_1_by_team = "1 тайм тотал {}"
    total_period_2_by_team = "2 тайм тотал {}"
    result_period_all = "Исход 1X2"
    result_period_all_copy = "Двойной шанс"

    under_text = "Меньше"

    is_sleeps = True
    dynamic_team_name = True

    result_team = "{}"
    result_team_X = "X"
    result_team_or_X = "{}X"
    result_team_or_X_copy = "X{}"
    result_team_or_team = "{}{}"

    def __init__(self):
        super().__init__()

    def get_main_quotes(self, page):
        result = list()
        return result

    def get_results(self, name, sub_name, q_name, q_value, team1, team2):
        try:
            q_value = float(q_value)
        except ValueError:
            return None
        period_number_dict = {
            "осн. время": 0,
            "матч": 0,
            "1 тайм": 1,
            "2 тайм": 2,
            "1 период": 1,
            "2 период": 2,
            "3 период": 3,
            "1 четверть": 1,
            "2 четверть": 2,
            "3 четверть": 3,
            "4 четверть": 4,
            "1 сет": 1,
            "2 сет": 2,
            "3 сет": 3,
        }
        if sub_name in period_number_dict:
            period_number = period_number_dict[sub_name]
        else:
            return None
        q_name_dict = {
            "П1": team1,
            "X": "X",
            "П2": team2,
            "1X": team1 + "X",
            "X2": "X" + team2,
            "12": team1+team2,
        }
        q_name = q_name_dict[q_name]
        team_number = self.result_team_number[q_name]
        return [period_number, team_number, q_value]

    def get_quartets(self, page, teams):
        data = list()
        tables = page.select(selector=".result-table.ng-star-inserted")

        for table in tables:
            name = table.select_one(".result-table__header")
            rows = table.select(".result-table__row.ng-star-inserted")
            for row in rows:
                items = row.select(".result-table__item.ng-star-inserted")
                counter = 0
                for item in items:
                    if counter == 0:
                        sub_name = item.select_one(".text")
                    else:
                        bb = item.select("span")
                        try:
                            data.append([name.text.strip(), sub_name.text.strip(),
                                         bb[0].text.strip(), bb[1].text.strip(), teams])
                            # print([name.text.strip(), sub_name.text.strip(), bb[0].text.strip(), bb[1].text.strip(), teams])
                        except IndexError:
                            break
                    counter += 1
        return data

    def get_handicap(self, name, sub_name, q_name, q_value, team1, team2):
        period_number = self.handicap_period_number[name]
        team_number = 1 if team1 == sub_name else 2
        q_name = q_name.replace("−", "-")
        q_name = float(q_name)
        q_value = float(q_value)
        if q_name % 0.5 == 0.0:
            return [period_number, team_number, q_name, q_value]

    def get_total(self, name, sub_name, q_name, q_value, team1, team2):
        symbol, q_name = q_name.split()
        q_name.replace("−", "-")
        try:
            q_name = float(q_name)
            q_value = float(q_value)
        except ValueError:
            return None

        team_number = self.total_team_number[name]
        under_over_number = -1 if sub_name == self.under_text else 1
        period_number = self.total_period_number[name]
        return [period_number, team_number, under_over_number, q_name, q_value]
