import math
import re
import requests
from izluscevanje_podatkov import izlusci_bloke, izlusci_podatke

prvotni_url_naslov = "https://math.stackexchange.com/questions"


def shrani_vprasanja_v_seznam(stran):
    vprasanja = []
    html1 = requests.get(stran)
    with open("micka.htm", "w", encoding="utf8") as dat:
        dat.write(html1.text)
    bloki = izlusci_bloke(html1.text)
    for blok in bloki:
        vprasanje = izlusci_podatke(blok)
        vprasanja.append(vprasanje)
    return vprasanja,len(vprasanja)

print(shrani_vprasanja_v_seznam(prvotni_url_naslov))

