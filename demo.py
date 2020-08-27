from contextlib import suppress

from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import requests
from lxml.html.soupparser import fromstring
from lxml import etree
from selenium import webdriver


# driver = requests.get("https://www.bet365.com/#/IP/B1")
# result = driver.links
# #print(result)
# soup = BeautifulSoup(driver.text, 'html.parser')
# mydivs = soup.select("ovm-FixtureDetailsTwoWay_TeamName ")
# print(soup)

from requests_html import HTMLSession
import pyppdf.patch_pyppeteer
from bs4 import BeautifulSoup

url = "https://www.bet365.com/#/IP/B1"

session = HTMLSession()


resp = session.get(url)
resp.html.render()
html = resp.html.html

page_soup = BeautifulSoup(html, 'html.parser')

containers = page_soup.find_all("div", {"class": "grid-item"})
print(page_soup)
resp.close()
session.close()
# soup = BeautifulSoup(driver, 'html.parser')
# rows = soup.find_all('div')
# items = []
# for row in rows:
#     if row.has_attr('class'):
#         with suppress(IndexError):
#             if "ipo-TeamStack_Team" in row['class']:
#                 items.append(row.text)
#             elif any(x.startswith("ipo-TeamPoints_TeamScore") for x in row['class']):
#                 items.append(row.text)
#
# print([Match(*x) for x in chunks(items, 6)])
