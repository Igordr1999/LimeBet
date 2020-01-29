from .parimatch import Parimatch


class ParimatchBasketball(Parimatch):
    handicap_period_1 = "Фора. 1-я четверть"
    handicap_period_2 = "Фора. 2-я четверть"
    handicap_period_3 = "Фора. 3-я четверть"
    handicap_period_4 = "Фора. 4-я четверть"
    total_period_1 = "Тотал. 1-я четверть"
    total_period_2 = "Тотал. 2-я четверть"
    total_period_3 = "Тотал. 3-я четверть"
    total_period_4 = "Тотал. 4-я четверть"
    result_period_1 = "Результат. 1-я четверть"
    result_period_2 = "Результат. 2-я четверть"
    result_period_3 = "Результат. 3-я четверть"
    result_period_4 = "Результат. 4-я четверть"

    def __init__(self):
        super().__init__()

    def get_main_quotes(self, page):
        main_quotes = page.select(selector=self.main_quotes_selector)
        result = list()
        result.append([0, 0, float(main_quotes[0].text.strip())])
        result.append([0, 1, float(main_quotes[1].text.strip())])
        result.append([0, 2, float(main_quotes[2].text.strip())])
        return result

