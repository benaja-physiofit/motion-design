# REVIEW – Patientenaufnahme, Teil 1

## Kreative Entscheidungen

- Stil 1:1 aus `finales_video.mp4` übernommen: weiße Karten auf dem Footage, die als Skeleton landen und sich dann füllen,
  harte Schnitte auf eine Vollbild-Karte und zurück, Navy-Balken mit Haken, Lora + Ubuntu, Lucide-Icons in Petrol.
- Rhythmus wie in der Referenz: Karte links → Karten rechts → Vollbild → Karte links (Heimat-Position).
- Jeder Satz bekommt ein eigenes Bild statt einer Liste: Papierbogen mit Kuli/Scan/Tippen, Uhr mit leerlaufendem Balken,
  Zeitstrahl Termin → Start, Dokument-Balken mit Unterschrift, Sanduhr + Suche.
- Keine erfundenen Zahlen: „zu spät“, „Jahrelang“ und „Max Muster“ sind die einzigen Zusatz-Texte; Uhrzeiten oder
  Aufbewahrungsfristen wurden bewusst weggelassen, weil der O-Ton keine nennt.
- Kein Physiofit-Logo: Teil 1 beschreibt nur das Problem. Laut Story-Regel landet die Marke einmal, mit Gewicht, wenn
  die Lösung kommt (Teil 2). Logos liegen unter `assets/brand/` bereit.
- Footage mit `friendly-saas-explainer-patientenaufnahme2.cube` gegradet. Der erste LUT machte diesen helleren Clip fast weiß
  (Wand ≈ 237) mit leichtem Grünstich (R−G −4); die Variante gleicht Weißabgleich und 35 % der Belichtung an (Wand ≈ 233, neutral).
  Das finale Video nutzt noch den wärmeren Original-Look.

## Gemessen vs. nur angesehen

- `check`: 0 Fehler. Zwei Warnungen bewusst behalten (siehe unten).
- Angesehen: Standbilder an allen QA-Zeitpunkten aus `SPEC.md`, Schnitt-Streifen an 0,25 / 6,55 / 12,0 / 17,15 s,
  Handy-Ansicht (360 px).
- Ton: nur der O-Ton des Clips, unverändert (Pegel 1). Nicht gehört, nur durchgereicht.

## Schwächste Stelle

- 19,44–20,4 s: Die Suche „Behandlungsvertrag“ und der Treffer-Ring stehen nur ca. 0,6 s, weil der Clip endet.
  Im Gesamtschnitt läuft Teil 2 direkt weiter; dort könnte die Karte noch 1–2 s stehen bleiben oder in die Lösung übergehen.

## Bewusst behaltene Warnungen

- `line_unread` „Max Muster“: Das ist getippter UI-Text, kein Lese-Satz; der Checker zählt jeden Buchstaben als Wort.
- `line_unread` letzte Zeile: siehe „Schwächste Stelle“, der Clip endet hier, der Film geht in Teil 2 weiter.
