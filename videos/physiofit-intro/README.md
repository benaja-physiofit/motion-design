# Physiofit Intro „Blende“ – Sonic-Logo-Sting (2,5 s)

Kurzes Premium-Intro für Product-Launch- und Academy-Videos, gewählt aus der Storyboard-Runde
(Konzept 4). Das Bild startet als volle Fläche in Physiofit-BlueDark. Eine Kreisblende schließt sich
und rastet exakt als Kopf des P ein. Daraus wächst das Logo, die Wortmarke folgt, dann Ausblenden auf
helles Papier. Die Wort-Bild-Marke ist 1:1 aus den offiziellen SVGs übernommen.

| | |
|---|---|
| Format | 1920×1080, 60 fps, 2,50 s, H.264 + AAC 48 kHz Stereo |
| Lautheit | −15 LUFS integriert, True Peak ≤ −1 dBTP |
| Render | `renders/physiofit-intro-blende.mp4` |
| Ton einzeln | `assets/audio/physiofit-sonic-logo.wav` (24 bit) |
| Proof-Sheet | `snapshots/contact-sheet-1.jpg`, `snapshots/contact-sheet-2.jpg` |

## Timing (Beats)

| Zeit | Bild | Ton |
|---|---|---|
| 0,00 s | Volle Fläche in BlueDark | Stille |
| 0,10–0,72 s | Die Kreisblende schließt sich und gibt helles Papier frei | Luftzug, der der Blendengeschwindigkeit folgt, tiefe Spannung steigt eine Quarte, leiser Reverse-Swell |
| **0,72 s** | **Einrasten:** Der Kreis ist der Kopf des P, ein Haarlinien-Ring hallt nach, der Stamm wächst heraus | präziser Blenden-Klick, kurzer Sub-Impuls, gläserner Akkord D5 · A5 · E6 über leisem warmem Bett |
| 0,86 s | Der Fuß setzt nach | weicher Filz-Tap |
| 0,98–1,48 s | PHYSIOFIT wischt vom Bildzeichen aus auf | ein Hauch Luft von links nach rechts |
| 0,72–2,0 s | Das ganze Bild setzt sich von 102,5 % auf 100 % | Akkord klingt aus |
| 2,20–2,50 s | Ausblenden auf Papier | Ausklang bis Stille |

## Anpassen

- **Farbe:** Variable `ink` (Standard `#1E3542` = Physiofit BlueDark) in `index.html` oder im Studio unter Variablen.
- **Timing:** Die Beats stehen oben im Skript von `compositions/lockup.html` und in `sound/sonic_logo.py`. Bei Änderungen beide synchron halten und den Ton neu erzeugen.

## Ton neu erzeugen

```bash
pip install numpy scipy   # ffmpeg muss installiert sein
python3 sound/sonic_logo.py   # → assets/audio/physiofit-sonic-logo.wav (deterministisch, Seed-basiert)
```

## Prüfen & rendern

```bash
npx hyperframes check .
npx hyperframes render . --fps 60 --quality high -o renders/physiofit-intro-blende.mp4
# Variante für 30-fps-Timelines: --fps 30
```

## Dateien

- `index.html`: schlanker Orchestrator (3 Sub-Kompositionen + Audio-Spur)
- `compositions/lockup.html`: Blende, Wort-Bild-Marke, Stamm-Wachstum, Fuß, Wortmarken-Wisch, Exit (eine Vollbild-SVG im Logo-Koordinatensystem)
- `compositions/atmosphere.html`: helles Papier
- `compositions/grain.html`: feines Grain gegen Banding (aus Registry `grain-overlay`)
- `sound/sonic_logo.py`: minimalistisches Sound-Design, synthetisiert
- `shot-plan.json`: Shot-Plan (Kategorie `logo-reveal`, Konzept „Blende“)
- GSAP lokal unter `assets/vendor/`
