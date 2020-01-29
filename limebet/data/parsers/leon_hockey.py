from .leon import Leon


class LeonHockey(Leon):
    total_periods_all = "Тотал"
    total_periods_all_by_team_copy_1 = "Тотал хозяев"
    total_periods_all_by_team_copy_2 = "Тотал гостей"
    total_period_1_by_team = "1-й тайм: Тотал {}"
    total_period_1 = "1-й период: Тотал"
    total_period_2 = "2-й период: Тотал"
    total_period_3 = "3-й период: Тотал"
    result_period_1 = "1-й период: 1X2"
    result_period_2 = "2-й период: 1X2"
    result_period_3 = "3-й период: 1X2"
    result_period_all_copy = "Двойной исход"
    result_period_1_copy = "1-й период: Двойной исход"
    result_period_2_copy = "2-й период: Двойной исход"
    result_period_3_copy = "3-й период: Двойной исход"

    def __init__(self):
        super().__init__()

    def get_main_quotes(self, page):
        main_quotes = page.select(selector=self.main_quotes_selector)
        result = list()
        result.append([0, 0, float(main_quotes[0].text.strip())])
        result.append([0, 1, float(main_quotes[1].text.strip())])
        result.append([0, 2, float(main_quotes[2].text.strip())])
        return result
