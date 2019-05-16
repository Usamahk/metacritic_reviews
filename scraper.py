import pandas as pd
import numpy as np
import requests
import bs4
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen

df = pd.DataFrame(columns=["Title", "Platform", "Metascore", "User Score", "Release Date"])

for i in range(0,162):
    URL = "https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?view=condensed&sort=desc&page="+str(i)
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent':user_agent,} 
    request = urllib.request.Request(URL,None,headers) 
    response = urllib.request.urlopen(request)
    data = response.read()

    soup = BeautifulSoup(data, "html.parser")

    for games in soup.find_all('div', class_ = "product_wrap", limit=100):

        # Extract title and platform
        title_platform = games.find('a').text
        title_platform = str(title_platform).replace("\n".join(["  "]), "").strip()

        title = title_platform[0:title_platform.find('\n')]
        platform = title_platform[title_platform.find('\n')+2:len(title_platform)-1]

        # Extract Metascore and User score
        m_score = games.find('div', class_ = 'metascore_w').text
        u_score = games.find('span', class_ = 'textscore').text

        # Extract release date
        r_date = games.find_all('span', class_= 'data')[1].text

        df = df.append({'Title':title, 'Platform':platform ,'Metascore':m_score, 'User Score':u_score, 'Release Date':r_date}, ignore_index = True)