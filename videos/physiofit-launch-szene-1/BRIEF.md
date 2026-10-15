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

## Notes

- Unternehmensfarben (von der Nutzerin bzw. dem Nutzer): #60f90 (gelesen als #607F90, das Blau der Foto-Kreise),
  #00B8E1, #102D49, #FAFAFA, #F2FBFD. Verwendung: Hintergrund #F2FBFD · Text und Endbild #102D49 ·
  Foto-Kreise, „DU"-Kreis, „%" und Hervorhebungen #607F90 · Fortschrittsringe und „App." #00B8E1 ·
  heller Text auf Dunkel #FAFAFA.
- physiofit.app ist in dieser Cloud-Umgebung per Netzwerk-Policy blockiert. Logo und Farben kamen deshalb direkt
  von der Nutzerin bzw. dem Nutzer.
- „Alles in einer App" statt „auf einer App", weil das die übliche Formulierung ist (angenommen, nicht bestätigt).
- Keine Musik (nicht angefragt).
