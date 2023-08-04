def prevedi(str):
    """Prevede ime dneva v tednu iz angleščine v slovenščino."""
    if str == "Monday":
        return "Ponedeljek"
    if str == "Tuesday":
        return "Torek"
    if str == "Wednesday":
        return "Sreda"
    if str == "Thursday":
        return "Četrtek"
    if str == "Friday":
        return "Petek"
    if str == "Saturday":
        return "Sobota"
    if str == "Sunday":
        return "Nedelja"
    else:
        return str
