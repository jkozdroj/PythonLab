
def remove_one_word_no_re(text: str, word_to_remove: str) -> str:

    if not word_to_remove:
        return text

    tokens = text.split()
    kept = []

    for token in tokens:

        prefix = ''
        suffix = ''
        core = token

        while core and not core[0].isalnum():
            prefix += core[0]
            core = core[1:]
        while core and not core[-1].isalnum():
            suffix = core[-1] + suffix
            core = core[:-1]


        if core and core.lower() == word_to_remove.lower():
            continue

        kept.append(token)

    return " ".join(kept)

if __name__ == "__main__":

    tekst = (
        "Ala ma kota, a kot ma Ale. Koty sa piekne! "
        "W Warszawie pada deszcz, ale Ala nadal lubi spacery. "
        "Ala i kot to najlepsi przyjaciele."
    )

    print("=== TEKST WEJSCIOWY ===")
    print(tekst)
    print()

    old_w = input("Podaj slowo do usuniecia: ").strip()

    wynik = remove_one_word_no_re(tekst, old_w)

    print("\n=== WYNIK ===")
    print(wynik)
