"""
WebScraping Part - By Chen Yangyifan
In this part, we try to scrap the Chinese inter-bank Exchange rates from website of Chinese central bank
This website is maiitained by Money Policy Department of PBOC.
Main packages we use: re, seleniumrequests, BeautifulSoup
Webpage: http://www.pbc.gov.cn/zhengcehuobisi/125207/125217/125925/index.html
After data collection and cleaning process, we save it into "all_quots.pkl" for later use.
"""

import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt

import re
import requests
from bs4 import BeautifulSoup

# my main scape function
def my_scaper(addr, finaldf, webdriver):
    """
    this function will scrape exchange rates from MPD of PBOC:
    Step 1: scrape the webpage at addr
    Step 2: append the exchanges rates into the dataframe finaldf
    Step 3: return the finaldf
    """

    import re
    from bs4 import BeautifulSoup
    import requests
    import datetime
    import pandas as pd

    response = webdriver.request("GET", addr)
    response.encoding = "utf-8"
    s = BeautifulSoup(response.text, "lxml")  # Use `lxml` to parse the webpage.
    # Find the date
    date = re.search(r"\d+年\d+月\d+日", s.text).group()
    date = datetime.datetime.strptime(date, "%Y年%m月%d日")
    # save the webpage locally for proofreading
    with open("Webpages/{}.html".format(date), mode="wb") as fd:
        fd.write(response.content)

    # use the selector to findout the paragraph we need
    tag = s.select("#zoom > p:nth-child(1)")

    ## Find the quots
    quots = re.findall(r"1\w+对人民币\d+.\d+元", tag[0].get_text())
    df = pd.DataFrame()
    for quot in quots:
        temp = re.split(r"对人民币", quot)
        currency = temp[0][:]
        df[currency] = [temp[1][:-1]]
        df["date"] = [date]
    df.set_index("date", inplace=True)
    df.index = pd.to_datetime(df.index)
    finaldf = pd.concat([finaldf, df], 0)
    finaldf.sort_index(inplace=True)

    return finaldf


# Web_scraping with seleniumrequests

from seleniumrequests import Chrome
webdriver = Chrome()

# Scrape the quots from 82 pages
for i in range(1, 83):
    index1 = r"http://www.pbc.gov.cn/zhengcehuobisi/125207/125217/125925/17105/index{}.html".format(
        i
    )
    response = webdriver.request("GET", index1)
    response.encoding = "utf-8"
    s = BeautifulSoup(response.text, "lxml")

    hrefs = {tag.get("href") for tag in s.find_all("a")}
    hrefs = list(hrefs)
    # select those useful links
    recomp = re.compile(r"/zhengcehuobisi/125207/125217/125925/\d+.*")
    hrefs = [
        "http://www.pbc.gov.cn" + str(item) for item in hrefs if recomp.match(str(item))
    ]

    for addr in hrefs:
        try:
            fdf = my_scaper(addr, fdf, webdriver)
        except:
            print("Fail at {}".format(addr))
            continue
fdf = fdf.astype("float")

fdf.columns = ["USD", "EUD", "100JPY", "HKD", "GBP", "AUD", "NZD", "SGD", "CFH", "CAD"]
fdf.to_pickle("all_quots.pkl")
fdf.tail()
