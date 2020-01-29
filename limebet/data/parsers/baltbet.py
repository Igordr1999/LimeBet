from .bet import Bet


class Baltbet(Bet):
    base_url = "https://www.baltbet.ru"
    matches_teams_selector = ".event-header-prematch__teams span"
    main_quotes_selector = ".event-markets__coef-value"
    matches_links_selector = ".events-table__title-wrapper"

    handicap_period_all = "Фора"
    handicap_period_all_copy = "Доп. фора"
    handicap_period_1 = "По таймам Фора (1-й тайм)"
    handicap_period_2 = "По таймам Фора (2-й тайм)"
    total_periods_all = "Тотал"
    total_periods_all_copy = "Дополнительный тотал"
    total_periods_all_by_team = "Индивидуальный тотал {}К (Матч)"
    total_period_1 = "По таймам Тотал (1-й тайм)"
    total_period_2 = "По таймам Тотал (2-й тайм)"
    total_period_1_by_team = "Индивидуальный тотал {}К (1-й тайм)"
    total_period_2_by_team = "Индивидуальный тотал {}К (2-й тайм)"
    result_period_1 = "По таймам исход (1-й тайм)"
    result_period_2 = "По таймам исход (2-й тайм)"

    under_text = "Мен"

    team1 = "1"
    team2 = "2"

    def __init__(self):
        super().__init__()

    def get_quartets(self, page, teams):
        data = list()
        tables = page.select(selector=".event-markets__item")

        for table in tables:
            name = table.select_one(".event-markets__title")
            quotes = table.select(".event-markets__coef")
            for quote in quotes:
                q_name = quote.select_one(".event-markets__coef-title")
                q_value = quote.select_one(".event-markets__coef-value")
                data.append([name.text.strip(), "", q_name.text.strip(), q_value.text.strip(), teams])
        return data

    def get_results(self, name, sub_name, q_name, q_value, team1, team2):
        q_value = float(q_value)
        period_number = self.result_period_number[name]
        q_name = q_name.split(") ")[1]
        q_name_dict = {
            "Поб. 1": 0,
            "Поб. 2": 2,
            "Ничья": 1,
            "1": 0,
            "X": 1,
            "2": 2,
        }
        team_number = q_name_dict[q_name]
        print(q_name)
        return [period_number, team_number, q_value]

    def get_handicap(self, name, sub_name, q_name, q_value, team1, team2):
        period_number = self.handicap_period_number[name]
        try:
            team_dry_text, q_name, trash = q_name.split(" ")
        except ValueError:
            team_dry_text, q_name = q_name.split(" ")
        q_name = q_name[1:-1]
        q_name = q_name.replace(",", ".")
        team_number = 1 if "Ф1к" == team_dry_text else 2
        q_name = float(q_name)
        q_value = float(q_value)
        return [period_number, team_number, q_name, q_value]

    def get_total(self, name, sub_name, q_name, q_value, team1, team2):
        try:
            team_dry_text, q_name, trash = q_name.split(" ")
        except ValueError:
            try:
                team_dry_text, q_name = q_name.split(" ")
            except ValueError:
                team_dry_text, trash, q_name, trash_2 = q_name.split(" ")
        q_name = q_name[1:-1]
        q_name = q_name.replace(",", ".")

        q_name = float(q_name)
        q_value = float(q_value)

        team_number = self.total_team_number[name]
        try:
            under_over_number = -1 if trash == self.under_text else 1
        except UnboundLocalError:
            under_over_number = -1 if team_dry_text == self.under_text else 1
        period_number = self.total_period_number[name]
        return [period_number, team_number, under_over_number, q_name, q_value]
