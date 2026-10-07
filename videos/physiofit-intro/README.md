# Physiofit Intro – Sonic-Logo-Sting (4,0 s)

Kurzes Premium-Intro für Product-Launch- und Academy-Videos. Eine Bildidee zieht sich durch: **Atem**.
Erst das Einatmen (ein Lichtpunkt, eine Haarlinie zieht sich auf und wieder zusammen), dann das Aufblühen
(das Logo entsteht aus dem Licht), dann das Ausatmen (Blur und Fade auf Schwarz). Der Ton ist
eigens komponiert und framegenau auf die Bewegung gelegt.

| | |
|---|---|
| Format | 1920×1080, 60 fps, 4,00 s, H.264 + AAC 48 kHz Stereo |
| Lautheit | −15 LUFS integriert, True Peak ≤ −1 dBTP |
| Review-Render | `renders/physiofit-intro-review.mp4` |
| Proof-Sheet | `snapshots/contact-sheet-1.jpg`, `snapshots/contact-sheet-2.jpg` |

## Timing (Beats)

| Zeit | Bild | Ton |
|---|---|---|
| 0,12–0,80 s | Lichtpunkt, Haarlinie dehnt sich und zieht sich zusammen | Reverse-Swell des Hit-Akkords + aufsteigende Luft |
| **0,80 s** | **Hit:** Logo blüht aus dem Punkt (Blur → scharf), Bloom und ein Ring | Sub-Drop, Filz-Transient, Dmaj9-Pad, Glasglocke |
| 1,18–1,85 s | Mark gleitet nach links, Wortmarke gleitet unter dem Tile hervor | Whoosh folgt der Geschwindigkeit; Harfen-Glissando, ein Ton pro Buchstabe |
| 1,85 s | Lockup steht | Chime (offene Quinte D6 + A6) |
| 1,98–2,95 s | Ein Specular-Lichtstreif über Tile und Wortmarke | Sparkle, wandert von links nach rechts |
| 3,05–3,70 s | Ausatmen: Blur, Fade, leichter Push | Abwärts-Luft, Hall klingt bis 4,0 s aus |

Schnitt-Tipp: Das Bild ist ab ca. 3,7 s schwarz. Das eigentliche Video kann dort beginnen, der Hall-Ausklang läuft darunter weiter.

## ⚠ Logo ist ein Platzhalter

Das offizielle Physiofit-Logo ließ sich aus der Build-Umgebung nicht laden (Netzwerk-Policy).
Das grüne „P“-Tile und die gesetzte Wortmarke (Geist SemiBold) sind **Platzhalter**.

**Logo austauschen:** In `compositions/lockup.html` den Inhalt von `#lk-mark-pop` (Tile + SVG) durch das
offizielle SVG ersetzen. Bewegung, Timing und Ton bleiben gleich. Das Draw-on des „P“ entfällt dann,
das Logo blüht einfach auf. Ist das offizielle Logo eine reine Wortmarke, kann man das Mark weglassen.

**Farben:** Variablen `accent` / `accentDeep` in `index.html` (oder im Studio unter Variablen) auf die Brand-Farben setzen.
**Wortmarke:** Variable `wordmark` in `compositions/lockup.html`.

Wenn Wortmarke, Schriftgröße oder Slide-Timing sich ändern: die Buchstaben-Zeiten in
`sound/letter-emergence.json` neu messen (Zeitpunkt, an dem jeder Buchstabe unter dem Tile hervorkommt)
und den Ton neu erzeugen.

## Ton neu erzeugen

```bash
pip install numpy scipy   # ffmpeg muss installiert sein
python3 sound/sonic_logo.py   # → assets/audio/physiofit-sonic-logo.wav (deterministisch, Seed-basiert)
```

## Prüfen & rendern

```bash
npx hyperframes check .
npx hyperframes render . --fps 60 --quality high -o renders/physiofit-intro.mp4
# Variante für 30-fps-Timelines: --fps 30
```

## Dateien

- `index.html`: schlanker Orchestrator (3 Sub-Kompositionen + Audio-Spur)
- `compositions/atmosphere.html`: Bühne, Glow, Dot-Grid, Lichtpunkt, Haarlinie, Bloom, Ring
- `compositions/lockup.html`: Mark + Wortmarke, Slide-out, Specular-Sweep, Exit
- `compositions/grain.html`: Film-Grain gegen Banding (aus Registry `grain-overlay`)
- `sound/sonic_logo.py`: Synthese des Sonic Logos (Dmaj9, D-Dur pentatonisch)
- `shot-plan.json`: Shot-Plan (Kategorie `logo-reveal`)
- Schrift: Geist (SIL OFL, `assets/fonts/`), GSAP lokal unter `assets/vendor/`
