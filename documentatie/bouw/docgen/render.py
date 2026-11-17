"""De renderlaag: van blokken naar een verzorgde PDF.

Deze module weet als enige iets van reportlab. Ze zet een `Document` (kop +
blokken) om naar een PDF met logo, koptekst, voettekst en paginanummers in de
huisstijl uit `theme.py`. Bewust compact gehouden: geen inhoudsopgave of
diagram-machinerie, want zakelijke documenten (offerte, factuur, brief) hebben
die niet nodig. De em-dash-huisregel is wel overgenomen.
"""

from __future__ import annotations

from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Table as PTable,
    TableStyle,
)
from reportlab.platypus import (
    Image as PImage,
)
from reportlab.platypus import (
    Spacer as PSpacer,
)

from . import theme
from .blocks import (
    Bullets,
    Code,
    Document,
    Heading,
    Image,
    Note,
    Para,
    Spacer,
    Table,
    Total,
)

# ---------------------------------------------------------------------------
# Vaste huisregel: nooit een em-dash of en-dash. De build faalt liever dan er
# eentje door te laten, zodat de tekst er verzorgd en menselijk uit blijft zien.
# ---------------------------------------------------------------------------
EM_DASH = "—"
EN_DASH = "–"


def _controleer_geen_dash(doc: Document) -> None:
    verboden = {EM_DASH: "em-dash", EN_DASH: "en-dash"}

    def check(tekst: str, waar: str) -> None:
        for teken, naam in verboden.items():
            if teken in tekst:
                i = tekst.index(teken)
                fragment = tekst[max(0, i - 25) : i + 25]
                raise ValueError(
                    f"{naam} gevonden in {waar}: ...{fragment}... "
                    f"Gebruik een komma, dubbele punt of haakjes."
                )

    def loop(waarde, waar: str) -> None:
        if isinstance(waarde, str):
            check(waarde, waar)
        elif isinstance(waarde, (list, tuple)):
            for item in waarde:
                loop(item, waar)
        elif hasattr(waarde, "__dict__"):
            for naam, deel in vars(waarde).items():
                loop(deel, f"{waar}.{naam}")

    loop(doc.meta, "kop")
    for blok in doc.blokken:
        loop(blok, type(blok).__name__)


# ---------------------------------------------------------------------------
# Tekst-opmaak: **vet** naar reportlab-<b>. Simpel en voldoende voor deze docs.
# ---------------------------------------------------------------------------
def _rijk(tekst: str) -> str:
    uit, vet = [], False
    i = 0
    while i < len(tekst):
        if tekst.startswith("**", i):
            uit.append("</b>" if vet else "<b>")
            vet = not vet
            i += 2
        else:
            ch = tekst[i]
            # Newline -> harde regelafbreking (voor adresblokken e.d.).
            uit.append(
                {"&": "&amp;", "<": "&lt;", ">": "&gt;", "\n": "<br/>"}.get(ch, ch)
            )
            i += 1
    if vet:
        uit.append("</b>")
    return "".join(uit)


def _stijlen() -> dict:
    basis = ParagraphStyle(
        "basis",
        fontName=theme.FONT,
        fontSize=10.5,
        leading=15.5,
        textColor=theme.INKT,
    )
    return {
        "para": basis,
        "h1": ParagraphStyle(
            "h1", parent=basis, fontName=theme.FONT_VET, fontSize=14,
            leading=18, spaceBefore=14, spaceAfter=4, textColor=theme.INKT,
            keepWithNext=1,
        ),
        "h2": ParagraphStyle(
            "h2", parent=basis, fontName=theme.FONT_VET, fontSize=11.5,
            leading=15, spaceBefore=10, spaceAfter=2, textColor=theme.ACCENT_TEKST,
            keepWithNext=1,
        ),
        "bullet": ParagraphStyle(
            "bullet", parent=basis, leftIndent=12, bulletIndent=2, spaceAfter=2,
        ),
        "note": ParagraphStyle(
            "note", parent=basis, fontSize=10, leading=14.5,
        ),
        "note_kop": ParagraphStyle(
            "note_kop", parent=basis, fontName=theme.FONT_VET, fontSize=9,
            textColor=theme.ACCENT_TEKST, spaceAfter=2,
        ),
        "code": ParagraphStyle(
            "code", fontName=theme.FONT_CODE, fontSize=8.5, leading=11.5,
            textColor=theme.INKT,
        ),
        "onderschrift": ParagraphStyle(
            "onderschrift", parent=basis, fontSize=8.5, textColor=theme.GRIJS,
            spaceBefore=2,
        ),
        "cel": ParagraphStyle("cel", parent=basis, fontSize=9.5, leading=13),
        "cel_r": ParagraphStyle(
            "cel_r", parent=basis, fontSize=9.5, leading=13, alignment=TA_RIGHT,
        ),
        "kop_titel": ParagraphStyle(
            "kop_titel", parent=basis, fontName=theme.FONT_VET, fontSize=22,
            leading=25, textColor=theme.INKT,
        ),
        "kop_onder": ParagraphStyle(
            "kop_onder", parent=basis, fontSize=11, textColor=theme.GRIJS,
            spaceBefore=2,
        ),
        "kopregel": ParagraphStyle(
            "kopregel", parent=basis, fontSize=9.5, textColor=theme.GRIJS,
            alignment=TA_RIGHT, leading=13,
        ),
        "totaal_l": ParagraphStyle(
            "totaal_l", parent=basis, fontName=theme.FONT_VET, fontSize=11.5,
        ),
        "totaal_r": ParagraphStyle(
            "totaal_r", parent=basis, fontName=theme.FONT_VET, fontSize=11.5,
            alignment=TA_RIGHT, textColor=theme.ACCENT_TEKST,
        ),
    }


