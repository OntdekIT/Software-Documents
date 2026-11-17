"""De huisstijl van de app (MB Ontdekt / ClimateChecker), op een plek.

Kleuren, lettertypes en de logo-tekening. Alles wat het "gezicht" van de PDF
bepaalt staat hier, zodat een stijlwijziging op een plek gebeurt.
"""

from __future__ import annotations

from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm

# --- Kleuren (de merkkleuren van de app) ---
INKT = HexColor("#111827")  # inkt, zoals in de app
ACCENT = HexColor("#fecb3d")  # amber, de merkkleur van de app
# Donkerder magenta voor kleine accent-tekst (subkoppen, labels). Haalt WCAG-AA.
ACCENT_TEKST = HexColor("#8a6408")  # donker amber (brand-800), AA op wit
GRIJS = HexColor("#4b5563")  # rustige tekstkleur voor bijschriften
LICHTGRIJS = HexColor("#9aa1ab")
LIJN = HexColor("#e5e7eb")  # dunne scheidingslijnen
KADER_VUL = HexColor("#fff9e6")  # lichte amber-zweem voor notities
CODE_VUL = HexColor("#f6f7f9")  # grijs vlak achter code
CODE_LIJN = HexColor("#e2e5ea")
TABEL_KOP = HexColor("#111827")
TABEL_STREEP = HexColor("#f7f7f9")  # om-en-om rijkleur

# --- Lettertypes (ingebouwd in reportlab, geen extra bestanden nodig) ---
FONT = "Helvetica"
FONT_VET = "Helvetica-Bold"
FONT_CURSIEF = "Helvetica-Oblique"
FONT_CODE = "Courier"

# --- Pagina ---
MARGE_LINKS = 22 * mm
MARGE_RECHTS = 22 * mm
MARGE_BOVEN = 26 * mm
MARGE_ONDER = 20 * mm

# --- Merk-teksten ---
MERK_NAAM_1 = "MB"
MERK_NAAM_2 = " Ontdekt"

# De voettekst is niet vast: elk documenttype/build kan hem zetten. Standaard
# alleen het merk, zodat de engine generiek blijft.
VOETTEKST = "MB Ontdekt - ClimateChecker"


def bouwdatum() -> str:
    """De datum van vandaag als YYYY-MM-DD, voor de voettekst."""
    from datetime import date

    return date.today().isoformat()


def teken_logo(canvas, x, y, schaal=1.0):
    """Tekent het merk van de app: amber badge met inkttekst (zoals de navbar).

    Vectortekening, geen plaatje. y is de basislijn van de tekst.
    """
    grootte = 13 * schaal
    tekst = MERK_NAAM_1 + MERK_NAAM_2
    breedte = canvas.stringWidth(tekst, FONT_VET, grootte)
    pad = 5 * schaal
    canvas.setFillColor(ACCENT)
    canvas.roundRect(x - pad, y - 4 * schaal, breedte + 2 * pad, grootte + 5 * schaal, 4 * schaal, stroke=0, fill=1)
    canvas.setFillColor(INKT)
    canvas.setFont(FONT_VET, grootte)
    canvas.drawString(x, y, tekst)
    return breedte
