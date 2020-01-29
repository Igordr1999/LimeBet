from .mbet import Mbet


class MbetTennis(Mbet):
    handicap_period_all = "Победа с учетом форы по геймам"
    handicap_period_1 = "Победа с учетом форы по геймам, 1-й сет"
    handicap_period_2 = "Победа с учетом форы по геймам, 2-й сет"
    handicap_period_3 = "Победа с учетом форы по геймам, 3-й сет"

    total_periods_all = "Тотал геймов"
    total_periods_all_by_team = "Тотал выигранных геймов ({})"

    total_period_1_by_team = "Тотал выигранных геймов ({}), 1-й сет"
    total_period_2_by_team = "Тотал выигранных геймов ({}), 2-й сет"
    total_period_3_by_team = "Тотал выигранных геймов ({}), 3-й сет"

    total_period_1 = "Тотал геймов, 1-й сет"
    total_period_2 = "Тотал геймов, 2-й сет"
    total_period_3 = "Тотал геймов, 3-й сет"

    result_period_1 = "Результат, 1-й сет"
    result_period_2 = "Результат, 2-й сет"
    result_period_3 = "Результат, 3-й сет"

    def __init__(self):
        super().__init__()

    def get_main_quotes(self, page):
        main_quotes = page.select(selector=self.main_quotes_selector)
        result = list()
        result.append([0, 0, float(main_quotes[0].text.strip())])
        result.append([0, 2, float(main_quotes[1].text.strip())])
        return result