class _Streep(Flowable):
    """Een dunne horizontale scheidingslijn over de tekstbreedte."""

    def __init__(self, breedte, kleur=theme.LIJN, dikte=0.8):
        super().__init__()
        self.breedte, self.kleur, self.dikte = breedte, kleur, dikte

    def wrap(self, *_):
        return (self.breedte, self.dikte + 6)

    def draw(self):
        self.canv.setStrokeColor(self.kleur)
        self.canv.setLineWidth(self.dikte)
        self.canv.line(0, 3, self.breedte, 3)


# ---------------------------------------------------------------------------
# Blok -> flowables
# ---------------------------------------------------------------------------
def _blok(blok, st, breedte) -> list:
    if isinstance(blok, Heading):
        stijl = st["h1"] if blok.niveau == 1 else st["h2"]
        return [Paragraph(_rijk(blok.tekst), stijl)]

    if isinstance(blok, Para):
        return [Paragraph(_rijk(blok.tekst), st["para"]), PSpacer(1, 4)]

    if isinstance(blok, Bullets):
        uit = []
        for item in blok.items:
            uit.append(Paragraph(_rijk(item), st["bullet"], bulletText="•"))
        uit.append(PSpacer(1, 4))
        return uit

    if isinstance(blok, Table):
        return _tabel(blok, st, breedte)

    if isinstance(blok, Total):
        rij = [[Paragraph(_rijk(blok.label), st["totaal_l"]),
                Paragraph(_rijk(blok.bedrag), st["totaal_r"])]]
        t = PTable(rij, colWidths=[breedte * 0.7, breedte * 0.3])
        t.setStyle(TableStyle([
            ("LINEABOVE", (0, 0), (-1, 0), 1.0, theme.ACCENT),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        return [PSpacer(1, 2), t, PSpacer(1, 4)]

    if isinstance(blok, Note):
        kop = Paragraph(_rijk(blok.kop), st["note_kop"])
        tekst = Paragraph(_rijk(blok.tekst), st["note"])
        t = PTable([[kop], [tekst]], colWidths=[breedte])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), theme.KADER_VUL),
            ("LINEBEFORE", (0, 0), (0, -1), 2.5, theme.ACCENT),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, 0), 8),
            ("BOTTOMPADDING", (0, -1), (-1, -1), 8),
        ]))
        return [PSpacer(1, 2), KeepTogether([t]), PSpacer(1, 6)]

    if isinstance(blok, Code):
        regels = [Paragraph(_rijk(r) or "&nbsp;", st["code"]) for r in blok.tekst.split("\n")]
        t = PTable([[r] for r in regels], colWidths=[breedte])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), theme.CODE_VUL),
            ("BOX", (0, 0), (-1, -1), 0.6, theme.CODE_LIJN),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 1.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
        ]))
        uit = [PSpacer(1, 2), t]
        if blok.onderschrift:
            uit.append(Paragraph(_rijk(blok.onderschrift), st["onderschrift"]))
        uit.append(PSpacer(1, 6))
        return uit

    if isinstance(blok, Image):
        return _beeld(blok, st, breedte)

    if isinstance(blok, Spacer):
        return [PSpacer(1, blok.hoogte)]

    return []


def _tabel(blok, st, breedte) -> list:
    ncols = len(blok.kop)
    uitl = blok.uitlijning or ["links"] * ncols

    def cel(tekst, kol, kop=False):
        stijl = st["cel_r"] if uitl[kol] == "rechts" else st["cel"]
        if kop:
            stijl = ParagraphStyle(
                "kopcel", parent=stijl, fontName=theme.FONT_VET,
                textColor=theme.TABEL_KOP,
            )
        return Paragraph(_rijk(str(tekst)), stijl)

    data = [[cel(k, i, kop=True) for i, k in enumerate(blok.kop)]]
    for rij in blok.rijen:
        data.append([cel(w, i) for i, w in enumerate(rij)])

    gewichten = blok.kolombreedtes or [1] * ncols
    totaal = sum(gewichten)
    t = PTable(data, colWidths=[breedte * g / totaal for g in gewichten], repeatRows=1)
    stijl = [
        ("LINEBELOW", (0, 0), (-1, 0), 1.0, theme.TABEL_KOP),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, theme.LIJN),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    for r in range(1, len(data)):
        if r % 2 == 0:
            stijl.append(("BACKGROUND", (0, r), (-1, r), theme.TABEL_STREEP))
    t.setStyle(TableStyle(stijl))
    # De witruimte erboven mag een voorgaande kop niet van de tabel losknippen.
    boven = PSpacer(1, 2)
    boven.keepWithNext = 1
    return [boven, t, PSpacer(1, 6)]


