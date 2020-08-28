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
    items = {"time": None, "home_team": None, "away_team": None, "home_odd": {"old": None, "new": None},
             "draw_odd": {"old": None, "new": None}, "away_odd": {"old": None, "new": None}}
    for el in tokens:
        if 'class="event__time' in el:
            pattern = r'\d+[:]\d{2}'
            time = re.search(pattern, el)
            items["time"] = time.group()
        elif 'participant--home' in el:
            pattern = r'\"\>(.+\(|\<\/[d]|.+\<)'
            home_search = re.search(pattern, el)
            home_team = ''
            if home_search.group()[-1] == '(':
                home_team = home_search.group()[2:-2]
            else:
                home_team = home_search.group()[2:-1]
            items["home_team"] = home_team
        elif 'participant--away' in el:
            pattern = r'\"\>(.+\(|.+\<)'
            away_search = re.search(pattern, el)
            away_team = ''
            if away_search.group()[-1] == '(':
                away_team = away_search.group()[2:-2]
            else:
                away_team = away_search.groups()[2:-1]
            items["away_team"] = away_team
        elif '<span alt=' in el:
            old_odd_pattern = r"\=\"(\d+\.\d+)\["
            new_odd_pattern = r"\"\>(\d+\.\d+)\<"
            old_odd_search = re.search(old_odd_pattern, el)
            new_odd_search = re.search(new_odd_pattern, el)
    print(tokens)

    result_to_print = f""
    for key, value in items.items():
        result_to_print += f"---[{key}---{value}]---"
    print(result_to_print)
print(len(matches))

# if len(tokens) == 6:
#     if tokens.index(el) == 4:
#         items["home_odd"]["old"] = old_odd_search.group()
#         items["home_odd"]["new"] = new_odd_search.group()
#     elif tokens.index(el) == 5:
#         items["draw_odd"]["old"] = old_odd_search.group()
#         items["draw_odd"]["new"] = new_odd_search.group()
#     elif tokens.index(el) == 6:
#         items["away_odd"]["old"] = old_odd_search.group()
#         items["away_odd"]["new"] = new_odd_search.group()
# elif len(tokens) == 5:
#     if tokens.index(el) == 3:
#         items["home_odd"]["old"] = old_odd_search.group()
#         items["home_odd"]["new"] = new_odd_search.group()
#     elif tokens.index(el) == 4:
#         items["draw_odd"]["old"] = old_odd_search.group()
#         items["draw_odd"]["new"] = new_odd_search.group()
#     elif tokens.index(el) == 5:
#         items["away_odd"]["old"] = old_odd_search.group()
#         items["away_odd"]["new"] = new_odd_search.group()