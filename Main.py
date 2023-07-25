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


blokec = """<div id="question-summary-4742111" class="s-post-summary    js-post-summary" data-post-id="4742111" data-post-type-id="1">
    <div class="s-post-summary--stats js-post-summary-stats">
        <div class="s-post-summary--stats-item s-post-summary--stats-item__emphasized" title="Score of 1">
            <span class="s-post-summary--stats-item-number">1</span>
            <span class="s-post-summary--stats-item-unit">vote</span>
        </div>
        <div class="s-post-summary--stats-item has-answers " title="2 answers">
            <span class="s-post-summary--stats-item-number">2</span>
            <span class="s-post-summary--stats-item-unit">answers</span>
        </div>
        <div class="s-post-summary--stats-item " title="52 views">
            <span class="s-post-summary--stats-item-number">52</span>
            <span class="s-post-summary--stats-item-unit">views</span>
        </div>



    </div>
    <div class="s-post-summary--content">


        <h3 class="s-post-summary--content-title">
            <a href="/questions/4742111/prove-left-sum-i-1na-ix-i2-right-left-sum-i-1n-a-iy-i-right-geq-le" class="s-link">Prove: $\left(\sum_{i=1}^na_ix_i^2\right)\left(\sum_{i=1}^n a_iy_i\right)\geq\left(\sum_{i=1}^n a_ix_i\right)\left(\sum_{i=1}^n a_ix_iy_i\right)$</a>
        </h3>
            <div class="s-post-summary--content-excerpt">
                I've been struggling with the following inequality, perhaps because it is not always true after all. Let $(a_1,\dots,a_n)$, $(x_1,\dots,x_n)$, and $(y_1,\dots,y_n)$ be non-negative real numbers. Can ...
            </div>
        <div class="s-post-summary--meta">
            <div class="s-post-summary--meta-tags d-inline-block tags js-tags t-inequality t-holder-inequality">

<ul class='ml0 list-ls-none js-post-tag-list-wrapper d-inline'><li class='d-inline mr4 js-post-tag-list-item'><a href="/questions/tagged/inequality" class="post-tag flex--item mt0 js-tagname-inequality" title="show questions tagged &#39;inequality&#39;" aria-label="show questions tagged &#39;inequality&#39;" rel="tag" aria-labelledby="tag-inequality-tooltip-container">inequality</a></li><li class='d-inline mr4 js-post-tag-list-item'><a href="/questions/tagged/holder-inequality" class="post-tag flex--item mt0 js-tagname-holder-inequality" title="show questions tagged &#39;holder-inequality&#39;" aria-label="show questions tagged &#39;holder-inequality&#39;" rel="tag" aria-labelledby="tag-holder-inequality-tooltip-container">holder-inequality</a></li></ul>
            </div>
            


<div class="s-user-card s-user-card__minimal" aria-live="polite">

                <a href="/users/406002/nathan-l" class="s-avatar s-avatar__16 s-user-card--avatar" data-user-id="406002">        <div class="gravatar-wrapper-16">
            <img src="https://www.gravatar.com/avatar/c59a3e27b2e1683c7f9741f89110c9e1?s=32&amp;d=identicon&amp;r=PG&amp;f=y&amp;so-version=2" alt="Nathan L&#39;s user avatar" width="16" , height="16" class="s-avatar--image" />
        </div>
</a>

    <div class="s-user-card--info">
            <div class="s-user-card--link d-flex gs4" >
                <a href="/users/406002/nathan-l" class="flex--item">Nathan L</a>
            </div>
        
                <ul class="s-user-card--awards">
            <li class="s-user-card--rep"><span class="todo-no-class-here" title="reputation score " dir="ltr">97</span></li>

        </ul>

        
    </div>

        <time class="s-user-card--time">asked <span title='2023-07-25 09:36:33Z' class='relativetime'>2 hours ago</span></time>
</div>

        </div>
       
    </div>
</div>"""


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
        r"""<h3 class="s-post-summary--content-title">
            <a href="/questions/\d*?/.*?" class="s-link">(?P<ime>.*?)</a>
        </h3>""",
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

    return vprašanje


print(izlusci_podatke(blokec))
