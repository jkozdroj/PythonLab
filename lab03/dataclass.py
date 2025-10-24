from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import re


@dataclass
class Osoba:
    imie: str
    nazwisko: str
    adres: str
    kod_pocztowy: str 
    pesel: str
    def __post_init__(self):
        if not re.fullmatch(r"\d{11}", self.pesel):
            raise ValueError("PESEL musi składać się z 11 cyfr.")
        if not re.fullmatch(r"\d{2}-\d{3}", self.kod_pocztowy):
            raise ValueError("Kod pocztowy musi mieć format NN-NNN (np. 00-001).")

    # --- Serializacja ---
    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, *, ensure_ascii: bool = False, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=ensure_ascii, indent=indent)

    def to_file(self, path: str | Path, *, ensure_ascii: bool = False, indent: int = 2) -> None:
        p = Path(path)
        p.write_text(self.to_json(ensure_ascii=ensure_ascii, indent=indent), encoding="utf-8")

    # --- Deserializacja ---
    @classmethod
    def from_dict(cls, data: dict) -> "Osoba":
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "Osoba":
        data = json.loads(json_str)
        return cls.from_dict(data)

    @classmethod
    def from_file(cls, path: str | Path) -> "Osoba":
        p = Path(path)
        data = json.loads(p.read_text(encoding="utf-8"))
        return cls.from_dict(data)


# --- Przykładowe użycie ---
if __name__ == "__main__":
    osoba = Osoba(
        imie="Jan",
        nazwisko="Kowalski",
        adres="ul. Fajna 1, 00-001 Warszawa",
        kod_pocztowy="00-001",
        pesel="90010112345",
    )

    js = osoba.to_json()
    print(js)

    osoba2 = Osoba.from_json(js)
    print(osoba2)

    osoba.to_file("osoba.json")
    osoba3 = Osoba.from_file("osoba.json")
    print(osoba3)
