def naredi_slovar_iz_albuma(album):
    vzorec_izvajalec = r' regarding this artist">(.*?)<'
    vzorec_naslov = r' regarding this album.">(.*?)<'
    vzorec_letnica = r'metric">(\d{4})'
    vzorec_rank = r'overall.php.rank=(\d{1,5})'
    vzorec_rank_score = r'Rank Score:<(.*?)metric">(\d{1,5})'
    vzorec_rating = r'>(\d{1,3}) '

    izvajalec = re.search(vzorec_izvajalec, album, flags=re.DOTALL).group(1)
    naslov = re.search(vzorec_naslov, album, flags=re.DOTALL).group(1)
    letnica = re.search(vzorec_letnica, album, flags=re.DOTALL).group(1)
    rank = re.search(vzorec_rank, album, flags=re.DOTALL).group(1)
    rank_score = re.search(vzorec_rank_score, album, flags=re.DOTALL).group(1) #popravi nazaj na 2
    rating = re.search(vzorec_rating, album, flags=re.DOTALL).group(1)
    return {"izvajalec": izvajalec,
            "naslov": naslov,
            "letnica": letnica,
            "rank": rank,
            "rank_score": rank_score,
            "rating": rating}


def extract_with_default(pattern, text, default="Unknown"):
    match = re.search(pattern, text, flags=re.DOTALL)
    return match.group(1) if match else default


def naredi_slovar_iz_albuma(album):
    vzorec_izvajalec = r'regarding this artist">(.*?)<'
    vzorec_naslov = r'regarding this album.">(.*?)<'
    vzorec_letnica = r'metric">(\d{4})'
    vzorec_rank = r'overall.php.rank=(\d{1,5})'
    vzorec_rank_score = r'Rank Score:<(.*?)metric">(\d{1,5})'
    vzorec_rating = r'>(\d{1,3}) '

    return {
        "izvajalec": extract_with_default(vzorec_izvajalec, album),
        "naslov": extract_with_default(vzorec_naslov, album),
        "letnica": extract_with_default(vzorec_letnica, album),
        "rank": extract_with_default(vzorec_rank, album),
        "rank_score": extract_with_default(vzorec_rank_score, album, default="0"),
        "rating": extract_with_default(vzorec_rating, album, default="0")
    }