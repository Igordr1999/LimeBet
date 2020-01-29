from .bet import Bet


class Fonbet(Bet):
    base_url = "https://fonbet.ru"
    matches_teams_selector = ".ev-scoreboard__team-name--22w0L"
    matches_links_selector = "a.table__match-title-text"
    main_quotes_selector = ".ev-factors__row--3LmVL._type_body--HtZvu .ev-factors__col--uCmqD._type_factor--oqccY"

    handicap_period_all = "Форы"
    total_periods_all = "Тоталы"
    total_periods_all_by_team = "Инд. тоталы-{}"

    under_text = "М"

    add_slash_url = True
    is_sleeps = True

    def __init__(self):
        super().__init__()

    def get_quartets(self, page, teams):
        data = list()
        tables = page.select(selector=".table__details")

        data = list()
        for table in tables:
            name = table.select_one(".table__details-title")
            if name.text not in self.handicap_period_number and \
                    (name.text not in self.total_period_number):
                continue
            heads = table.select(".table__grid-col._type_head")
            rows = table.select(".table__grid-row")
            for row in rows:
                q = row.select("td")
                if len(q) == 3:
                    data.append([name.text, heads[1].text, q[0].text, q[1].text, teams])
                    data.append([name.text, heads[2].text, q[0].text, q[2].text, teams])
                elif len(q) == 4:
                    print(heads[0], heads[1], heads[2], heads[3])
                    data.append([name.text, heads[1].text, q[0].text, q[1].text, teams])
                    data.append([name.text, heads[3].text, q[2].text, q[3].text, teams])

        return data

    def get_handicap(self, name, sub_name, q_name, q_value, team1, team2):
        period_number = self.handicap_period_number[name]
        team_number = 1 if "1" == sub_name else 2
        q_name = float(q_name)
        q_value = float(q_value)
        return [period_number, team_number, q_name, q_value]

    def get_total(self, name, sub_name, q_name, q_value, team1, team2):
        q_name = float(q_name)
        q_value = float(q_value)

        team_number = self.total_team_number[name]
        under_over_number = -1 if sub_name == self.under_text else 1
        period_number = self.total_period_number[name]
        return [period_number, team_number, under_over_number, q_name, q_value]
