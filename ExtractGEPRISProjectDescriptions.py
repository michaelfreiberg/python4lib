# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import requests

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

with open("Suche-Seite-01.html","r",encoding="utf-8") as fp:
    soup = BeautifulSoup(fp)

log = open("Projekte-Seite-01-log.txt","w",encoding="utf-8")

# projectEntries = soup.find_all(class_=re.compile("eintrag"))
projectEntries = soup.find_all('div', class_='results')

for projectEntry in projectEntries:
    projectLink = projectEntry.h2.a["href"]
    projectNumberSearch = re.search('\d+', projectLink, re.IGNORECASE)
    if projectNumberSearch:
        projectNumber = projectNumberSearch.group(0)
    
    log.write(projectLink + "\n")
    
    projectPrintViewURL = "https://gepris.dfg.de" + projectLink + "?displayMode=print"
    req = requests.get(projectPrintViewURL, headers)
    projectDescriptionSoup = BeautifulSoup(req.content)
    
    
    if projectEntry.find_all("img", title = re.compile("Projektabschlussbericht")):
        log.write("*mit Projektergebnissen\n\n")
        
        projectResultsPrintViewURL = "https://gepris.dfg.de" + projectLink + "?displayMode=print&selectedSubTab=2"
        req = requests.get(projectResultsPrintViewURL, headers)
        projectResultsSoup = BeautifulSoup(req.content)
        
        resultDescription = projectResultsSoup.find_all('div', id = "projektbeschreibung")  
        projectDescriptionSoup.find(id="projektbeschreibung").insert_after(projectResultsSoup)
    
    projectDescriptionHTML = projectDescriptionSoup.prettify()
    projectDescriptionHTML = projectDescriptionHTML.replace('/gepris/', 'https://gepris.dfg.de/gepris/')
    
    projectOut = open(projectNumber + ".html","w",encoding="utf-8")
    projectOut.write(projectDescriptionHTML)
    projectOut.close
        

log.close
