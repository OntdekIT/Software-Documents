"""02 Leeswijzer: de weg door de hele documentenset van MB Ontdekt."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from opmaak import DATUM, DIAG, Bullets, Heading, Para, Table, bronnenblok  # noqa: E402
from docgen import Document, Image, Meta, Note  # noqa: E402

from documentenset import LEESROUTES, SET, genummerd  # noqa: E402

TITELS = {nr: t for nr, t, *_ in SET}


def document() -> Document:
    op_nr = sorted(SET, key=lambda x: x[0])
    b = [
        Para("Deze documentatieset beschrijft MB Ontdekt (ClimateChecker): de webapplicatie die de metingen van de "
             "meetstations van Ontdekstation en Bibliotheek Midden-Brabant toont. De set bestaat uit 21 documenten. Dit "
             "document wijst de weg: hoe de set is geordend, waar je begint en wat je waar vindt."),
        Heading("Hoe het is geordend", 1),
        Para("De documenten zijn genummerd 01 tot 21 en in vijf groepen verdeeld. De PDF-bestandsnaam is de titel zonder "
             "nummer, bijvoorbeeld Overzicht.pdf. In de rest van de set verwijzen we naar een document bij die titel."),
        Image(str(DIAG / "leeswijzer" / "set.png"), onderschrift="De 21 documenten in vijf groepen. Bron: de vaste lijst van de set; "
              "het diagram en de tabel hieronder komen uit dezelfde lijst.", max_hoogte_mm=95),
        Heading("Alle documenten", 1),
        Table(kop=["Nr", "Document", "Voor wie", "Wat je erin vindt"],
              rijen=[[f"{nr:02d}", t, wie, wat] for nr, t, _g, wie, wat in op_nr],
              kolombreedtes=[1, 5, 4, 8]),
        Heading("Waar je begint", 1),
        Para("Begin altijd met het Overzicht: dat legt in gewone taal uit wat de app is en voor wie. Daarna hangt de "
             "route af van wat je wilt weten."),
        Table(kop=["Jij bent", "Leesroute"], rijen=[
            [wie, " > ".join(genummerd(n, TITELS[n]) for n in route)] for wie, route in LEESROUTES
        ], kolombreedtes=[3, 10]),
        Heading("Wat opvalt in de set", 1),
        Bullets([
            "**Gebaseerd op de code.** De diagrammen zijn waar mogelijk afgeleid uit de broncode, configuratie en "
            "database, en elk diagram heeft een onderschrift met 'Bron:' en de commit. Wat niet vast te stellen was staat als 'onduidelijk'.",
            "**Bronnen en controle.** Elk document sluit af met een kop 'Bronnen en controle': de gebruikte bronnen, de "
            "commits, de datum en wat onduidelijk bleef.",
            "**Peildatum.** De set is gemaakt op 2026-11-17 uit de branch s3nj26_dev van de backend en de frontend.",
            "**Oudere documenten.** De mappen s3nj22 tot en met s3vj24 in de repository zijn historisch; waar ze afwijken van de code, wint de code.",
            "**Taal en stijl.** Alles is Nederlands; de kleuren (amber en inkt) zijn die van de app.",
        ]),
        Note("Zoek je iets specifieks? Een scherm of handeling staat in de Gebruikershandleiding, een begrip in de Woordenlijst, "
             "een endpoint in het API-document en een keuze met afweging in Architectuurbeslissingen.", kop="Tip"),
    ]
    b += bronnenblok([
        "De vaste lijst van 21 documenten en de leesroutes.",
        "Titels en nummers volgen de afspraak van de documentenset; de inhoud van de andere documenten is hier alleen samengevat.",
    ], [
        "Of alle 21 documenten tegelijk zijn opgeleverd, is op het moment van schrijven niet vast te stellen; de beschrijvingen "
        "per document zijn de bedoeling van het document, niet een controle van de inhoud.",
        "De leesroutes zijn een voorstel van de schrijvers en geen eis uit de code.",
    ])
    return Document(meta=Meta("Leeswijzer", "Hoe de documentatie is opgebouwd en waar je begint.", [("Datum", DATUM)]),
                    blokken=b, voettekst="MB Ontdekt · leeswijzer")
