from contextlib import suppress
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time
import re

WEB_LINKS = {
    "Football": "https://www.flashscore.com/football/",
    "Tennis": "https://www.flashscore.com/tennis/"
}


data = []

options = Options()
options.headless = True
driver = Chrome(options=options, executable_path='C:\Windows\chromedriver.exe')
driver.get(WEB_LINKS["Football"])


while True:
    with suppress(Exception):
        driver.find_element_by_css_selector("#live-table > div.tabs > div.tabs__group > div:nth-child(4) > div").click()
        break

html = driver.execute_script("return document.documentElement.outerHTML;")
soup = BeautifulSoup(html, 'html.parser')
matches = soup.find_all(class_=re.compile("event__match"))

for row in matches:
    token = str(row)
    tokens = token.split('div ')
    items = {"time": None, "home_team": None, "away_team": None, "home_odd": None,
             "draw_odd": None, "away_odd": None}
    for el in tokens:
        if 'class="event__time' in el:
            pattern = r'\d+[:]\d{2}'
            time = re.search(pattern, el)
            items["time"] = time.group()
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

    #print(tokens)

    result_to_print = f""
    for key, value in items.items():
        result_to_print += f"---[{key}---{value}]---"
    print(result_to_print)
print(len(matches))
