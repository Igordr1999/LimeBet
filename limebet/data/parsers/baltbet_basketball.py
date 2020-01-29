from .baltbet import Baltbet


class BaltbetBasketball(Baltbet):
    handicap_period_1 = "Фора По четвертям (1-я четверть)"
    handicap_period_2 = "Фора По четвертям (2-я четверть)"
    handicap_period_3 = "Фора По четвертям (3-я четверть)"
    handicap_period_4 = "Фора По четвертям (4-я четверть)"
    total_periods_all_by_team = "Инд. тотал {} команды"
    total_period_1 = "Тотал По четвертям (1-я четверть)"
    total_period_2 = "Тотал По четвертям (2-я четверть)"
    total_period_3 = "Тотал По четвертям (3-я четверть)"
    total_period_4 = "Тотал По четвертям (4-я четверть)"
    result_period_1 = "Результат По четвертям (1-я четверть)"
    result_period_2 = "Результат По четвертям (2-я четверть)"
    result_period_3 = "Результат По четвертям (3-я четверть)"
    result_period_4 = "Результат По четвертям (4-я четверть)"

    def __init__(self):
        super().__init__()

    def get_main_quotes(self, page):
        main_quotes = page.select(selector=self.main_quotes_selector)
        result = list()
        result.append([0, 0, float(main_quotes[0].text.strip())])
        result.append([0, 2, float(main_quotes[1].text.strip())])
        return result
