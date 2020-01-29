from .mbet import Mbet


class MbetHockey(Mbet):
    handicap_period_1 = "Победа с учетом форы, 1-й период"
    handicap_period_2 = "Победа с учетом форы, 2-й период"
    handicap_period_3 = "Победа с учетом форы, 3-й период"

    total_period_1 = "Тотал голов, 1-й период"
    total_period_2 = "Тотал голов, 2-й период"
    total_period_3 = "Тотал голов, 3-й период"

    result_period_1 = "Результат, 1-й период"
    result_period_2 = "Результат, 2-й период"
    result_period_3 = "Результат, 3-й период"

    def __init__(self):
        super().__init__()
