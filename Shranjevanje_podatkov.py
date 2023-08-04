import requests
import csv
import os
from Izluscevanje_podatkov import izlusci_bloke, izlusci_podatke_iz_bloka, izlusci_stevilo_vseh_vprasanj_in_vseh_strani


najvec_strani = izlusci_stevilo_vseh_vprasanj_in_vseh_strani()[1]


def shrani_v_txt_datoteko(ime_txt_datoteke, html):
    """Funkcija HTML izbrane strani shrani v datoteko z želenim imenom."""
    with open(ime_txt_datoteke, "w", encoding="utf8") as f:
        f.write(html)
    return None


def shrani_vprasanja_v_seznam(stran):
    """Funkcija iz spletne strani potegne HTML in vprašanja na njem shrani v seznam."""
    vprasanja = []
    html_strani = requests.get(stran).text
    bloki = izlusci_bloke(html_strani)
    for blok in bloki:
        vprasanje = izlusci_podatke_iz_bloka(blok)
        vprasanja.append(vprasanje)
    return vprasanja


def naredi_CSV_1(ime_datoteke):
    """Funkcija naredi CSV datoteko in vanjo vpiše začetne podatke."""
    with open(ime_datoteke, "w", encoding="utf8") as dat:
        pisatelj = csv.writer(dat)
        pisatelj.writerow(
            [
                "Id",
                "Ime",
                "Opomba",
                "Glasovi",
                "Odgovori",
                "Sprejet odgovor",
                "Ogledi",
                "Leto",
                "Mesec",
                "Dan",
                "Ura",
            ]
        )


def naredi_CSV_2(ime_datoteke):
    """Funkcija naredi pomožno CSV datoteko in vanjo vpiše začetne podatke."""
    with open(ime_datoteke, "w", encoding="utf8") as dat:
        pisatelj = csv.writer(dat)
        pisatelj.writerow(
            [
                "Id",
                "Oznaka",
            ]
        )


def vpiši_podatke_v_CSV(pot_1, pot_2, stevilo_strani):
    """funkcija v CSV zapiše informacije o vprašanjih"""
    for stevilka_strani in range(1, int(stevilo_strani)+1):
        vprasanja = shrani_vprasanja_v_seznam(
            f"https://math.stackexchange.com/questions?tab={filter}&page={stevilka_strani}&pagesize=50"
        )
        with open(pot_1, "a", encoding="utf8") as datoteka:
            with open(pot_2, "a", encoding="utf8") as datoteka_pom:
                pisatelj = csv.writer(datoteka)
                pisatelj_pom = csv.writer(datoteka_pom)
                for vprasanje in vprasanja:
                    pisatelj.writerow(
                        [
                            vprasanje["Id"],
                            vprasanje["Ime"],
                            vprasanje["Opomba"],
                            vprasanje["Glasovi"],
                            vprasanje["Odgovori"],
                            vprasanje["Sprejet odgovor"],
                            vprasanje["Ogledi"],
                            vprasanje["Leto"],
                            vprasanje["Mesec"],
                            vprasanje["Dan"],
                            vprasanje["Ura"],
                        ]
                    )
                    for oznaka in vprasanje["Oznake"]:
                        pisatelj_pom.writerow([vprasanje["Id"], oznaka])
        print(f"Shranjeno ({stevilka_strani}/{stevilo_strani})")
    print("CSV je bil uspešno shranjen.")


def shrani_vprasanja_v_CSV(ime_CSV_datoteke, mapa="", stevilo_strani=None, filter="newest"):
    """Funkcija v CSV datoteki z želenimi imeni shrani informacije o vprašanjih. Lahko ji predpišemo koliko 
    strani s foruma želimo, če tega ne storimo, bo funkcija prensesla vse strani. Predpišemo ji lahko tudi filter. 
    Če delovanje funcije prekinemo, bo vseeno naredila CSV datoteko z do takrat prenesenimi stranmi."""
    filtri = ["newest", "active", "bounties",
              "unanswered", "frequent", "votes"]
    try:
        if filter.casefold() not in filtri:
            raise ValueError
        elif not stevilo_strani or int(stevilo_strani) > najvec_strani:
            stevilo_strani = najvec_strani
        os.makedirs(mapa, exist_ok=True)
        pot = os.path.join(mapa, ime_CSV_datoteke)
        pot_oznake = pot[:-4]+"_oznake.csv"
        naredi_CSV_1(pot)
        naredi_CSV_2(pot_oznake)
        vpiši_podatke_v_CSV(pot, pot_oznake, stevilo_strani)
    except ValueError:
        print("Vnešeni podatki so napačni!")
        print("Možnosti za filter so:")
        for i in filtri:
            print(i.title())
