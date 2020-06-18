# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


with open("BASE-Quellen-20200424-Rest.html","r",encoding="utf-8") as fp:
    soup = BeautifulSoup(fp)

out = open("BASE-Quellen-Rest.txt","w",encoding="utf-8")

contentProviders = soup.find_all('div', class_='ContentProvider')

for contentProvider in contentProviders:
    out.write(contentProvider.text + "\n")
    
out.close