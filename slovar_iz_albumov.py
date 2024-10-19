def naredi_slovar_iz_albuma(album):
    vzorec_izvajalec = r'regarding this artist">(.*?)<'
    vzorec_naslov = r'regarding this album.">(.*?)<'
    vzorec_letnica = r'Year of Release:</div><div class="chart-stats-metric">(\d+)<'
    vzorec_rank = r'overall.php.rank=(\d+)#'
    vzorec_rank_score = r'Rank Score:<.*?metric">(\d+,\d+)<'
    vzorec_rating = r'(\d+) \('

    izvajalec = re.search(vzorec_izvajalec, album, flags=re.DOTALL).group(1)
    naslov = re.search(vzorec_naslov, album, flags=re.DOTALL).group(1)
    letnica = re.search(vzorec_letnica, album)
    rank = re.search(vzorec_rank, album)
    rank_score = re.search(vzorec_rank_score, album)
    rating = re.search(vzorec_rating, album)
    return {"izvajalec": izvajalec,
            "naslov": naslov,
            "letnica": letnica,
            "rank": rank,
            "rank_score": rank_score,
            "rating": rating}







def poisci_albume2(spletna_podstran):
    vzorec = r'Year of.+?votes'
    return re.findall(vzorec, spletna_podstran, flags=re.DOTALL)


