import re
import math
import requests

prvotni_url_naslov = "https://math.stackexchange.com/questions"


def izlusci_stevilo(niz):
    stevilo = ""
    for i in niz:
        if i != ",":
            stevilo += i
    return int(stevilo)


def izlusci_stevilo_vseh_strani_in_vprasanj():
    vzorec = requests.get(prvotni_url_naslov)
    vzorec_za_re = r"""<div class="fs-body3 flex--item fl1 mr12 sm:mr0 sm:mb12">.+?(?P<Stevilo_objav>\d+(,\d+)*).+?questions.+?</div>"""
    stevilo = re.search(vzorec_za_re, vzorec.text, flags=re.DOTALL)
    strani = math.ceil(izlusci_stevilo(stevilo.group(1)) / 50)
    return (stevilo.group(1), strani)


def izlusci_bloke(tekst):
    model = r"""<div id="question-summary-\d+" class="s-post-summary.*?</span></time>.*?</div>.*?</div>"""
    rezultat = re.findall(model, tekst, flags=re.DOTALL)
    return rezultat


def izlusci_podatke1(blok):
    vprasanje = {}
    vzorec = re.compile(
        r"""<div id="question-summary-(?P<id>\d+)" class="s-post-summary.*?"""
        r"""<span class="s-post-summary--stats-item-number">(?P<votes>.+?)</span>.*?<span class="s-post-summary--stats-item-unit">.*?</span>.*?<span class="s-post-summary--stats-item-number">(?P<answers>.+?)</span>.*?<span class="s-post-summary--stats-item-unit">.*?</span>.*?<span class="s-post-summary--stats-item-number">(?P<views>.+?)</span>.*?<span class="s-post-summary--stats-item-unit">.*?</span>.*?"""
        r"""<h3 class="s-post-summary--content-title">.*?<a href="/questions/\d*?/.*?" class="s-link">(?P<ime>.*?)</a>.*?"""
        r"""<div class="s-post-summary--meta">.*?<div class="s-post-summary--meta-tags d-inline-block tags js-tags (?P<tag>(t-.*?)*?)">.*?"""
        r"""<time class="s-user-card--time">asked <span title='(?P<dat>.*?)' class='relativetime'>.*?</span></time>""",
        re.DOTALL
    )
    najdba = vzorec.search(blok)
    vprasanje["id"] = najdba["id"]
    vprasanje["ime"] = najdba["ime"].strip()
    vprasanje["tags"] = najdba["tag"].strip()
    vprasanje["glasovi"] = najdba["votes"].strip()
    vprasanje["odgovori"] = najdba["answers"].strip()
    vprasanje["ogledi"] = najdba["views"].strip()
    vprasanje["datum in čas objave"] = najdba["dat"].strip()
    return vprasanje
