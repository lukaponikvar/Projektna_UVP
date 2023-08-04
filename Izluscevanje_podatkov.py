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
    vzorec_za_re = (r"""<div class="fs-body3 flex--item fl1 mr12 sm:mr0 sm:mb12">.+?"""
                    r"""(?P<Stevilo_objav>\d+(,\d+)*).+?questions.+?</div>""")
    stevilo = re.search(vzorec_za_re, vzorec.text, flags=re.DOTALL)
    strani = math.ceil(izlusci_stevilo(stevilo.group(1)) / 50)
    return (stevilo.group(1), strani)


def izlusci_bloke(niz):
    """Funkcija iz HTML datoteke izlušči blok z vsemi informacijami o nekem vprašanju s foruma."""
    vzorec = r"""<div id="question-summary-\d+" class="s-post-summary.*?(?:(?:>Community wiki)|(?:</span></time>))"""
    rezultat = re.findall(vzorec, niz, flags=re.DOTALL,)
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
        r"""<span class="s-post-summary--stats-item-number">(?P<votes>.+?)</span>.*?<span class="s-post-summary-"""
        r"""-stats-item-unit">.*?</span>.*?<div class="s-post-summary--stats-item( has-answers)?(?P<sprejet> has-accepted-answer)"""
        r"""?.*?<span class="s-post-summary--stats-item-number">(?P<answers>.+?)</span>.*?<span class="s-post-summary--stats-"""
        r"""item-unit">.*?</span>.*?<div class="s-post-summary--stats-item.*?" title="(?P<views>\d+) views?">.*?"""
        r"""<h3 class="s-post-summary--content-title">.*?<a href="/questions/\d*?/.*?" class="s-link">(?P<ime>.*?)"""
        r"""(?P<duplikat> \[duplicate\])?(?P<zaprto> \[closed\])?</a>.*?"""
        r"""<div class="s-post-summary--meta">.*?<div class="s-post-summary--meta-tags d-inline-block tags js-tags """
        r"""(?P<tag>(t-.*?)*?)">.*?"""
        r"""((<time class="s-user-card--time">asked <span title='(?P<date>.*?)Z?' class='relativetime'>"""
        r""".*?</span></time>)|(Community wiki))""",
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
    if najdba["date"]:
        vprasanje["Datum in ura"] = najdba["date"].strip()
    else:
        vprasanje["Datum in ura"] = None
    if najdba["sprejet"]:
        vprasanje["Sprejet odgovor"] = "Da"
    else:
        vprasanje["Sprejet odgovor"] = "Ne"
    return vprasanje
