from selenium import webdriver
import selenium
from bs4 import BeautifulSoup as bs4
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



class Bet(object):
    base_url = "https://www.yandex.ru"

    matches_teams_selector = ""
    main_quotes_selector = ""
    matches_links_selector = ""

    add_slash_url = False
    is_sleeps = False
    dynamic_team_name = False

    handicap_period_all = "Победа с учетом форы"
    handicap_period_all_copy = "###"

    handicap_period_1 = "Победа с учетом форы, 1-й тайм"
    handicap_period_2 = "Победа с учетом форы, 2-й тайм"
    handicap_period_3 = "###"
    handicap_period_4 = "###"

    total_periods_all = "Тотал голов"
    total_periods_all_copy = "###"
    total_periods_all_by_team = "Тотал голов ({})"
    total_periods_all_by_team_copy_1 = "###"
    total_periods_all_by_team_copy_2 = "###"

    total_period_1_by_team = "Тотал голов ({}), 1-й тайм"
    total_period_2_by_team = "Тотал голов ({}), 2-й тайм"
    total_period_3_by_team = "###"
    total_period_4_by_team = "###"

    total_period_1 = "По таймам Тотал (1-й тайм)"
    total_period_2 = "По таймам Тотал (2-й тайм)"
    total_period_3 = "#"
    total_period_4 = "#"

    result_period_1 = "Результат, 1-й тайм"
    result_period_2 = "Результат, 2-й тайм"
    result_period_3 = "###"
    result_period_4 = "###"

    result_period_1_copy = "###"
    result_period_2_copy = "###"
    result_period_3_copy = "###"
    result_period_4_copy = "###"

    result_period_all = "Результат, основное время"
    result_period_all_copy = "###"

    result_team = "{} (победа)"
    result_team_X = "Ничья"
    result_team_or_X = "{} (победа) или ничья"
    result_team_or_X_copy = "###"
    result_team_or_team = "{} (победа) или {} (победа)"

    under_text = "Меньше"
    over_text = "Больше"

    team1 = team2 = ""

    is_extra_js_command = False
    extra_js_command = "console.log('Hi')"

    def __init__(self):
        self.update_dicts()

    def update_dicts(self):
        self.result_period_number = {
            self.result_period_1: 1,
            self.result_period_2: 2,
            self.result_period_3: 3,
            self.result_period_4: 4,
            self.result_period_all: 0,
            self.result_period_1_copy: 1,
            self.result_period_2_copy: 2,
            self.result_period_3_copy: 3,
            self.result_period_4_copy: 4,
            self.result_period_all_copy: 0,
        }

        self.result_team_number = {
            self.result_team.format(self.team1): 0,
            self.result_team_X: 1,
            self.result_team.format(self.team2): 2,

            self.result_team_or_X.format(self.team1): 3,
            self.result_team_or_X_copy.format(self.team1): 3,
            self.result_team_or_team.format(self.team1, self.team2): 4,
            self.result_team_or_X.format(self.team2): 5,
            self.result_team_or_X_copy.format(self.team2): 5,
        }

        self.handicap_period_number = {
            self.handicap_period_1: 1,
            self.handicap_period_2: 2,
            self.handicap_period_3: 3,
            self.handicap_period_4: 4,
            self.handicap_period_all: 0,
            self.handicap_period_all_copy: 0,
        }

        self.total_team_number = {
            self.total_periods_all: 0,
            self.total_periods_all_copy: 0,
            self.total_periods_all_by_team.format(self.team1): 1,
            self.total_periods_all_by_team.format(self.team2): 2,
            self.total_periods_all_by_team_copy_1: 1,
            self.total_periods_all_by_team_copy_2: 2,
            self.total_period_1_by_team.format(self.team1): 1,
            self.total_period_1_by_team.format(self.team2): 2,
            self.total_period_2_by_team.format(self.team1): 1,
            self.total_period_2_by_team.format(self.team2): 2,
            self.total_period_3_by_team.format(self.team1): 1,
            self.total_period_3_by_team.format(self.team2): 2,
            self.total_period_4_by_team.format(self.team1): 1,
            self.total_period_4_by_team.format(self.team2): 2,
            self.total_period_1: 0,
            self.total_period_2: 0,
            self.total_period_3: 0,
            self.total_period_4: 0,
        }

        self.total_period_number = {
            self.total_periods_all: 0,
            self.total_periods_all_copy: 0,
            self.total_periods_all_by_team.format(self.team1): 0,
            self.total_periods_all_by_team.format(self.team2): 0,
            self.total_periods_all_by_team_copy_1: 0,
            self.total_periods_all_by_team_copy_2: 0,
            self.total_period_1_by_team.format(self.team1): 1,
            self.total_period_1_by_team.format(self.team2): 1,
            self.total_period_2_by_team.format(self.team1): 2,
            self.total_period_2_by_team.format(self.team2): 2,
            self.total_period_3_by_team.format(self.team1): 3,
            self.total_period_3_by_team.format(self.team2): 3,
            self.total_period_4_by_team.format(self.team1): 4,
            self.total_period_4_by_team.format(self.team2): 4,
            self.total_period_1: 1,
            self.total_period_2: 2,
            self.total_period_3: 3,
            self.total_period_4: 4,
        }

    def get_pages_by_urls(self, urls):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Remote("http://172.31.12.48:4444/wd/hub",
                                  desired_capabilities=webdriver.DesiredCapabilities.CHROME,
                                  options=options)
        pages = list()
        for url in urls:
            driver.get(self.base_url)
            print(url)
            driver.get(url=url)
            if self.is_sleeps:
                time.sleep(5)
            driver = self.extra_commands_by_driver(driver=driver)
            page = driver.page_source
            page = bs4(page, 'lxml')
            pages.append([page, url])
        driver.quit()
        return pages

    def extra_commands_by_driver(self, driver):
        try:
            driver.execute_script(self.extra_js_command)
        except selenium.common.exceptions.WebDriverException:
            print("Extra command error")
        return driver

    def get_events_urls_by_leagues_urls(self, urls):
        data = list()
        pages = self.get_pages_by_urls(urls=urls)
        for page in pages:
            html, url = page
            links = self.get_match_links(page=html)
            data.append([links, url])
        return data

    def get_match_links(self, page):
        matches_links_elements = page.select(selector=self.matches_links_selector)
        slash = "/" if self.add_slash_url else ""
        return [self.base_url + slash + link["href"] for link in matches_links_elements]

    def get_teams(self, page):
        teams_elements = page.select(selector=self.matches_teams_selector)
        return [link.text.strip() for link in teams_elements]

    def get_main_quotes(self, page):
        main_quotes = page.select(selector=self.main_quotes_selector)
        result = list()
        try:
            result.append([0, 0, float(main_quotes[0].text.strip())])
            result.append([0, 1, float(main_quotes[1].text.strip())])
            result.append([0, 2, float(main_quotes[2].text.strip())])
            result.append([0, 3, float(main_quotes[3].text.strip())])
            result.append([0, 4, float(main_quotes[4].text.strip())])
            result.append([0, 5, float(main_quotes[5].text.strip())])
        except ValueError:
            return result
        return result

    def get_results(self, name, sub_name, q_name, q_value, team1, team2):
        pass

    def get_handicap(self, name, sub_name, q_name, q_value, team1, team2):
        pass

    def get_total(self, name, sub_name, q_name, q_value, team1, team2):
        pass

    def get_quartets(self, page, teams):
        pass

    def get_all_quotes_by_urls(self, urls):
        data = list()

        pages_urls_array = self.get_pages_by_urls(urls=urls)
        counter = 0
        for page_url in pages_urls_array:
            counter += 1
            if counter >= 12:
                continue
            results = list()
            handicaps = list()
            totals = list()
            page, url = page_url
            teams = self.get_teams(page=page)
            try:
                team1, team2 = teams
            except ValueError:
                print("Error. No team names")
                continue
            self.team1, self.team2 = teams
            if self.dynamic_team_name:
                self.update_dicts()
            results = self.get_main_quotes(page=page)
            quartets = self.get_quartets(page=page, teams=teams)
            for quartet in quartets:
                name, sub_name, q_name, q_value, teams = quartet
                if name in self.result_period_number:
                    results.append(self.get_results(name, sub_name, q_name, q_value, team1, team2))
                elif name in self.handicap_period_number:
                    handicaps.append(self.get_handicap(name, sub_name, q_name, q_value, team1, team2))
                elif name in self.total_period_number:
                    totals.append(self.get_total(name, sub_name, q_name, q_value, team1, team2))

            data.append([results, handicaps, totals, teams, url])
        return data

    def clean_q_name(self, q_name):
        pass

    def clean_q_value(self, q_value):
        pass
