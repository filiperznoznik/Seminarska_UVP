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
#pomozna funkcija da vidim ce sploh dela
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
    vzorec1 = r'Year of.+?--'
    vzorec2 = r'Click to see further details regarding this album.">.*?</a></div>'
    seznam1 = re.findall(vzorec1, spletna_podstran, flags=re.DOTALL)
    seznam2 = re.findall(vzorec2, spletna_podstran, flags=re.DOTALL)
    zdruzen_seznam = [a + b for a, b in zip(seznam1, seznam2)]
    return zdruzen_seznam

#pogleda, če je vse ok do tukaj
def grupiranje(vzorec, datoteka, default="Unknown"):
    match = re.search(vzorec, datoteka, flags=re.DOTALL)
    return match.group(1) if match else default

#naredi slovar za posamezen album
def naredi_slovar_iz_albuma(album):
    vzorec_izvajalec = r'regarding this artist">(.*?)<'
    vzorec_naslov = r'regarding this album.">(.*?)<'
    vzorec_letnica = r'metric">(\d{4})'
    vzorec_rank = r'overall.php.rank=(\d{1,5})'
    vzorec_rank_score = r'Rank Score:<.*?metric">(\d+,?\d+)'
    vzorec_rating = r'>(\d{1,3}) '

    return {
        "izvajalec": grupiranje(vzorec_izvajalec, album),
        "naslov": grupiranje(vzorec_naslov, album),
        "letnica": grupiranje(vzorec_letnica, album, default="0"),
        "rank": grupiranje(vzorec_rank, album, default="0"),
        "rank_score": grupiranje(vzorec_rank_score, album, default="0").replace(",",""),
        "rating": grupiranje(vzorec_rating, album, default="0")
    }


#zdruzi prejsnje tri funkcije in naredi seznam vseh albumov (oz. njihovih slovarjev)
def albumi_iz_datoteke(ime_datoteke, mapa):
    vsebina = preberi_datoteko_v_string(mapa, ime_datoteke)
    albumi = poisci_albume(vsebina)
    sez_slovarjev = []
    for i,album in enumerate(albumi):
            sez_slovarjev.append(naredi_slovar_iz_albuma(album))
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
    if not albumi or not all(slo.keys() == albumi[0].keys() for slo in albumi):
        raise ValueError("Nekaj je narobe s slovarji")
    napisi_csv(albumi[0].keys(), albumi, mapa, ime_datoteke)