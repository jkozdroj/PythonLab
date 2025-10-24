# -*- coding: utf-8 -*-
import re

def apply_casing(src: str, target: str) -> str:
    """Zachowuje styl liter dopasowanego slowa (src) w zastepniku (target)."""
    if src.isupper():
        return target.upper()
    if len(src) >= 2 and src[0].isupper() and src[1:].islower():
        return target.capitalize()
    return target

def replace_one_pair(text: str, old_word: str, new_word: str) -> str:
    """Zamienia JEDNA pare (old_word -> new_word) jako cale slowa, case-insensitive, z zachowaniem stylu."""
    if not old_word:
        return text  # brak slowa do zamiany

    pattern = r'\b' + re.escape(old_word) + r'\b'  # tylko cale slowa

    def repl(m: re.Match) -> str:
        src = m.group(0)
        return apply_casing(src, new_word)

    return re.sub(pattern, repl, text, flags=re.IGNORECASE)

if __name__ == "__main__":
    # --- ZAHARDKODOWANY TEKST ---
    tekst = (
        "Ala ma kota, a kot ma Ale. Koty sa piekne! "
        "W Warszawie pada deszcz, ale Ala nadal lubi spacery. "
        "Ala i kot to najlepsi przyjaciele."
    )

    print("=== TEKST WEJSCIOWY ===")
    print(tekst)
    print()

    # --- JEDNA PARA OD UZYTKOWNIKA ---
    old_w = input("Podaj STARE slowo: ").strip()
    new_w = input("Podaj NOWE slowo: ").strip()

    wynik = replace_one_pair(tekst, old_w, new_w)

    print("\n=== WYNIK ===")
    print(wynik)
