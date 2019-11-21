from re import sub, findall


def fraction_lowercase(s):
    return "{}/{}".format(len(findall(r"([a-z])", s)), len(s))


def printer_error(s):
    return "{}/{}".format(len(sub("[a-m]", '', s)), len(s))




print(fraction_lowercase("aAiIeEOouU"))
