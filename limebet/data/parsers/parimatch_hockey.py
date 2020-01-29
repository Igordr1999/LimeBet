from .parimatch import Parimatch


class ParimatchHockey(Parimatch):
    handicap_period_1 = "Фора. 1-й период"
    handicap_period_2 = "Фора. 2-й период"
    handicap_period_3 = "Фора. 3-й период"
    total_period_1 = "Тотал. 1-й период"
    total_period_2 = "Тотал. 2-й период"
    total_period_3 = "Тотал. 3-й период"
    total_period_1_by_team = "Индивидуальный тотал {}. 1-й период"
    total_period_2_by_team = "Индивидуальный тотал {}. 2-й период"
    total_period_3_by_team = "Индивидуальный тотал {}. 3-й период"
    result_period_1 = "Результат. 1-й период"
    result_period_1_copy = "Двойной исход. 1-й период"
    result_period_2 = "Результат. 2-й период"
    result_period_2_copy = "Двойной исход. 2-й период"
    result_period_3 = "Результат. 3-й период"
    result_period_3_copy = "Двойной исход. 3-й период"

    def __init__(self):
        super().__init__()
