from Tekstovni_vmesnik import pozdrav, ponudi_moznosti, zakljuci_izvajanje
from Analiza import zacni


def tekstovni_vmesnik():
    pozdrav()
    moznost = ponudi_moznosti(
        [
            [zacni, "Začni z analizo"],
            [zakljuci_izvajanje, "Končaj z izvajanjem"],
        ]
    )
    return moznost()


tekstovni_vmesnik()
