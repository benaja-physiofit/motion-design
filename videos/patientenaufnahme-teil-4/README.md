# Patientenaufnahme – Teil 4: Aufnahmeformular einrichten

Animationen zum Clip `Patientenaufnahme_Teil_4.mov` (19,4 s), abstrahiert in der Karten-Sprache von Teil 1. Komplett Vollbild,
Benaja ist nur zu hören. Ohne Musik und Soundeffekte, nur der O-Ton.

| | |
|---|---|
| Format | 1920×1080, 30 fps, 19,43 s, H.264 + AAC |
| Render | `renders/patientenaufnahme-teil-4.mp4` |
| Storyboard | `boards/storyboard.html` (Bild: `boards/storyboard.png`), Plan: `STORYBOARD.md` |
| Plan mit allen Maßen | `SPEC.md` |
| Review-Notizen | `REVIEW.md` |
| Transkript mit Wortzeiten | `transcript.json` |

## Ablauf

| Zeit | Gesprochen | Bild |
|---|---|---|
| 0–3,7 s | „Frage Stammdaten wie Name, Adresse oder Geburtsdatum ab.“ | Karte „Patientenaufnahme“: Balken „Stammdaten“, darunter Name, Adresse, Geburtsdatum. |
| 3,7–6,3 s | „Füge deinen Behandlungsvertrag ein …“ | Balken „Behandlungsvertrag“ füllt sich, Haken. |
| 6,3–10,6 s | „… ergänze wichtige Hinweise, zum Beispiel zur gesetzlichen Zuzahlung oder Ausfallgebühren.“ | Hinweis-Balken „Zuzahlung“ und „Ausfallgebühren“. |
| 10,6–14,3 s | „Stelle dabei sicher, dass sie auch wirklich gesehen und akzeptiert werden.“ | Augen-Symbol (gesehen), dann Haken (akzeptiert) an beiden Hinweisen. |
| 14,3–19,43 s | „Lass Patienten alles rechtssicher und digital signieren. Ganz einfach per Checkbox.“ | Karte rückt nach links, eine Linie führt zu zwei Checkboxen, beide werden angehakt. |

## Bearbeiten

- Texte sind Variablen (Studio → Variablen): Titel, Balken, Hinweise, Checkbox-Texte.
- Timing: `compositions/formular.html` (Filmzeit) und `compositions/signatur.html` (ab 14,3 s); die Kommentare nennen die Wörter.

## Footage neu erzeugen

Das umkodierte Footage liegt nicht im Repo (nur für den Ton nötig). Aus dem Original-Clip:

```bash
ffmpeg -i Patientenaufnahme_Teil_4.mov -c:v libx264 -crf 14 -preset slow -g 30 -keyint_min 30 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -c:a aac -b:a 192k -movflags +faststart assets/footage/patientenaufnahme-teil4.mp4
```

## Prüfen und rendern

```bash
npx hyperframes check
```

```bash
npx hyperframes render --quality delivery --output renders/patientenaufnahme-teil-4.mp4
```
