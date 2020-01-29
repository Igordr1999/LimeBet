from .bet import Bet


class Parimatch(Bet):
    base_url = "https://www.parimatch.ru"
    matches_teams_selector = ".event-view-info__competitor-name"
    main_quotes_selector = ".event-outcome__value"
    matches_links_selector = ".live-block-competitors"

    handicap_period_all = "Фора"
    handicap_period_1 = "Фора. 1-й тайм"
    handicap_period_2 = "Фора. 2-й тайм"
    total_periods_all = "Тотал"
    total_periods_all_by_team = "Индивидуальный тотал {}"
    total_period_1 = "Тотал. 1-й тайм"
    total_period_2 = "Тотал. 2-й тайм"
    result_period_1 = "Результат. 1-й тайм"
    result_period_1_copy = "Двойной исход. 1-й тайм"
    result_period_2 = "Результат. 2-й тайм"
    result_period_2_copy = "Двойной исход. 2-й тайм"
    result_team = "{}"
    result_team_X = "Ничья"
    result_team_or_X = "{} не проиграет"
    result_team_or_team = "Не будет ничьей"

    is_sleeps = True
    dynamic_team_name = True
    is_extra_js_command = True
    extra_js_command = 'var markets = document.getElementsByClassName("event-market"); for (var i=0;i<markets.length;i++){ if(markets[i].childElementCount < 2){ markets[i].firstElementChild.click();}}'

    under_text = "Меньше"

    def __init__(self):
        super().__init__()

    def get_quartets(self, page, teams):
        data = list()
        counter = 0
        tables = page.select(selector=".event-market")

        for table in tables:
            name = table.select_one(".event-market__title")
            rows = table.select(".event-outcome-group__wrapper")
            for row in rows:
                quotes = row.select(".event-outcome")
                for quote in quotes:
                    q_name = quote.select_one(".event-outcome__name")
                    q_value = quote.select_one(".event-outcome__value")
                    try:
                        data.append([name.text.strip(), "", q_name.text.strip(), q_value.text.strip(), teams])
                    except AttributeError:
                        try:
                            q_name = row.select_one(".event-outcome-group-head")
                            q_values = row.select(".event-outcome__value")
                            sub_name = "Больше" if counter % 2 == 0 else "Меньше"
                            data.append([name.text.strip(), sub_name, q_name.text.strip(), q_values[0].text.strip(), teams])
                            counter += 1
                            sub_name = "Больше" if counter % 2 == 0 else "Меньше"
                            data.append([name.text.strip(), sub_name, q_name.text.strip(), q_values[1].text.strip(), teams])
                            counter += 1
                        except AttributeError:
                            continue

        return data

    def get_results(self, name, sub_name, q_name, q_value, team1, team2):
        q_value = float(q_value)
        period_number = self.result_period_number[name]
        team_number = self.result_team_number[q_name]
        print(name, sub_name, q_name, period_number, team_number)
        return [period_number, team_number, q_value]

    def get_handicap(self, name, sub_name, q_name, q_value, team1, team2):
        period_number = self.handicap_period_number[name]
        team_name, q_name = q_name.split("(")
        q_name = q_name[:-1]
        team_number = 1 if team1 == team_name else 2
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
