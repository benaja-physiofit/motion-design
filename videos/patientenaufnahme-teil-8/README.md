# Patientenaufnahme – Teil 8 (Ende): Animationen

Grafik-Animationen über dem Clip `PatientenaufnahmeTeil_8_Ende.mov` (7,07 s), im Stil der Abschluss-Karten aus
`finales_video.mp4`. Benaja bleibt die ganze Zeit im Bild; die Karten stehen links und rechts daneben. Ohne Musik und
Soundeffekte, nur der O-Ton. Das Footage ist mit `friendly-saas-explainer-patientenaufnahme2.cube` gegradet
(gleiches Licht wie Teil 2, Wand RGB 217/215/210).

| | |
|---|---|
| Format | 1920×1080, 30 fps, 7,07 s, H.264 + AAC |
| Render | `renders/patientenaufnahme-teil-8.mp4` |
| Storyboard (freigegeben) | `boards/storyboard.html`, `boards/storyboard.png`, `STORYBOARD.md` |
| Plan mit allen Maßen | `SPEC.md` |
| Review-Notizen | `REVIEW.md` |
| Transkript mit Wortzeiten | `transcript.json` |

## Ablauf

| Zeit | Gesprochen | Bild |
|---|---|---|
| 0,0–2,85 s | „Wenn du Hilfe bei der einmaligen Einrichtung benötigst,“ | Karte links landet: Rettungsring, „Hilfe bei der Einrichtung?“, Button noch als Platzhalter. |
| 2,85–4,3 s | „schreib uns eine Nachricht“ | Button „Nachricht schreiben“ füllt sich und wird angetippt. Oben mittig erscheint die Physiofit-Pille, eine Linie verbindet sie mit der Karte. |
| 4,3–6,0 s | „oder vereinbare einen Gesprächstermin“ | Karte rechts „Gesprächstermin“ mit Button „Termin vereinbaren“, zweite Linie zur Pille. |
| 6,0–7,07 s | „über dein Portal.“ | Die Pille öffnet sich zu „Physiofit \| Dein Portal“, beide Linien werden Cyan. Endbild. |

## Bearbeiten

- Texte und Farben sind Variablen (Studio → Variablen): beide Kartentitel, Button-Texte, „Dein Portal“, Navy/Petrol/Cyan.
- Timing: `compositions/ende.html`; die Kommentare nennen die Zeiten der gesprochenen Wörter.

## Footage neu erzeugen

Das umkodierte Footage liegt nicht im Repo. Aus dem Original-Clip:

```bash
ffmpeg -i PatientenaufnahmeTeil_8_Ende.mov -c:v libx264 -crf 14 -preset slow -g 30 -keyint_min 30 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -c:a aac -b:a 192k -movflags +faststart assets/footage/patientenaufnahme-teil8.mp4
```

## Prüfen und rendern

```bash
npx hyperframes check
```

```bash
npx hyperframes render --quality looks --output renders/patientenaufnahme-teil-8.mp4
```
