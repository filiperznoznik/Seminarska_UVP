from web_scrapper import *

def main(): 
    albumi_csv = 'albumi.csv'
    albumi_html = 'albumi.html'
    podatki1 ='podatki1'
    url = "https://www.besteveralbums.com/overall.php?o=&f=&fv=&orderby=-InfoRankScore&sortdir=asc&page=1"
    shrani_stran(url, podatki1, albumi_html)
    seznam = albumi_iz_datoteke(albumi_html,podatki1)
    celoten_csv(seznam, podatki1, albumi_csv)
if __name__ == '__main__':
    main()