#!/usr/bin/env python3
"""Bouw een documentmodule naar een PDF in de huisstijl van de app.

Gebruik:
    python3 build.py <module.py> [--uit <pad.pdf>]

Een documentmodule is een klein Python-bestand met een functie `document()`
die een `docgen.Document` teruggeeft (zie de recepten in documenttypes/ en de
voorbeelden in voorbeelden/). Dit bestand laadt die module, bouwt het document
en schrijft de PDF. De bestandsnaam komt van de titel als je geen --uit geeft.

De docgen-engine (blocks, render, theme) staat naast dit bestand; het pad wordt
automatisch toegevoegd, dus je kunt dit overal draaien.

Enige afhankelijkheid: reportlab  (pip install reportlab)
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

# Zorg dat het docgen-pakket naast dit bestand importeerbaar is, waar je ook draait.
BOUW_DIR = Path(__file__).resolve().parent
if str(BOUW_DIR) not in sys.path:
    sys.path.insert(0, str(BOUW_DIR))

from docgen import Document, render_pdf  # noqa: E402


def _veilige_naam(titel: str) -> str:
    naam = re.sub(r"[^\w\s-]", "", titel).strip()
    naam = re.sub(r"\s+", " ", naam)
    return naam or "document"


def _laad_module(pad: Path):
    spec = importlib.util.spec_from_file_location("docmodule", pad)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Kan module niet laden: {pad}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "document"):
        raise SystemExit(f"{pad} heeft geen functie document().")
    return mod


def main() -> None:
    p = argparse.ArgumentParser(description="Bouw een documentmodule naar PDF.")
    p.add_argument("module", help="pad naar een .py met een document()-functie")
    p.add_argument("--uit", help="pad voor de PDF (standaard: de titel .pdf)")
    args = p.parse_args()

    modpad = Path(args.module).resolve()
    if not modpad.exists():
        raise SystemExit(f"Bestaat niet: {modpad}")

    mod = _laad_module(modpad)
    doc: Document = mod.document()

    if args.uit:
        uit = Path(args.uit).resolve()
    else:
        naam = doc.bestandsnaam or _veilige_naam(doc.meta.titel)
        uit = modpad.parent / f"{naam}.pdf"

    uit.parent.mkdir(parents=True, exist_ok=True)
    render_pdf(doc, str(uit))
    print(f"PDF gebouwd: {uit}")


if __name__ == "__main__":
    main()
