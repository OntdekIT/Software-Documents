"""docgen: een kleine, zelfstandige PDF-documentbouwer in de huisstijl van de app.

De inhoud staat los
van de opmaak: je bouwt een `Document` uit blokken (`blocks`) en `render_pdf`
zet het om naar een verzorgde PDF (`render`), in de huisstijl uit `theme`.

Huisregel: nooit een em-dash of
en-dash. De build faalt hard als er een in de tekst staat.
"""

from __future__ import annotations

from .blocks import (
    Bullets,
    Code,
    Document,
    Heading,
    Image,
    Meta,
    Note,
    Para,
    Spacer,
    Table,
    Total,
)
from .render import render_pdf

__all__ = [
    "Bullets",
    "Code",
    "Document",
    "Heading",
    "Image",
    "Meta",
    "Note",
    "Para",
    "Spacer",
    "Table",
    "Total",
    "render_pdf",
]
