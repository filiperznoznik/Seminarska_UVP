import csv
import os
import requests
import time
import re


url = "https://www.nepremicnine.net/oglasi-prodaja/stanovanje/"
podatki_stanovanja = "podatki"
html_datoteka = "glavna_stran.html"
csv_datoteka = "podatki.csv"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

def url_v_niz(url):
    try:
        page_content = requests.get(url, headers=headers)
        return page_content.text
    except Exception:
        print("nekaj je narobe")
        return "prazna stran"
    
def niz_v_datoteko(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None

def save_frontpage(page, directory, filename):
    html_besedilo = url_v_niz(page)
    niz_v_datoteko(html_besedilo, directory, filename)

save_frontpage(url, podatki_stanovanja, html_datoteka)


def preglej_podstrani():
    for i in range(1,840):
       mapa_za_html = "stanovanja"
       url_podstrani =  f"https://www.nepremicnine.net/oglasi-prodaja/stanovanje/{i}/"
       shrani_podstran_v_html = f"stanovanja_podstran{i}.html" 
       save_frontpage(url_podstrani,mapa_za_html,shrani_podstran_v_html)
       time.sleep(5)

preglej_podstrani()
