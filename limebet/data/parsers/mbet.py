from .bet import Bet


class Mbet(Bet):
    base_url = "https://www.marathonbet.ru"
    matches_teams_selector = ".member-link > span"
    main_quotes_selector = ".height-column-with-price"

    matches_links_selector = ".member-link"
    all_quotes_tab_selector = ".markets-additional-root-block td"
    sections_selectors = ".block-market-table-wrapper"
    tables_selectors = ".market-inline-block-table-wrapper"
    table_name_selector = ".market-table-name .name-field"
    rows_names_selectors = ".td-border.table-layout-fixed th"
    quote_names_selectors = ".td-border.table-layout-fixed .coeff-handicap"
    quote_values_selectors = ".td-border.table-layout-fixed .coeff-price"

    dynamic_team_name = True

    def __init__(self):
        super().__init__()

    def get_results(self, name, sub_name, q_name, q_value, team1, team2):
        q_value = self.clean_q_value(q_value=q_value)
        period_number = self.result_period_number[name]
        team_number = self.result_team_number[q_name]
        return [period_number, team_number, q_value]

    def get_handicap(self, name, sub_name, q_name, q_value, team1, team2):
        period_number = self.handicap_period_number[name]
        team_number = 1 if team1 == sub_name else 2
        q_name = self.clean_q_name(q_name=q_name)
        q_value = self.clean_q_value(q_value=q_value)
        return [period_number, team_number, q_name, q_value]

    def get_total(self, name, sub_name, q_name, q_value, team1, team2):
        team_number = self.total_team_number[name]
        period_number = self.total_period_number[name]
        under_over_number = -1 if sub_name == self.under_text else 1
        q_name = self.clean_q_name(q_name=q_name)
        q_value = self.clean_q_value(q_value=q_value)
        return [period_number, team_number, under_over_number, q_name, q_value]

    def get_quartets(self, page, teams):
        all_data = list()
        sections = page.select(selector=self.sections_selectors)
        for section in sections:
            tables = section.select(self.tables_selectors)
            for table in tables:
                name = table.select_one(self.table_name_selector)
                all_data += self.get_all_data_by_table(table=table, name=name, teams=teams)
        return all_data

    def get_all_data_by_table(self, table, name, teams):
        all_data = list()
        rows_names = table.select(self.rows_names_selectors)
        quote_names = table.select(self.quote_names_selectors)
        quote_values = table.select(self.quote_values_selectors)

        rows_count = len(rows_names)
        my_counter = 0

        try:
            if name.text.strip() in self.result_period_number:
                q_names = table.select(".result-left")
                q_values = table.select(".result-right")
                for q_name, q_value in zip(q_names, q_values):
                    all_data.append([name.text.strip(), "",
                                     q_name.text.strip(), q_value.text.strip(), teams])
            else:

                if (not len(quote_names)) or (not len(quote_values)):
                    return []
                for q_name, q_value in zip(quote_names, quote_values):
                    try:
                        sub_name = rows_names[my_counter % rows_count]
                    except ZeroDivisionError:
                        continue
                    all_data.append([name.text.strip(), sub_name.text.strip(),
                                     q_name.text.strip(), q_value.text.strip(), teams])
                    print([name.text.strip(), sub_name.text.strip(), q_name.text.strip(), q_value.text.strip(), teams])
                    my_counter += 1
        except AttributeError:
            return all_data
        return all_data

    def clean_q_name(self, q_name):
        return float(q_name[1:-1])

    def clean_q_value(self, q_value):
        return float(q_value)
