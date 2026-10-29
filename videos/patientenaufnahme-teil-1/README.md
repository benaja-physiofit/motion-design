# Patientenaufnahme – Teil 1: Animationen

Grafik-Animationen über dem Clip `Patientenaufnahme2_Teil_1.mov` (20,4 s), im Stil von `finales_video.mp4`:
helle Karten, Lora-Titel, Ubuntu-UI-Text, Navy-Balken, Petrol-Icons, Cyan-Haken. Ohne Musik und Soundeffekte,
nur der O-Ton. Das Footage ist mit `friendly-saas-explainer-patientenaufnahme2.cube` gegradet: derselbe Look wie der erste LUT,
aber auf das hellere, neutralere Licht dieses Clips abgestimmt.

| | |
|---|---|
| Format | 1920×1080, 30 fps, 20,4 s, H.264 + AAC |
| Render | `renders/patientenaufnahme-teil-1.mp4` |
| Plan mit allen Maßen | `SPEC.md` |
| Review-Notizen | `REVIEW.md` |
| Transkript mit Wortzeiten | `transcript.json` |

## Ablauf

| Zeit | Gesprochen | Bild |
|---|---|---|
| 0,25–6,5 s | „Bei der Patientenaufnahme werden immer noch Papierbögen ausgefüllt, eingescannt oder mühsam abgetippt.“ | Karte links: Papierbogen landet, Kuli füllt aus, Scan-Linie, Name wird getippt. Die Status-Pill wechselt Ausgefüllt → Eingescannt → Abgetippt. |
| 6,55–12,0 s | „Das kostet den Empfang wertvolle Zeit. Und nicht selten starten Patienten zu spät in die Behandlung.“ | Zwei Karten rechts: Uhr und leerlaufender Balken „Wertvolle Zeit“, danach Zeitstrahl Termin → Start mit „zu spät“. |
| 12,0–17,15 s | „Der unterschriebene Behandlungsvertrag, die Regelungen zur Ausfallgebühr und andere wichtige Dokumente …“ | Harter Schnitt auf Vollbild: „Wichtige Dokumente“, drei Balken füllen sich, Unterschrift zeichnet sich, je ein Haken. |
| 17,15–20,4 s | „… müssen jahrelang aufbewahrt werden und griffbereit sein.“ | Karte links: „Aufbewahrung“, Sanduhr „Jahrelang“, Suche findet den Behandlungsvertrag. |

## Bearbeiten

- Texte und Farben sind Variablen (Studio → Variablen): Titel jeder Karte, Badge „zu spät“, Navy/Petrol/Cyan/Grund.
- Timing: Jede Szene steht in `compositions/<szene>.html`; die Zeiten im Skript sind lokal zur Szene, die Kommentare
  nennen die Filmzeit der gesprochenen Wörter.
- LUT-Stärke: `data-color-grading` am `#footage`-Video in `index.html` (`lut.intensity`, 0–1), am besten per
  `npx hyperframes media-treatment --selector '#footage' …`.

## Footage neu erzeugen

Das umkodierte Footage liegt nicht im Repo (36 MB). Aus dem Original-Clip:

```bash
ffmpeg -i Patientenaufnahme2_Teil_1.mov -c:v libx264 -crf 14 -preset slow -g 30 -keyint_min 30 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -c:a aac -b:a 192k -movflags +faststart assets/footage/patientenaufnahme2-teil1.mp4
```

## Prüfen und rendern

```bash
npx hyperframes check
```

```bash
npx hyperframes render --quality delivery --output renders/patientenaufnahme-teil-1.mp4
```
