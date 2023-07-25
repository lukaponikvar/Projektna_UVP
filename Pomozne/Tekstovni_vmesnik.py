def pozdrav():
    print("Pozdravljeni v programu za analizo!")


def preberi_stevilo():
    while True:
        vnos = input("> ")
        try:
            return int(vnos)
        except ValueError:
            print("Vnesti morate število")


def ponudi_moznosti(seznam_moznosti):
    print("Prosim izberite eno od naslednjih moznosti")
    for i, (_moznost, opis) in enumerate(seznam_moznosti, 1):
        print(f"{i}) {opis}")
    while True:
        i = preberi_stevilo()
        if 1 <= i <= len(seznam_moznosti):
            moznost = seznam_moznosti[i-1]
            return moznost[0]
        else:
            print(f"vnesti morate število med 1 in {len(seznam_moznosti)}.")


def zakljuci_izvajanje():
    print("Nasvidenje.")
    exit()


def zacni():
    print("Spoštovani, analiza Vas čaka v mapi Analiza.")


def tekstovni_vmesnik():
    pozdrav()
    moznost = ponudi_moznosti(
        [
            [zacni, "Začni z analizo"],
            [zakljuci_izvajanje, "Končaj z izvajanjem"],
        ]
    )
    return moznost()
