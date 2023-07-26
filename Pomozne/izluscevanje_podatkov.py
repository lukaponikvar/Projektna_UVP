import re
import math
import requests


def izlusci_stevilo(niz):
    """Funkcija iz niza oblike "1,234,567" izlušči število"""
    stevilo = ""
    for i in niz:
        if i != ",":
            stevilo += i
    return int(stevilo)


def izlusci_stevilo_vseh_vprasanj_in_vseh_strani():
    """Funkcija vrne nabor števila vseh vprašanj in števila vseh strani."""
    vzorec = requests.get(f"https://math.stackexchange.com/questions?")
    vzorec_za_re = r"""<div class="fs-body3 flex--item fl1 mr12 sm:mr0 sm:mb12">.+?(?P<Stevilo_objav>\d+(,\d+)*).+?questions.+?</div>"""
    stevilo = re.search(vzorec_za_re, vzorec.text, flags=re.DOTALL)
    strani = math.ceil(izlusci_stevilo(stevilo.group(1)) / 50)
    return (stevilo.group(1), strani)


def izlusci_bloke(niz):
    """Funkcija iz HTML datoteke izlušči blok z vsemi informacijami o nekem vprašanju s foruma."""
    vzorec = r"""<div id="question-summary-\d+" class="s-post-summary.*?</span></time>.*?</div>.*?</div>"""
    rezultat = re.findall(vzorec, niz, flags=re.DOTALL)
    return rezultat


def izlusci_oznake(neobdelan_tag):
    """Funkcija iz niza, ki vsebuje oznake naredi seznam oznak."""
    tags = neobdelan_tag.strip().split(" ")
    return [tag[2:] for tag in tags]


def izlusci_podatke_iz_bloka(blok):
    """Funkcija iz bloka izlusci vse pomembne informacije o vprašanju in ga vrne kot slovar."""
    vprasanje = {}
    vzorec = re.compile(
        r"""<div id="question-summary-(?P<id>\d+)" class="s-post-summary.*?"""
        r"""<span class="s-post-summary--stats-item-number">(?P<votes>.+?)</span>.*?<span class="s-post-summary--stats-item-unit">.*?</span>.*?<div class="s-post-summary--stats-item( has-answers)?(?P<sprejet> has-accepted-answer)?.*?<span class="s-post-summary--stats-item-number">(?P<answers>.+?)</span>.*?<span class="s-post-summary--stats-item-unit">.*?</span>.*?<span class="s-post-summary--stats-item-number">(?P<views>.+?)</span>.*?<span class="s-post-summary--stats-item-unit">.*?</span>.*?"""
        r"""<h3 class="s-post-summary--content-title">.*?<a href="/questions/\d*?/.*?" class="s-link">(?P<ime>.*?)(?P<duplikat> \[duplicate\])?(?P<zaprto> \[closed\])?</a>.*?"""
        r"""<div class="s-post-summary--meta">.*?<div class="s-post-summary--meta-tags d-inline-block tags js-tags (?P<tag>(t-.*?)*?)">.*?"""
        r"""<time class="s-user-card--time">asked <span title='(?P<date>.*?)Z?' class='relativetime'>.*?</span></time>""",
        re.DOTALL
    )
    najdba = vzorec.search(blok)
    vprasanje["Id"] = najdba["id"]
    vprasanje["Ime"] = najdba["ime"].strip()
    if najdba["duplikat"]:
        vprasanje["Opomba"] = "Duplikat"
    elif najdba["zaprto"]:
        vprasanje["Opomba"] = "Zaprt"
    else:
        vprasanje["Opomba"] = "Odprt"
    vprasanje["Oznake"] = izlusci_oznake(najdba["tag"])
    vprasanje["Glasovi"] = najdba["votes"].strip()
    vprasanje["Odgovori"] = najdba["answers"].strip()
    vprasanje["Ogledi"] = najdba["views"].strip()
    vprasanje["Leto"] = najdba["date"].strip().split(" ")[0].split("-")[0]
    vprasanje["Mesec"] = najdba["date"].strip().split(" ")[0].split("-")[1]
    vprasanje["Dan"] = najdba["date"].strip().split(" ")[0].split("-")[2]
    vprasanje["Ura"] = najdba["date"].strip().split(" ")[1]
    if najdba["sprejet"]:
        vprasanje["Sprejet odgovor"] = "Da"
    else:
        vprasanje["Sprejet odgovor"] = "Ne"
    return vprasanje
