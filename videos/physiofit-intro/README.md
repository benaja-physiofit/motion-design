# Physiofit Intro – Sonic-Logo-Sting (4,0 s, hell)

Kurzes Premium-Intro für Product-Launch- und Academy-Videos, im hellen Notion-/Linear-Light-Stil, mit
der offiziellen Physiofit-Wort-Bild-Marke. Eine Bildidee zieht sich durch: **Atem**. Erst das Einatmen
(ein Tintenpunkt, eine Haarlinie zieht sich auf und wieder zusammen), dann das Aufblühen (der Punkt wird
zum Kopf des P), dann das Ausatmen (Blur und Fade zurück auf Papier). Der Ton ist eigens komponiert und
framegenau auf die Bewegung gelegt.

| | |
|---|---|
| Format | 1920×1080, 60 fps, 4,00 s, H.264 + AAC 48 kHz Stereo |
| Lautheit | −15 LUFS integriert, True Peak ≤ −1 dBTP |
| Render | `renders/physiofit-intro-light.mp4` |
| Proof-Sheet | `snapshots/contact-sheet-1.jpg`, `snapshots/contact-sheet-2.jpg` |
| Logo | `assets/brand/` (offizielle SVGs, Pfade 1:1 übernommen) |

## Timing (Beats)

| Zeit | Bild | Ton |
|---|---|---|
| 0,12–0,80 s | Tintenpunkt, Haarlinie dehnt sich und zieht sich zusammen | Reverse-Swell des Hit-Akkords + aufsteigende Luft |
| **0,80 s** | **Hit:** Das P wächst aus dem Punkt (der Punkt wird zum Kopf), Tinten-Welle und ein Ring | Sub-Drop, Filz-Transient, Dmaj9-Pad, Glasglocke |
| 0,92 s | Der Fuß des P setzt wie ein Schritt nach | weicher Filz-„Schritt“ |
| 1,10–1,70 s | Bildmarke gleitet an ihren Platz | Whoosh folgt der Geschwindigkeit |
| 1,48–2,0 s | PHYSIOFIT steigt Buchstabe für Buchstabe aus einer Maske | Harfen-Glissando, ein Ton pro Buchstabe |
| 1,92 s | Lockup steht | Chime (offene Quinte D6 + A6) |
| 2,15–3,0 s | Ein Satin-Glanz läuft über das Logo | Sparkle, wandert von links nach rechts |
| 3,05–3,70 s | Ausatmen: Blur, Fade, leichter Push | Abwärts-Luft, Hall klingt bis 4,0 s aus |

Schnitt-Tipp: Ab ca. 3,7 s ist das Bild leeres Papier. Das eigentliche Video kann dort beginnen, der Hall-Ausklang läuft darunter weiter.

## Anpassen

- **Farben:** Variablen `ink` (Logo, Standard `#1E3542` = Physiofit BlueDark) und `tint` (Halo) in `index.html` oder im Studio unter Variablen.
- **Größe des Logos:** `#lk-lockup` in `compositions/lockup.html` (Breite = 1680 Logo-Einheiten × Skalierung; Höhe proportional anpassen).
- **Timing:** Die Beats stehen oben in den Skripten von `compositions/atmosphere.html`, `compositions/lockup.html` und `sound/sonic_logo.py`. Bei Änderungen alle drei synchron halten und den Ton neu erzeugen.

## Ton neu erzeugen

```bash
pip install numpy scipy   # ffmpeg muss installiert sein
python3 sound/sonic_logo.py   # → assets/audio/physiofit-sonic-logo.wav (deterministisch, Seed-basiert)
```

## Prüfen & rendern

```bash
npx hyperframes check .
npx hyperframes render . --fps 60 --quality high -o renders/physiofit-intro-light.mp4
# Variante für 30-fps-Timelines: --fps 30
```

## Dateien

- `index.html`: schlanker Orchestrator (3 Sub-Kompositionen + Audio-Spur)
- `compositions/atmosphere.html`: helle Bühne, Halo, Dot-Grid, Tintenpunkt, Haarlinie, Welle, Ring
- `compositions/lockup.html`: offizielle Wort-Bild-Marke, Wachsen aus dem Punkt, Fuß-Schritt, Slide, Buchstaben-Rise, Satin-Glanz, Exit
- `compositions/grain.html`: feines Grain gegen Banding (aus Registry `grain-overlay`)
- `sound/sonic_logo.py`: Synthese des Sonic Logos (Dmaj9, D-Dur pentatonisch)
- `shot-plan.json`: Shot-Plan (Kategorie `logo-reveal`)
- GSAP lokal unter `assets/vendor/`
