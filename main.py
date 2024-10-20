from web_scrapper import *

def main(): 
    albumi_csv = 'albumi.csv'
    podatki1 ='podatki1' 
    sez_slovarjev = []
    for stevilka_podstrani in range(1,1001):
        time.sleep(1)
        html_dat = f"podstran_{stevilka_podstrani}"
        url = f"https://www.besteveralbums.com/overall.php?o=&f=&fv=&orderby=-InfoRankScore&sortdir=asc&page={stevilka_podstrani}"
        shrani_stran(url, podatki1, html_dat)
        vsebina = preberi_datoteko_v_string(podatki1, html_dat)
        albumi = poisci_albume(vsebina)
        for i,album in enumerate(albumi):
            sez_slovarjev.append(naredi_slovar_iz_albuma(album))
    celoten_csv(sez_slovarjev, podatki1, albumi_csv) 
if __name__ == '__main__':
    main()