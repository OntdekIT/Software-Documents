"""Hulpfuncties voor de procesdocumenten (15 tot 18)."""
from docgen import Bullets, Heading, Note, Para, Table


def _s(t):
    return t.replace("`", "") if isinstance(t, str) else t


def schoon(blokken):
    """De engine kent geen codespans: haal backticks uit alle tekst."""
    for b in blokken:
        if isinstance(b, (Para, Heading)):
            b.tekst = _s(b.tekst)
        elif isinstance(b, Note):
            b.tekst = _s(b.tekst)
        elif isinstance(b, Bullets):
            b.items = [_s(i) for i in b.items]
        elif isinstance(b, Table):
            b.kop = [_s(c) for c in b.kop]
            b.rijen = [[_s(c) for c in r] for r in b.rijen]
    return blokken
