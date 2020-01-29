from .baltbet import Baltbet


class BaltbetTennis(Baltbet):
    handicap_period_1 = "Фора по сетам (1-й сет)"
    handicap_period_2 = "Фора по сетам (2-й сет)"
    handicap_period_3 = "Фора по сетам (3-й сет)"
    total_period_1 = "Тотал (1-й сет)"
    total_period_2 = "Тотал (2-й сет)"
    total_period_3 = "Тотал (3-й сет)"
    result_period_1 = "Победа в сете (1-й сет)"
    result_period_2 = "Победа в сете (2-й сет)"
    result_period_3 = "Победа в сете (3-й сет)"

    def __init__(self):
        super().__init__()

    def get_main_quotes(self, page):
        main_quotes = page.select(selector=self.main_quotes_selector)
        result = list()
        result.append([0, 0, float(main_quotes[0].text.strip())])
        result.append([0, 2, float(main_quotes[1].text.strip())])
        return result
