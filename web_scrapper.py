import os
import time
import requests
import re
import csv

podatki = "podatki"
user_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

#uzame url podstrani in ga pretvori v text
def url_v_niz(url):
    spletna_podstran = requests.get(url, headers=user_agent)
    return spletna_podstran.text

#uzame ta niz, naredi mapo ce ne obstaja, in da datoteko s textom v to mapo 
def niz_v_datoteko(text, mapa, ime_datoteke):
    os.makedirs(mapa, exist_ok=True)
    path = os.path.join(mapa, ime_datoteke)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None

#poveze prejsni dve funkciji za lepsi zapis
def shrani_stran(url, mapa, ime_datoteke):
    html_besedilo = url_v_niz(url) #text
    niz_v_datoteko(html_besedilo, mapa, ime_datoteke)

#iterira po podstraneh, pobere html in naredi mapo tekstovnih datotek 'podatki'
#pomozna funkcija za pridobitev vseh html-jev da lahko napisem regularne izraze
def pobiranje_html():
    for stevilka_podstrani in range(1,1001):
        url = f"https://www.besteveralbums.com/overall.php?o=&f=&fv=&orderby=-InfoRankScore&sortdir=asc&page={stevilka_podstrani}"
        html_dat = f"podstran_{stevilka_podstrani}"
        shrani_stran(url, podatki, html_dat)
        time.sleep(1)
    return None

#pobiranje_html()

#odpre datoteko v mapi 'podatki'
def preberi_datoteko_v_string(mapa, ime_datoteke):
    with open(os.path.join(mapa, ime_datoteke),"r", encoding="utf-8") as f:
        return f.read()

#poisce vse albume (10 na stran) na podstrani    
def poisci_albume(spletna_podstran):
    vzorec = r'<source type="image/w.*?(<div class="chartstring chart-rank-note-col">)'
    return re.findall(vzorec, spletna_podstran, flags=re.DOTALL)

#naredi slovar za posamezen album
def naredi_slovar_iz_albuma(album):
    vzorec_izvajalec = r'title="Click to see further details regarding this artist">(.*?)</a>'
    vzorec_naslov = r'title="Click to see further details regarding this album.">(.*?)</a>'
    vzorec_letnica = r'Year of Release:</div><div class="chart-stats-metric">(\d{4})'
    vzorec_rank = r'(\d{1,5})</a></div><div  class="chartstring">'
    vzorec_rank_score = r'Rank Score:</div><div class="chart-stats-metric">(\d{1,5})'
    vzorec_rating = r'title="Click to see the ratings for this album.">(\d{1,3}\.\d{1,2})'

    izvajalec = re.search(vzorec_izvajalec, album).group(1)
    naslov = re.search(vzorec_naslov, album).group(1)
    letnica = re.search(vzorec_letnica, album).group(1)
    rank = re.search(vzorec_rank, album).group(1)
    rank_score = re.search(vzorec_rank_score, album).group(1)
    rating = re.search(vzorec_rating, album).group(1)
    return {"izvajalec": izvajalec,
            "naslov": naslov,
            "letnica": letnica,
            "rank": rank,
            "rank_score": rank_score,
            "rating": rating}

#zdruzi prejsnje tri funkcije in naredi seznam vseh albumov (oz. njihovih slovarjev)
def albumi_iz_datoteke(ime_datoteke, mapa):
    vsebina = preberi_datoteko_v_string(mapa, ime_datoteke)
    albumi = poisci_albume(vsebina)
    sez_slovarjev = []
    for i,album in enumerate(albumi):
        try:
            sez_slovarjev.append(naredi_slovar_iz_albuma(album))
        except AttributeError:
            print(f"tezava z oglasom {i}")
    return sez_slovarjev

#naredi csv datoteko
def napisi_csv(stolpci, vrstice, mapa, ime_datoteke):
    os.makedirs(mapa, exist_ok=True)
    path = os.path.join(mapa, ime_datoteke)
    with open(path, 'w', encoding='utf-8',newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=stolpci)
        writer.writeheader()
        for vrstica in vrstice:
            writer.writerow(vrstica)
    return

#naredi csv datoteko iz podatkov o albumih
def celoten_csv(albumi, mapa, ime_datoteke):
    assert albumi and (all(slo.keys() == albumi[0].keys() for slo in albumi))
    napisi_csv(albumi[0].keys(), albumi, mapa, ime_datoteke)


  #SPREMNI IMENA FUNKCIJ IN SPREMENLJIVK TER DODAJ KOMENATRJE!!!!!!!!!!!!!
