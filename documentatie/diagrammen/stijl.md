# Diagramstijl

Alle diagrammen gebruiken de kleuren van de app. Bronnen: `src/index.css` van de frontend.

| Rol | Kleur |
|---|---|
| Inkt (lijnen, tekst) | #111827 |
| Amber (accent, hoofdelementen) | #FECB3D |
| Donker amber (kleine accenttekst, kaders) | #8A6408 |
| Zachte vulling (vakken, notities) | #FFF9E6 |
| Gedempt (bijschriften, secundaire pijlen) | #4B5563 |
| Lijn licht | #E5E7EB |

- Lettertype Helvetica (zelfde als de PDF).
- Blauw wordt niet gebruikt in diagrammen, net als in de app (blauw is alleen voor knoppen).
- PlantUML: `!include` van `diagrammen/stijl.puml`. Graphviz: gebruik `graph [fontname="Helvetica"]`, `node [style="filled,rounded", shape=box, fillcolor="#FFF9E6", color="#111827", fontcolor="#111827", fontname="Helvetica"]`, `edge [color="#111827", fontcolor="#4B5563", fontname="Helvetica"]`, hoofdonderdelen `fillcolor="#FECB3D"`.
- Exporteer PNG op minimaal 200 dpi (`dot -Gdpi=200`, `plantuml -tpng -Sdpi=200`).
- Geen em- of en-dashes in labels.
