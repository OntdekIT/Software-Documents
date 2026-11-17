"""De bouwstenen van een document.

Een document is een lijst van blokken. Elk blok is een klein, simpel object
(geen markdown). De renderlaag (`render.py`) weet hoe elk blok op papier komt.
Zo staat de inhoud los van de opmaak: je verandert hier de tekst, niet de
PDF-code.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Meta:
    """De kop van een document: titel, ondertitel en losse kop-gegevens."""

    titel: str
    ondertitel: str = ""
    # Vrije sleutel/waarde-regels rechtsboven in de kop (klant, datum, nummer).
    # Bijvoorbeeld [("Klant", "McVerspil"), ("Datum", "2026-09-24")].
    kopregels: list[tuple[str, str]] = field(default_factory=list)


@dataclass
class Heading:
    """Een kop binnen het document. niveau 1 = hoofdstuk, 2 = subkop."""

    tekst: str
    niveau: int = 1


@dataclass
class Para:
    """Een gewone alinea. **vet** mag met dubbele sterren."""

    tekst: str


@dataclass
class Bullets:
    """Een opsomming. Elk item mag **vet** bevatten."""

    items: list[str]


@dataclass
class Table:
    """Een tabel met een koprij en daarna de gegevens.

    uitlijning is een lijst per kolom: "links" (standaard) of "rechts"
    (bijvoorbeeld voor bedragen). Laat leeg voor alles links.

    kolombreedtes is een lijst relatieve gewichten per kolom, bijvoorbeeld
    [1, 8, 2]. Laat leeg voor gelijke breedtes.
    """

    kop: list[str]
    rijen: list[list[str]]
    uitlijning: list[str] = field(default_factory=list)
    kolombreedtes: list[float] = field(default_factory=list)


@dataclass
class Total:
    """Een uitgelichte totaalregel (label links, bedrag rechts, in accent)."""

    label: str
    bedrag: str


@dataclass
class Code:
    """Een stukje code of een schema, in een kader met vaste breedte."""

    tekst: str
    onderschrift: str = ""


@dataclass
class Note:
    """Een uitgelicht kader, bv. een belangrijke opmerking of samenvatting."""

    tekst: str
    kop: str = "Kort gezegd"


@dataclass
class Image:
    """Een afbeelding uit een bestand: een logo, foto of grafiek.

    pad mag absoluut zijn of relatief aan de werkmap. Standaard op de tekstbreedte
    geschaald; geef breedte_mm voor een vaste breedte. uitlijning kan "links",
    "midden" of "rechts".
    """

    pad: str
    onderschrift: str = ""
    max_hoogte_mm: float = 130.0
    breedte_mm: float | None = None
    uitlijning: str = "midden"
    kader: bool = False


@dataclass
class Spacer:
    """Wat extra witruimte."""

    hoogte: int = 6


@dataclass
class Document:
    """Een compleet document: de kop plus alle blokken."""

    meta: Meta
    blokken: list[object] = field(default_factory=list)
    bestandsnaam: str = ""  # zonder .pdf; wordt van de titel afgeleid als leeg
    voettekst: str = ""  # overschrijft de merk-voettekst als gezet
