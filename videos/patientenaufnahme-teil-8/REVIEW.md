# REVIEW – Patientenaufnahme, Teil 8 (Ende)

## Kreative Entscheidungen

- Gebaut exakt nach dem freigegebenen Storyboard (4 Frames). Benaja bleibt durchgehend im Bild, kein Vollbild-Schnitt.
- Kartenpositionen und -aufbau wie die Endkarten im finalen Video („Fragen zur Abrechnung?“ / „Kurze Sprechstunde“).
- Die Physiofit-Pille mit dem Original-Logo erscheint auf „uns“ und öffnet sich auf „über dein Portal“; die Marke landet
  damit einmal, am Ende des Gesamtvideos. Linien wie in den Flussdiagrammen der Referenz verbinden sie mit beiden Karten.
- Kein Tipp-Ring: Das Antippen ist ein kurzes Eindrücken des Buttons (0,97). Das behebt auch, dass im Storyboard der Ring
  das Button-Icon an den Text drückte.
- Button-Cyan dunkler als in der Referenz (#0088B2 → #00A0CC statt #009FC8 → #00CFFD): Mit dem Original-Verlauf hatte der
  weiße Button-Text nur 2,3:1 Kontrast (`check`-Fehler), jetzt ≥ 3:1.
- Texte genau wie im Storyboard; keine Verlängerung über die Cliplänge hinaus.

## Gemessen vs. nur angesehen

- `check`: 0 Fehler, 1 Warnung (siehe unten).
- Angesehen: `snapshot --review` (Beat- und Handy-Blatt), Stichproben bei 0,66 / 0,72 / 3,45 / 3,7 / 4,5 / 5,5 / 6,1 / 7,03 s,
  dekodiertes Kontaktblatt und die ersten Frames des Renders.
- Render: 7,0667 s, 212 Frames, gleich lang wie der Original-Clip.
- Ton: nur der O-Ton, Pegel gemessen (Render −26,7 dB Mittel / −8,4 dB Spitze, Original −26,6 / −8,0). Nicht gehört.

## Schwächste Stelle

- „Dein Portal“ steht nur ≈ 1 s bis zum Clipende (Pille öffnet 5,98 s, kurz vor „über“). Für ein ruhigeres Ende das
  Endbild im Schnitt 1–2 s als Standbild stehen lassen.

## Bewusst behaltene Warnung

- `line_unread` „Dein Portal“: letzte Zeile unter 2 s, weil der Clip nach „Portal“ endet und nicht verlängert werden sollte.
