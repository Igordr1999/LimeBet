from .xbet import Xbet


class XbetBasketball(Xbet):
    handicap_period_all = "Фора. с ОТ"
    total_periods_all = "Тотал. с ОТ"
    total_periods_all_by_team = "Индивидуальный тотал {}-го. с ОТ"

    def __init__(self):
        super().__init__()

    def get_main_quotes(self, page):
        main_quotes = page.select(selector=self.main_quotes_selector)
        result = list()
        result.append([0, 0, float(main_quotes[0].text.strip())])
        result.append([0, 2, float(main_quotes[1].text.strip())])
        return result
