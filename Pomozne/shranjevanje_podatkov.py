import requests
import csv
from Pomozne.izluscevanje_podatkov import izlusci_bloke, izlusci_podatke1, izlusci_stevilo_vseh_strani_in_vprasanj


def shrani_v_txt_datoteko(ime_txt_datoteke, html):
    with open(ime_txt_datoteke, "w", encoding="utf8") as f:
        f.write(html)
    return None


def shrani_vprasanja_v_seznam(stran):
    vprasanja = []
    html1 = requests.get(stran)
    bloki = izlusci_bloke(html1.text)
    for blok in bloki:
        vprasanje = izlusci_podatke1(blok)
        vprasanja.append(vprasanje)
    return vprasanja


def shrani_vprasanja(ime_dat):
    with open(ime_dat, "w", encoding="utf8") as dat:
        pisatelj = csv.writer(dat)
        pisatelj.writerow(
            [
                "id",
                "ime",
                "tags",
                "glasovi",
                "odgovori",
                "ogledi",
                "datum in ura"
            ]
        )
    strani = izlusci_stevilo_vseh_strani_in_vprasanj()[1]
    for stevilka_strani in range(1, strani+1):
        vprasanja = shrani_vprasanja_v_seznam(
            f"https://math.stackexchange.com/questions?tab=newest&page={stevilka_strani}&pagesize=50"
        )
        with open(ime_dat, "a", encoding="utf8") as datt:
            pisatelj = csv.writer(datt)
            for vprasanje in vprasanja:
                pisatelj.writerow(
                    [
                        vprasanje["id"],
                        vprasanje["ime"],
                        vprasanje["tags"],
                        vprasanje["glasovi"],
                        vprasanje["odgovori"],
                        vprasanje["ogledi"],
                        vprasanje["datum in čas objave"]
                    ]
                )
        print(f"Shranjeno ({stevilka_strani}/{strani})")
    print("CSV je uspešno shranjen.")
