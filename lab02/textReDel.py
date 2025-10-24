# -*- coding: utf-8 -*-
import re

def remove_words(text: str, words, case_sensitive: bool = False) -> str:
    """
    Usuwa z tekstu cale slowa z listy `words`.
    Przyklad: words = ["Ala", "kot"]
    """
    if not words:
        return text

    # zbuduj wyrazenie typu: r'\b(?:Ala|kot)\b'
    escaped = [re.escape(w) for w in words]
    pattern = r'\b(?:' + "|".join(escaped) + r')\b'
    flags = 0 if case_sensitive else re.IGNORECASE

    # usun dopasowania i posprzataj wielokrotne spacje
    out = re.sub(pattern, "", text, flags=flags)
    out = re.sub(r"\s{2,}", " ", out).strip()
    return out

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

    # --- WEJSCIE UZYTKOWNIKA ---
    line = input("Podaj slowo(a) do usuniecia (po przecinku): ").strip()
    slowa = [w.strip() for w in line.split(",") if w.strip()]

    # --- PRZETWARZANIE ---
    wynik = remove_words(tekst, slowa)

    print("\n=== WYNIK ===")
    print(wynik)
