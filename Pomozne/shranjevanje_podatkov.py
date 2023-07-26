import requests
import csv
from Izluscevanje_podatkov import izlusci_bloke, izlusci_podatke_iz_bloka, izlusci_stevilo_vseh_vprasanj_in_vseh_strani

najvec_strani = izlusci_stevilo_vseh_vprasanj_in_vseh_strani()[1]


def shrani_v_txt_datoteko(ime_txt_datoteke, html):
    """Funkcija HTML izbrane strani shrani v datoteko z želenim imenom"""
    with open(ime_txt_datoteke, "w", encoding="utf8") as f:
        f.write(html)
    return None


def shrani_vprasanja_v_seznam(stran):
    """Funkcija iz spletne strani potegne HTML in vprašanja na njem shrani v seznam"""
    vprasanja = []
    html_strani = requests.get(stran).text
    bloki = izlusci_bloke(html_strani)
    for blok in bloki:
        vprasanje = izlusci_podatke_iz_bloka(blok)
        vprasanja.append(vprasanje)
    return vprasanja


def naredi_CSV(ime_datoteke):
    """Funkcija naredi CSV datoteko in vanjo vpiše začetne podatke"""
    with open(ime_datoteke, "w", encoding="utf8") as dat:
        pisatelj = csv.writer(dat)
        pisatelj.writerow(
            [
                "Id",
                "Ime",
                "Opomba",
                "Oznake",
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


def shrani_vprasanja_v_CSV(ime_datoteke, stevilo_strani=najvec_strani, filter="Newest", vprasanja_na_stran="50"):
    """Funkcija v CSV datoteko z želenim imenom shrani informacije o vprašanjih.Lahko ji predpišemo koliko 
    strani s foruma želimo, če tega ne storimo, bo funkcija prensesla vse strani. Če delovanje funcije 
    prekinemo bo vseeno naredila CSV datoteko z do takrat prenesenimi stranmi"""
    filtri = ["newest", "active", "bounties",
              "unanswered", "frequent", "votes"]
    moznosti_vpr_na_stran = ["15", "30", "50"]
    try:
        if stevilo_strani > najvec_strani or filter.casefold() not in filtri or vprasanja_na_stran not in moznosti_vpr_na_stran:
            raise ValueError
        naredi_CSV(ime_datoteke)
        for stevilka_strani in range(1, stevilo_strani+1):
            vprasanja = shrani_vprasanja_v_seznam(
                f"https://math.stackexchange.com/questions?tab={filter}&page={stevilka_strani}&pagesize={vprasanja_na_stran}"
            )
            with open(ime_datoteke, "a", encoding="utf8") as datoteka:
                pisatelj = csv.writer(datoteka)
                for vprasanje in vprasanja:
                    pisatelj.writerow(
                        [
                            vprasanje["Id"],
                            vprasanje["Ime"],
                            vprasanje["Opomba"],
                            vprasanje["Oznake"],
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
            print(f"Shranjeno ({stevilka_strani}/{stevilo_strani})")
        print("CSV je bil uspešno shranjen.")
    except ValueError:
        print("Vnešeni podatko so napačni!")
        print(f"Vseh strani je le {najvec_strani}!")
        print("Možnosti za filter so:")
        for i in filtri:
            print(i.title())
        print("Možnosti za število vprašanj na stran pa so:")
        for j in moznosti_vpr_na_stran:
            print(j)
