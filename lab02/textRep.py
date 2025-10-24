

def apply_casing(src: str, target: str) -> str:

    if src.isupper():
        return target.upper()
    if len(src) >= 2 and src[0].isupper() and src[1:].islower():
        return target.capitalize()
    return target

def replace_one_pair_no_re(text: str, old_word: str, new_word: str) -> str:

    words = text.split()
    result = []
    for w in words:
        prefix = ''
        suffix = ''
        core = w


        while core and not core[0].isalnum():
            prefix += core[0]
            core = core[1:]
        while core and not core[-1].isalnum():
            suffix = core[-1] + suffix
            core = core[:-1]

        if core.lower() == old_word.lower():
            new_word_cased = apply_casing(core, new_word)
            result.append(prefix + new_word_cased + suffix)
        else:
            result.append(w)
    return " ".join(result)

if __name__ == "__main__":

    tekst = (
        "Ala ma kota, a kot ma Ale. Koty sa piekne! "
        "W Warszawie pada deszcz, ale Ala nadal lubi spacery. "
        "Ala i kot to najlepsi przyjaciele."
    )

    print("=== TEKST WEJSCIOWY ===")
    print(tekst)
    print()

    old_w = input("Podaj STARE slowo: ").strip()
    new_w = input("Podaj NOWE slowo: ").strip()

    wynik = replace_one_pair_no_re(tekst, old_w, new_w)

    print("\n=== WYNIK ===")
    print(wynik)
