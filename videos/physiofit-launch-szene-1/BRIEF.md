---
workflow: general-video
flow: automation
storyboard: no
message: "70 % der Patienten trainieren nicht zuhause, 100 % der Therapeuten sind unzufrieden – Physiofit ändert das, alles in einer App."
destination: youtube
aspect: 1920x1080
language: de
audience: Physiotherapeut:innen und Praxisinhaber:innen
length: ~13s (Voiceover bestimmt die Länge)
narration: yes
voice: sherpa-onnx/piper de_DE-thorsten-high
---

## Intent

Szene 1 eines Launch-Videos für die Physiofit-App (Physiofit Digital GmbH). Das Problem
wird mit zwei Zahlen gesetzt: Die Prozentangaben zählen schnell hoch, links auf 70, rechts
auf 100, und eine deutsche KI-Stimme moderiert das Ganze. Der Wortlaut der Nutzerin bzw. des Nutzers:

> 70% der Physio Patienten trainieren nicht zuhause (2. Bild) und 100% (1. Bild) der
> Therapeuten sind damit unzufrieden → was wäre, wenn DU das ändern könntest? → Alles auf einer App

Referenz: Launch-Video https://www.youtube.com/watch?v=SgmuplXU2iY (in dieser Umgebung nicht abrufbar).

## Assets

- assets/patient.png — Bild 2: Patient mit verschränkten Armen auf dem Gymnastikball, transparentes PNG mit blauem Kreis (#607F90). Gehört zu „70 %", links.
- assets/therapeut.png — Bild 1: Therapeut im Physiotherapie-Polo, transparentes PNG mit blauem Kreis. Gehört zu „100 %", rechts.
- assets/logo/physiofit-logo-original.png — Physiofit-Logo (Bildmarke über Wortmarke, weiß auf Navy #1F3542), von der Nutzerin bzw. dem Nutzer geliefert.
- assets/logo/physiofit-mark.svg, assets/logo/physiofit-wordmark.svg — daraus vektorisiert (potrace), damit das Logo auch groß scharf bleibt. Steht im Endbild unter „Alles in einer App.".

## Customizations

- Count-up: 0 → 70 % (Patient) und 0 → 100 % (Therapeut), jeweils schnell und synchron zur Stimme.
- Deutsche KI-Stimme „Thorsten" (offline, Piper via sherpa-onnx), von der Nutzerin bzw. dem Nutzer aus drei Hörproben gewählt.
- Musik (Wunsch der Nutzerin bzw. des Nutzers): eigener 13-s-Track, 101,6 BPM. A-Moll-Spannung unter den Zahlen,
  Aufbau unter der Frage, C-Dur-Auflösung bei „Alles in einer App.", Takt-Einsen auf 0,55 / 7,64 / 10,0 / 12,36 s.
  Unter der Stimme per Voiceover-Carve abgesenkt (Stärke 0,55).
- Soundeffekte (Wunsch der Nutzerin bzw. des Nutzers): Pop beim Patienten-Bild, Zähl-Klicks und Ping bei 70 % / 100 %,
  Whoosh beim Split, beim Auseinanderfahren und bei der Kreisflut, Pop beim Kreis, Bass-Impact auf „DU",
  Riser in die Flut hinein, Sparkle beim Logo.

## Notes

- Unternehmensfarben (von der Nutzerin bzw. dem Nutzer): #60f90 (gelesen als #607F90, das Blau der Foto-Kreise),
  #00B8E1, #102D49, #FAFAFA, #F2FBFD. Verwendung: Hintergrund #F2FBFD · Text und Endbild #102D49 ·
  Foto-Kreise, „DU"-Kreis, „%" und Hervorhebungen #607F90 · Fortschrittsringe #00B8E1 ·
  heller Text auf Dunkel #FAFAFA. Im Endbild ist die Schrift nur weiß, ohne Cyan (Wunsch der Nutzerin bzw. des Nutzers).
- physiofit.app ist in dieser Cloud-Umgebung per Netzwerk-Policy blockiert. Logo und Farben kamen deshalb direkt
  von der Nutzerin bzw. dem Nutzer.
- „Alles in einer App" statt „auf einer App", weil das die übliche Formulierung ist (angenommen, nicht bestätigt).
- Musik: Es ist keine Musikquelle erreichbar (HeyGen nicht angemeldet und api.heygen.com blockiert, Hugging Face für
  MusicGen blockiert). Der Track ist deshalb offline komponiert (audio-src/compose_music.py) mit der Soundfont
  GeneralUser GS v2.0.3 (frei für kommerzielle Musikproduktion; Quelle github.com/mrbumpy409/GeneralUser-GS,
  nicht im Repo, weil 32 MB). Neu rendern: `python3 audio-src/compose_music.py GeneralUser-GS.sf2 music_raw.wav`,
  dann highpass 35 Hz + alimiter 0.89 nach assets/music.wav.
- Soundeffekte stammen aus der mitgelieferten HyperFrames-Bibliothek (Pixabay-Lizenz, assets/sfx/CREDITS.md).
  Die Zähl-Stems baut audio-src/counter_stem.py; sie hängen am Timing des Count-ups (expo.out, 1,2 s).
