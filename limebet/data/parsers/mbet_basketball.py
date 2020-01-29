from .mbet import Mbet


class MbetBasketball(Mbet):
    handicap_period_all = "Победа с учетом форы"
    handicap_period_1 = "Победа с учетом форы, 1-я четверть"
    handicap_period_2 = "Победа с учетом форы, 2-я четверть"
    handicap_period_3 = "Победа с учетом форы, 3-я четверть"
    handicap_period_4 = "Победа с учетом форы, 4-я четверть"

    total_periods_all = "Тотал очков"
    total_periods_all_by_team = "Тотал очков ({})"

    total_period_1_by_team = "Тотал очков ({}), 1-я четверть"
    total_period_2_by_team = "Тотал очков ({}), 2-я четверть"
    total_period_3_by_team = "Тотал очков ({}), 3-я четверть"
    total_period_4_by_team = "Тотал очков ({}), 4-я четверть"

    total_period_1 = "Тотал очков, 1-я четверть"
    total_period_2 = "Тотал очков, 2-я четверть"
    total_period_3 = "Тотал очков, 3-я четверть"
    total_period_4 = "Тотал очков, 4-я четверть"

    result_period_1 = "Результат, 1-я четверть"
    result_period_2 = "Результат, 2-я четверть"
    result_period_3 = "Результат, 3-я четверть"
    result_period_4 = "Результат, 4-я четверть"

    def __init__(self):
        super().__init__()

    def get_main_quotes(self, page):
        result = list()
        return result
