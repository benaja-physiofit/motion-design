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

## Customizations

- Count-up: 0 → 70 % (Patient) und 0 → 100 % (Therapeut), jeweils schnell und synchron zur Stimme.
- Deutsche KI-Stimme „Thorsten" (offline, Piper via sherpa-onnx), von der Nutzerin bzw. dem Nutzer aus drei Hörproben gewählt.

## Notes

- physiofit.app ist in dieser Cloud-Umgebung per Netzwerk-Policy blockiert. Logo und exakte Markenfarben
  fehlen deshalb noch. Bis dahin stammt die Farbe aus den Bildern (#607F90), und am Ende steht ein
  „Physiofit"-Schriftzug als Platzhalter, der gegen das echte Logo getauscht wird.
- „Alles in einer App" statt „auf einer App", weil das die übliche Formulierung ist (angenommen, nicht bestätigt).
- Keine Musik (nicht angefragt).
