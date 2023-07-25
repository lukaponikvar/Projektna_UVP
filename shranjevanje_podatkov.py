import requests
from izluscevanje_podatkov import izlusci_bloke, izlusci_podatke


def shrani_v_txt_datoteko(ime_txt_datoteke, html):
    with open(ime_txt_datoteke, "w", encoding="utf8") as f:
        f.write(html)
    return None


def shrani_vprasanja_v_seznam(stran):
    vprasanja = []
    html1 = requests.get(stran)
    with open("micka.htm", "w", encoding="utf8") as dat:
        dat.write(html1.text)
    bloki = izlusci_bloke(html1.text)
    for blok in bloki:
        vprasanje = izlusci_podatke(blok)
        vprasanja.append(vprasanje)
    return vprasanja
