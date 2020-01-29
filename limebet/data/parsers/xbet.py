from .bet import Bet


class Xbet(Bet):
    base_url = "https://1xstavka.ru"
    matches_teams_selector = ".team > a"
    main_quotes_selector = ".koeff"
    matches_links_selector = ".c-events__item_game > a"

    handicap_period_all = "Фора"
    total_periods_all = "Тотал"
    total_periods_all_by_team = "Индивидуальный тотал {}-го"
    under_text = "М"

    team1 = "1"
    team2 = "2"

    add_slash_url = True

    def __init__(self):
        super().__init__()

    def get_handicap(self, name, sub_name, q_name, q_value, team1, team2):
        period_number = 0
        team_number, handicap_value = q_name.split()
        team_number = int(team_number)
        q_name = float(handicap_value)
        q_value = float(q_value)
        return [period_number, team_number, q_name, q_value]

    def get_total(self, name, sub_name, q_name, q_value, team1, team2):
        total_value, under_over_text_value = q_name.split()
        under_over_value = -1 if under_over_text_value == self.under_text else 1
        team_number = self.total_team_number[name]
        print(name, team_number, self.total_team_number[name])
        period_number = 0
        under_over_number = under_over_value
        q_name = float(total_value)
        q_value = float(q_value)
        return [period_number, team_number, under_over_number, q_name, q_value]

    def get_quartets(self, page, teams):
        data = list()
        tables = page.select(selector=".bet_group_col.cols1 > div > .bet_group")

        for table in tables:
            name = table.select_one(".bet-title")
            quotes = table.select(".bets")
            for quote in quotes:
                cells = quote.select("div")
                print(cells)
                for c in cells:
                    bb = c.select("span")
                    try:
                        data.append([name.text.strip(), "", bb[0].text.strip(), bb[1].text.strip(), teams])
                    except IndexError:
                        break
        print("Data", data)
        return data

