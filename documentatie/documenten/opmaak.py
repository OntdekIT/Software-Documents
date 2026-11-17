"""Gedeelde opmaak voor de documenten 01, 02, 19 en 20 (bronnen, schermafbeeldingen, bronnenblok)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIAG = ROOT / "diagrammen"
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / "bouw"))

from docgen import Bullets, Heading, Para, Table  # noqa: E402

DATUM = "2026-11-17"
SCHERMEN = DIAG / "wireframes-en-schermen" / "png"
SHA_BE = "e104152e572449be91d75b1d86a3bcecd6d4f5d0"
SHA_FE = "13fc1e2f086ea4c2c52c37188294b6e3921bfebd"


def sha_be() -> str:
    return SHA_BE


def sha_fe() -> str:
    return SHA_FE


def schermpad(naam: str) -> str:
    return str(SCHERMEN / f"{naam}.png")


def diagram(map_: str, naam: str) -> str:
    return str(DIAG / map_ / f"{naam}.png")


def bron_regel() -> str:
    return f"commit backend {SHA_BE[:7]}, frontend {SHA_FE[:7]}"


def bronnenblok(bronnen: list[str], onduidelijk: list[str]) -> list:
    """Het vaste afsluitende blok 'Bronnen en controle'."""
    return [
        Heading("Bronnen en controle", 1),
        Para(f"Datum van controle: {DATUM}. Alle beweringen in dit document komen uit de onderstaande bronnen; "
             "wat niet vast te stellen was staat bij 'Onduidelijk'."),
        Table(kop=["Bron", "Versie"], rijen=[
            ["Backend: OntdekIT/Software-BackEnd, branch s3nj26_dev", SHA_BE],
            ["Frontend: OntdekIT/Software-FrontEnd, branch s3nj26_dev", SHA_FE],
        ], kolombreedtes=[3, 4]),
        Heading("Gebruikte bronnen", 2),
        Bullets(bronnen),
        Heading("Onduidelijk of niet vast te stellen", 2),
        Bullets(onduidelijk or ["Niets bijzonders."]),
    ]
