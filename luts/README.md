# Friendly SaaS Explainer LUT

33er 3D-LUTs, **Rec.709 rein → Rec.709 raus** (iPhone HEVC, SDR Rec.709, kein Apple Log).

| Datei | Für | Wand im Rohmaterial (RGB) |
| --- | --- | --- |
| `friendly-saas-explainer.cube` | `Patientenaufnahme-1.mov` | 176 / 168 / 163 (dunkler, rosa Stich) |
| `friendly-saas-explainer-patientenaufnahme2.cube` | `Patientenaufnahme2_Teil_1.mov` | 214 / 212 / 208 (heller, fast neutral) |

Beide ergeben denselben Look. Der erste LUT auf dem helleren zweiten Clip macht die Wand fast weiß (≈ 237)
mit leichtem Grünstich, deshalb hat Clip 2 seine eigene Variante.

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

Variante für einen anderen Clip: die Wand im Rohmaterial messen (8-bit RGB) und übergeben. `--match` (0–1) gleicht
zusätzlich die Belichtung an Clip 1 an; für Clip 2 passt 0,35:

```bash
python3 build_friendly_saas_lut.py friendly-saas-explainer-patientenaufnahme2.cube --wall 213.8 211.8 207.7 --match 0.35
```

Wichtige Stellschrauben oben im Skript: `WALL_TARGET` (Weißpunkt), `TONE_NEUTRAL` (Helligkeit Hintergrund),
`TONE_COLOUR` (Helligkeit Haut/Farben), `BLACK_LIFT` (Schwarzwert).
