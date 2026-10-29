# Friendly SaaS Explainer LUT

`friendly-saas-explainer.cube`: 33er 3D-LUT, **Rec.709 rein → Rec.709 raus**.
Abgestimmt auf den Dreh `Patientenaufnahme` (iPhone HEVC, SDR Rec.709, kein Apple Log).

## Look

- **Weißabgleich**: entfernt den warm-rosa Stich der Wand (RGB 176/168/163 → fast neutral, Hauch „Papierweiß“).
- **High-Key**: Die graue Wand wird hell und luftig (~168 → ~213), Schwarz wird nur minimal angehoben.
- **Hauttöne**: Haut bekommt eine eigene, sanftere Kurve, damit das Gesicht Kontur behält und Rot nicht clippt.
  Der Farbton ist leicht von rosig Richtung Pfirsich verschoben.
- **Farben**: insgesamt etwas gedämpft (Pastell), Blau-Akzente bleiben frisch, Weiß und Schatten sind sauber.
- **Highlights**: weicher Roll-off statt harter Clipping-Kante.

## Anwendung

| Programm | Wo |
| --- | --- |
| DaVinci Resolve | Color Page → Node → Rechtsklick → LUT, oder `LUT`-Ordner + Node-LUT |
| Premiere Pro | Lumetri Color → Kreativ → Look → Durchsuchen (alternativ Basiskorrektur → Eingabe-LUT) |
| Final Cut Pro | Effekt „Eigene LUT“ → LUT wählen, Eingang/Ausgang Rec.709 |
| CapCut (Desktop) | Anpassung → LUT → Importieren; fürs ganze Video eine Anpassungsebene über die Timeline ziehen und dort den LUT wählen |

- Auf den **unbearbeiteten** Clip legen, ohne andere Korrekturen davor.
- Auf Clips mit anderem Licht bzw. anderer Kamera-Einstellung wirkt der LUT anders, weil der Weißabgleich fest eingebaut ist.
  Bei Bedarf danach Belichtung/Temperatur leicht nachziehen oder die LUT-Deckkraft reduzieren.

## Anpassen

Der LUT wird mit `build_friendly_saas_lut.py` erzeugt (nur NumPy nötig):

```bash
python3 build_friendly_saas_lut.py friendly-saas-explainer.cube --size 33
```

Wichtige Stellschrauben oben im Skript: `WALL_TARGET` (Weißpunkt), `TONE_NEUTRAL` (Helligkeit Hintergrund),
`TONE_COLOUR` (Helligkeit Haut/Farben), `BLACK_LIFT` (Schwarzwert).
