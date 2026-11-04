# Patientenaufnahme – Teil 7: Konfigurator

Animationen zum Clip `Patientenaufnahme_Teil_7.mov` (13,6 s), im Stil von Teil 1 und `finales_video.mp4`.
Benaja ist in diesem Teil nicht zu sehen, nur zu hören; alles ist Vollbild (Wunsch). Ohne Musik und Soundeffekte,
nur der O-Ton. Der Konfigurator ist bewusst abstrahiert dargestellt, nicht als echter Screenshot.

| | |
|---|---|
| Format | 1920×1080, 30 fps, 13,56 s, H.264 + AAC |
| Render | `renders/patientenaufnahme-teil-7.mp4` |
| Storyboard | `boards/storyboard.html` (Bild: `boards/storyboard.png`), Plan: `STORYBOARD.md` |
| Plan mit allen Maßen | `SPEC.md` |
| Review-Notizen | `REVIEW.md` |
| Transkript mit Wortzeiten | `transcript.json` |

## Ablauf

| Zeit | Gesprochen | Bild |
|---|---|---|
| 0–4,3 s | „Du kannst mit unserem Konfigurator auch ganz individuelle Formulare erstellen.“ | Vollbild „Formular-Konfigurator“ mit Physiofit-Logo: Der Cursor zieht Skala, Auswahl, Textfeld und Unterschrift ins Formular. |
| 4,3–7,55 s | „So kannst du zum Beispiel ein Check-in-Formular erstellen, …“ | Das Formular wird zum „Check-in“ mit echten Fragen, Klick auf Speichern → „Gespeichert“. |
| 7,55–10,1 s | „… um bei jedem Termin das Wohlbefinden abzufragen, …“ | Karte „Check-in“ links, rechts die Termine mit Check-in; die 4 wird gewählt. |
| 10,1–13,56 s | „… oder allgemeines Feedback zur Patientenzufriedenheit einsammeln.“ | Karte „Feedback · Patientenzufriedenheit“: Sterne füllen sich, Antworten kommen rein. |

## Bearbeiten

- Texte und Farben sind Variablen (Studio → Variablen): Fenster-Titel, Formular-Name, Karten-Titel, Frage, Chip.
- Timing: jede Szene in `compositions/<szene>.html`; die Kommentare nennen die Filmzeit der Wörter.
- LUT: `friendly-saas-explainer-patientenaufnahme2.cube` am `#footage`-Video (das Video liegt nur noch für den Ton darunter).

## Footage neu erzeugen

Das umkodierte Footage liegt nicht im Repo. Aus dem Original-Clip:

```bash
ffmpeg -i Patientenaufnahme_Teil_7.mov -c:v libx264 -crf 14 -preset slow -g 30 -keyint_min 30 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -c:a aac -b:a 192k -movflags +faststart assets/footage/patientenaufnahme-teil7.mp4
```

## Prüfen und rendern

```bash
npx hyperframes check
```

```bash
npx hyperframes render --quality delivery --output renders/patientenaufnahme-teil-7.mp4
```
