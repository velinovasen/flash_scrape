from contextlib import suppress
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import requests
import time
import re

WEB_LINKS = {
    "Football": "https://www.flashscore.com/football/",
    "Tennis": "https://www.flashscore.com/tennis/"
}


data = []


driver = Chrome()
driver.get(WEB_LINKS["Football"])
time.sleep(2)

while True:
    with suppress(Exception):
        driver.find_element_by_css_selector("#live-table > div.tabs > div.tabs__group > div:nth-child(4) > div").click()
        break

html = driver.execute_script("return document.documentElement.outerHTML;")
soup = BeautifulSoup(html, 'html.parser')
rows = soup.find_all('div')
items = []
for row in rows:
    if row.has_attr('class'):
        with suppress(IndexError):
            if "event__match event__match--oneLine" in row['class']:
                items.append(row.text)
print(rows)
print(items)

# for x in range(len(rows)):
#     if len(rows[x]) > best:
#         best = x
#     cls = rows[x].attrs.get("class")
#     print(rows[x])
#

