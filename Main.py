import re
import requests
import math
# Pridobimo najprej naše podatke

prvotni_url_naslov = "https://math.stackexchange.com/questions"


def shrani_v_txt_datoteko(ime_txt_datoteke, html):
    with open(ime_txt_datoteke, "w", encoding="utf8") as f:
        f.write(html)
    return None


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


def izlusci_bloke():
    model = r"""<div id="question-summary-\d+" class="s-post-summary    js-post-summary" data-post-id="\d+" data-post-type-id="1">.*?<time class="s-user-card--time">asked <span title='.+?' class='relativetime'>.*?</span></time>.*?</div>.*?</div>.*?</div>.*?</div>"""
    with open("micka", "r", encoding="utf8") as f:
        tekst = f.read()
    rezultat = re.findall(model, tekst, flags=re.DOTALL)
    return rezultat


# def izlusci_podatke(blok):
