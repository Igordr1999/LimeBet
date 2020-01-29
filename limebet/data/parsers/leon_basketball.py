from .leon import Leon


class LeonBasketball(Leon):
    total_periods_all_by_team_copy_1 = "Тотал хозяев"
    total_periods_all_by_team_copy_2 = "Тотал гостей"
    result_period_1 = "1-я четверть: 1X2"
    result_period_2 = "2-я четверть: 1X2"
    result_period_3 = "3-я четверть: 1X2"
    result_period_4 = "4-я четверть: 1X2"

    def __init__(self):
        super().__init__()

    def get_main_quotes(self, page):
        main_quotes = page.select(selector=self.main_quotes_selector)
        result = list()
        result.append([0, 0, float(main_quotes[2].text.strip())])
        result.append([0, 1, float(main_quotes[3].text.strip())])
        result.append([0, 2, float(main_quotes[4].text.strip())])
        return result
