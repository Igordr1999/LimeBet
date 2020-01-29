from .winline import Winline


class WinlineHockey(Winline):
    handicap_period_1 = "1 период фора"
    handicap_period_2 = "2 период фора"
    handicap_period_3 = "3 период фора"
    total_periods_all = "Тотал (осн. время)"
    total_periods_all_by_team = "Тотал (осн. время) {}"
    total_period_1 = "1 период тотал"
    total_period_2 = "2 период тотал"
    total_period_3 = "3 период тотал"
    result_period_all = "Исход 1X2"
    result_period_all_copy = "Двойной шанс"

    def __init__(self):
        super().__init__()
