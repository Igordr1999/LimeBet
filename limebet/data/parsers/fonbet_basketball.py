from .fonbet import Fonbet


class FonbetBasketball(Fonbet):
    handicap_period_all = "Покупки форы"
    total_periods_all = "Покупки тотала"
    total_periods_all_by_team = "Индивидуальный тотал"

    def __init__(self):
        super().__init__()

    def get_main_quotes(self, page):
        main_quotes = page.select(selector=self.main_quotes_selector)
        result = list()
        result.append([0, 0, float(main_quotes[0].text.strip())])
        result.append([0, 2, float(main_quotes[2].text.strip())])
        return result
