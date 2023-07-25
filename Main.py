import csv
from izluscevanje_podatkov import izlusci_stevilo_vseh_strani_in_vprasanj
from shranjevanje_podatkov import shrani_vprasanja_v_seznam


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

    for stevilka_strani in range(1, izlusci_stevilo_vseh_strani_in_vprasanj()[1]):
        vprasanja = shrani_vprasanja_v_seznam(
            f"https://math.stackexchange.com/questions?tab=newest&page={stevilka_strani}&pagesize=50")
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
