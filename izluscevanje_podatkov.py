import re
import math
import requests


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
    model = r"""<div id="question-summary-\d+" class="s-post-summary    js-post-summary" data-post-id="\d+" data-post-type-id="1">.*?<time class="s-user-card--time">asked <span title='.+?' class='relativetime'>.*?</span></time>.*?</div>.*?</div>.*?</div>.*?</div>"""
    rezultat = re.findall(model, tekst, flags=re.DOTALL)
    return rezultat


def izlusci_podatke(blok):
    vprašanje = {}

    # izluscimo id
    vzorec_id = re.compile(
        r"""<div id="question-summary-(?P<id>\d+)" class="s-post-summary""",
        re.DOTALL
    )
    vprašanje["id"] = vzorec_id.findall(blok)[0]

    # izluscimo ime
    vzorec_ime = re.compile(
        r"""<h3 class="s-post-summary--content-title">.*?<a href="/questions/\d*?/.*?" class="s-link">(?P<ime>.*?)</a>""",
        re.DOTALL
    )
    najdba_ime = vzorec_ime.search(blok)
    vprašanje["ime"] = najdba_ime["ime"].strip()

    # izluscimo tags
    vzorec_tags = re.compile(
        r"""<div class="s-post-summary--meta">.*?<div class="s-post-summary--meta-tags d-inline-block tags js-tags (?P<tag>(t-.*?)*?)">""",
        re.DOTALL
    )
    najdba_tags = vzorec_tags.search(blok)
    vprašanje["tags"] = najdba_tags["tag"]

    # izluscimo votes, answers, views
    vzorec_vav = re.compile(
        r"""<span class="s-post-summary--stats-item-number">(?P<votes>.+?)</span>.*?<span class="s-post-summary--stats-item-unit">.*?</span>.*?<span class="s-post-summary--stats-item-number">(?P<answers>.+?)</span>.*?<span class="s-post-summary--stats-item-unit">.*?</span>.*?<span class="s-post-summary--stats-item-number">(?P<views>.+?)</span>.*?<span class="s-post-summary--stats-item-unit">.*?</span>""",
        re.DOTALL
    )
    najdba_vav = vzorec_vav.search(blok)
    vprašanje["glasovi"] = najdba_vav["votes"]
    vprašanje["odgovori"] = najdba_vav["answers"]
    vprašanje["ogledi"] = najdba_vav["views"]

    # izluscimo datum in uro
    vzorec_dat = re.compile(
        r"""<time class="s-user-card--time">asked <span title='(?P<dat>.*?)' class='relativetime'>.*?</span></time>""",
        re.DOTALL
    )
    najdba_dat = vzorec_dat.search(blok)
    vprašanje["datum in čas objave"] = najdba_dat["dat"]

    return vprašanje
