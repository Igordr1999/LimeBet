from .parimatch import Parimatch


class ParimatchTennis(Parimatch):
    handicap_period_1 = "Фора. 1-й сет"
    handicap_period_2 = "Фора. 2-й сет"
    handicap_period_3 = "Фора. 3-й сет"
    total_period_1 = "Тотал. 1-й сет"
    total_period_2 = "Тотал. 2-й сет"
    total_period_3 = "Тотал. 3-й сет"
    total_period_1_by_team = "Индивидуальный тотал {}. 1-й сет"
    total_period_2_by_team = "Индивидуальный тотал {}. 2-й сет"
    total_period_3_by_team = "Индивидуальный тотал {}. 3-й сет"
    result_period_1 = "Победитель. 1-й сет"
    result_period_2 = "Победитель. 2-й сет"
    result_period_3 = "Победитель. 3-й сет"

    def __init__(self):
        super().__init__()

    def get_main_quotes(self, page):
        main_quotes = page.select(selector=self.main_quotes_selector)
        result = list()
        result.append([0, 0, float(main_quotes[0].text.strip())])
        result.append([0, 2, float(main_quotes[1].text.strip())])
        return result