def _beeld(blok, st, breedte) -> list:
    from reportlab.lib.utils import ImageReader

    try:
        iw, ih = ImageReader(blok.pad).getSize()
    except Exception as e:
        return [Paragraph(f"[afbeelding niet gevonden: {blok.pad} ({e})]", st["onderschrift"])]

    max_h = blok.max_hoogte_mm * mm
    if blok.breedte_mm:
        w = blok.breedte_mm * mm
    else:
        w = breedte
    h = w * ih / iw
    if h > max_h:
        h = max_h
        w = h * iw / ih

    img = PImage(blok.pad, width=w, height=h)
    halign = {"links": "LEFT", "midden": "CENTER", "rechts": "RIGHT"}.get(blok.uitlijning, "CENTER")
    img.hAlign = halign
    uit = [PSpacer(1, 2), img]
    if blok.onderschrift:
        uit.append(Paragraph(_rijk(blok.onderschrift), st["onderschrift"]))
    uit.append(PSpacer(1, 6))
    return uit


def _titelband(doc: Document, st, breedte) -> list:
    m = doc.meta
    titel = Paragraph(_rijk(m.titel), st["kop_titel"])
    onder = Paragraph(_rijk(m.ondertitel), st["kop_onder"]) if m.ondertitel else None

    linkercel = [titel] + ([onder] if onder else [])
    rechtercel = []
    for label, waarde in m.kopregels:
        rechtercel.append(Paragraph(f"<b>{_rijk(label)}</b>  {_rijk(waarde)}", st["kopregel"]))

    t = PTable(
        [[linkercel, rechtercel]],
        colWidths=[breedte * 0.62, breedte * 0.38],
    )
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    return [t, PSpacer(1, 8), _Streep(breedte, theme.LIJN, 1.0), PSpacer(1, 10)]


# ---------------------------------------------------------------------------
# Pagina-decoratie: logo boven, voettekst + paginanummer onder.
# ---------------------------------------------------------------------------
def _maak_decorator(voettekst: str):
    def decoreer(canvas, doc_template):
        canvas.saveState()
        # Logo rechtsboven.
        breedte_logo = 0
        canvas.setFont(theme.FONT_VET, 15)
        breedte_logo = (
            canvas.stringWidth(theme.MERK_NAAM_1 + theme.MERK_NAAM_2, theme.FONT_VET, 13)
        )
        x = A4[0] - theme.MARGE_RECHTS - breedte_logo
        y = A4[1] - theme.MARGE_BOVEN + 6 * mm
        theme.teken_logo(canvas, x, y)

        # Voettekst links, paginanummer rechts.
        canvas.setFont(theme.FONT, 8)
        canvas.setFillColor(theme.LICHTGRIJS)
        vy = theme.MARGE_ONDER - 8 * mm
        canvas.drawString(theme.MARGE_LINKS, vy, voettekst)
        canvas.drawRightString(
            A4[0] - theme.MARGE_RECHTS, vy, f"{doc_template.page}"
        )
        canvas.restoreState()

    return decoreer


def render_pdf(doc: Document, pad: str) -> None:
    """Bouwt een Document naar een PDF op het gegeven pad."""
    _controleer_geen_dash(doc)
    st = _stijlen()
    breedte = A4[0] - theme.MARGE_LINKS - theme.MARGE_RECHTS

    frame = Frame(
        theme.MARGE_LINKS,
        theme.MARGE_ONDER,
        breedte,
        A4[1] - theme.MARGE_BOVEN - theme.MARGE_ONDER,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    voettekst = doc.voettekst or theme.VOETTEKST
    sjabloon = BaseDocTemplate(
        pad, pagesize=A4,
        leftMargin=theme.MARGE_LINKS, rightMargin=theme.MARGE_RECHTS,
        topMargin=theme.MARGE_BOVEN, bottomMargin=theme.MARGE_ONDER,
        title=doc.meta.titel,
    )
    sjabloon.addPageTemplates([
        PageTemplate(id="std", frames=[frame], onPage=_maak_decorator(voettekst))
    ])

    verhaal = _titelband(doc, st, breedte)
    for blok in doc.blokken:
        verhaal.extend(_blok(blok, st, breedte))

    sjabloon.build(verhaal)
