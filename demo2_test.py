import re
import sqlite3
import time
from contextlib import suppress

from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

WEB_LINKS = {
        "Football": "https://www.flashscore.com/football/",
        "Tennis": "https://www.flashscore.com/tennis/"
    }

all_data = []

conn = sqlite3.connect('test_bin.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS allGames')
c.execute('CREATE TABLE allGames(time TEXT, home_team TEXT, '
              'away_team TEXT, home_odd REAL, draw_odd REAL, away_odd REAL)')

options = Options()
options.headless = True
driver = Firefox(options=options, executable_path='C:\Windows\geckodriver.exe')
driver.get(WEB_LINKS["Football"])

while True:
    with suppress(Exception):
        driver.find_element_by_css_selector(
            "#live-table > div.tabs > div.tabs__group > div:nth-child(4) > div").click()
        break

while True:
    with suppress(Exception):
        driver.find_element_by_css_selector(
            "#live-table > div.tabs > div.calendar > div:nth-child(3) > div").click()
        break
time.sleep(3)
html = driver.execute_script("return document.documentElement.outerHTML;")
soup = BeautifulSoup(html, 'html.parser')
matches = soup.find_all(class_=re.compile("event__match"))

for row in matches:
    token = str(row)
    tokens = token.split('div ')
    items = {"time": None, "home_team": None, "away_team": None, "home_odd": "",
             "draw_odd": "", "away_odd": ""}
    # print(tokens)
    for el in tokens:
        if 'class="event__time' in el:
            # print(el)
            pattern = r'\d+[:]\d{2}'
            time = re.search(pattern, el)
            items["time"] = time.group()

        elif '"event__stage--block">' in el:
            if 'Cancelled' in el:
                items["time"] = "Cancelled"
            elif 'Postponed' in el:
                items["time"] = "Postponed"

        elif 'participant--home' in el:
            pattern = r'\"\>(.{1,})\/'
            home_search = re.search(pattern, el)
            home_team = home_search.group()[2:-2]
            items["home_team"] = home_team

        elif 'participant--away' in el:
            pattern = r'\"\>(.{1,})\/'
            away_search = re.search(pattern, el)
            away_team = away_search.group()[2:-2]
            items["away_team"] = away_team

        elif '<span alt=' in el:
            odd_pattern = r"\"\>(\d+\.\d+)\<"
            odd_search = re.search(odd_pattern, el)
            if len(tokens) - tokens.index(el) == 2:
                odd = odd_search.group()[2:-1]
                items["home_odd"] = odd
            elif len(tokens) - tokens.index(el) == 1:
                odd = odd_search.group()[2:-1]
                items["draw_odd"] = odd
            else:
                odd = odd_search.group()[2:-1]
                items["away_odd"] = odd

    c.execute('INSERT INTO allGames (time, home_team, away_team, home_odd, draw_odd, away_odd)'
                   ' VALUES (?, ?, ?, ?, ?, ?)', (items["time"], items["home_team"], items["away_team"],
                                                  items["home_odd"], items["draw_odd"], items["away_odd"]))
    conn.commit()

    # print(tokens)

    result_to_print = f""
    for key, value in items.items():
        result_to_print += f"---[{key}---{value}]---"
    print(result_to_print)

