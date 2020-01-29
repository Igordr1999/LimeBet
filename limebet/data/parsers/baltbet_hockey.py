from .baltbet import Baltbet


class BaltbetHockey(Baltbet):
    handicap_period_1 = "Фора периода (1-й период)"
    handicap_period_2 = "Фора периода (2-й период)"
    handicap_period_3 = "Фора периода (3-й период)"
    total_periods_all_by_team = "Индивидуальный тотал {}-й команды"
    total_period_1 = "Тотал периода (1-й период)"
    total_period_2 = "Тотал периода (2-й период)"
    total_period_3 = "Тотал периода (3-й период)"
    total_period_1_by_team = "Индивидуальный тотал {}-й команды в периоде (1-й период)"
    total_period_2_by_team = "Индивидуальный тотал {}-й команды в периоде (2-й период)"
    total_period_3_by_team = "Индивидуальный тотал {}-й команды в периоде (3-й период)"
    result_period_1 = "Результат периода (1-й период)"
    result_period_2 = "Результат периода (2-й период)"
    result_period_3 = "Результат периода (3-й период)"

    def __init__(self):
        super().__init__()

