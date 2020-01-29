from .winline import Winline


class WinlineTennis(Winline):
    handicap_period_1 = "1 сет фора"
    handicap_period_2 = "2 сет фора"
    handicap_period_3 = "3 сет фора"
    total_periods_all = "Тотал (матч)"
    total_periods_all_by_team = "Тотал (матч) {}."
    total_period_1 = "1 сет тотал"
    total_period_2 = "2 сет тотал"
    total_period_3 = "3 сет тотал"
    result_period_all = "Исход 12"

    def __init__(self):
        super().__init__()
