from .winline import Winline


class BasketballTennis(Winline):
    handicap_period_all = "Фора (с ОТ)"
    handicap_period_1 = "1 четверть фора"
    handicap_period_2 = "2 четверть фора"
    handicap_period_3 = "3 четверть фора"
    handicap_period_4 = "4 четверть фора"
    total_periods_all = "Тотал (с ОТ)"
    total_periods_all_by_team = "Тотал (с ОТ) {}"
    total_period_1 = "1 четверть тотал"
    total_period_2 = "2 четверть тотал"
    total_period_3 = "3 четверть тотал"
    total_period_4 = "4 четверть тотал"
    result_period_all = "Исход 1X2"

    def __init__(self):
        super().__init__()
