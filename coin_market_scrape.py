# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 17:52:32 2020

@author: Awoyele Temiloluwa
"""
#importing libraries
from requests import get
from bs4 import BeautifulSoup
import pandas as pd


filename = "coinmarketcap_scrape.csv"
columns = ["Coin Name" , "Market Cap" , "Price" , "Volume(24h)" , "Circulating Supply" , "Change(24h)"]
data = pd.DataFrame(columns=columns)
for page in range(1,29):
    #url link to our website
    url = f"https://coinmarketcap.com/{page}/"

    #send  a request to the website and grab the response
    client = get(url)
    
    #caution incase of bad internet connection
    try:
        client.raise_for_status()
    except Exception as exc:
        print("There is a problem %s"%(exc))
        
    
    html = client.text
    
    client.close()#close client request
    
    soup = BeautifulSoup(html , "html.parser")
    rows = soup.findAll("tr" , {"class":"cmc-table-row"})
    
    
    df = pd.DataFrame(columns=columns)
    for row in rows:
        name = row.select("td > div > a[title]")[0].text
        market_cap = row.find("td" , {"class":"cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__market-cap"}).text
        price = row.find("td" , {"class":"cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price"}).text
        volume = row.find("td" , {"class":"cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__volume-24-h"}).text
        supply = row.find("td" , {"class":"cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__circulating-supply"}).text
        supply.replace("*","")
        change = row.find("td" , {"class":"cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-24-h"}).text
        _ = pd.DataFrame([[name,market_cap,price,volume,supply,change]] , columns=columns)
        df = df.append(_)
        
    data = data.append(df)
    
data.to_csv(filename , index=False)