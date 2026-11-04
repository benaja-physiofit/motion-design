# REVIEW – Patientenaufnahme, Teil 8 (Ende)

## Kreative Entscheidungen

- Zuerst exakt nach dem freigegebenen Storyboard gebaut, danach nach Feedback reduziert: Physiofit-Pille (auch „Physiofit |
  Dein Portal“) und beide Verbindungslinien entfernt; die Karten zeigen nur noch je einen Button („Nachricht schreiben“
  links, „Termin vereinbaren“ rechts). Titel und Icon-Kreise sind weg, die Karten sind auf den Button verkleinert
  (34 px Innenabstand rundum), Positionen und Seiten wie vorher.
- Benaja bleibt durchgehend im Bild, kein Vollbild-Schnitt. 0–2,85 s ist bewusst ohne Grafik, damit die Buttons als
  Antwort auf die Frage kommen.
- Die linke Karte landet mit dem Button schon darauf (kein grauer Platzhalter mehr), die rechte gleitet von rechts
  herein; beide Buttons werden auf dem jeweiligen Wort kurz eingedrückt (kein Tipp-Ring).
- Button-Cyan dunkler als in der Referenz (#0088B2 → #00A0CC statt #009FC8 → #00CFFD): Mit dem Original-Verlauf hatte der
  weiße Text nur 2,3:1 Kontrast (`check`-Fehler), jetzt ≥ 3:1.
- Keine Verlängerung über die Cliplänge hinaus; das Endbild hält bis zum letzten Frame.

## Gemessen vs. nur angesehen

- `check`: 0 Fehler, 0 Warnungen außer GPU-Konsolenmeldungen der Software-Darstellung.
- Angesehen: Standbilder bei 1,5 / 2,95 / 3,3 / 3,65 / 4,45 / 5,0 / 5,42 / 7,03 s und ein dekodiertes Kontaktblatt des Renders.
- Render: 7,0667 s, 212 Frames, gleich lang wie der Original-Clip.
- Ton: nur der O-Ton, Pegel gemessen (Render −26,7 dB Mittel / −8,4 dB Spitze, Original −26,6 / −8,0). Nicht gehört.

## Schwächste Stelle

- „über dein Portal“ hat kein eigenes Bild mehr; das Endbild (beide Buttons) steht ab 5,8 s still bis zum Clipende.
  Für ein ruhigeres Ende das Endbild im Schnitt 1–2 s als Standbild stehen lassen.
- Die Storyboard-Standbilder unter `boards/stills/` zeigen noch den Stand vor dem Feedback.
