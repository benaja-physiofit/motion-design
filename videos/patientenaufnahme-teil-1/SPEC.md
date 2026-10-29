# SPEC – Patientenaufnahme, Teil 1 (Problem)

GOAL:    Die Praxis erkennt sich wieder: Papier, Abtippen, Zeitverlust und Aktenberge bei der Aufnahme.
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps. Ohne Musik und Soundeffekte (Wunsch), nur der O-Ton.
TIME:    20,40 s x 30 = 612 Frames. Takt = O-Ton (Wortzeiten aus `transcript.json`).

LOOK:    exakt wie `finales_video.mp4` (Referenz der Nutzerin bzw. des Nutzers):
         Vollbild-Grund #F0F4F6 · Karten #FFFFFF, Radius 30 px, Schatten 0 24 48 -12 rgba(30,53,66,.18) + 0 4 12 rgba(30,53,66,.06)
         Tinte/Navy #1E3542 (Physiofit BlueDark, auch Balken) · Petrol #217C93 (Icons, Linien) · Icon-Kreis #DDF2F9
         Akzent Cyan #00BAE7 nur für Haken, Scan-Linie, Verspätungs-Strecke, Treffer-Ring
         Skeleton #EDF1F3, Skeleton-Striche #CDD6DC
         Titel: Lora 500, 40–80 px · UI-Text: Ubuntu 500, ≥ 28 px · Icons: Lucide, Strich 2, Petrol
         Footage: LUT `friendly-saas-explainer-patientenaufnahme2.cube` (Intensität 1) über media-treatment:
         derselbe Look wie Clip 1, Weißabgleich auf diese Wand (RGB 214/212/208) abgestimmt, Belichtung zu 35 % angeglichen.
OBJECTS: Papierbogen (Papierweiß, 2 px Rand, umgeknickte Ecke, Kugelschreiber-Linien) · Scanner-Linie ·
         Eingabefeld mit Cursor · Uhr mit drehenden Zeigern · Zeitstrahl Termin → Start ·
         Navy-Dokumentbalken mit Unterschrift · Sanduhr · Suchfeld
MOTION:  Ankunft expo.out 0,45–0,6 s mit Blur 10–12 → 0 · Abgang power2.in 0,2–0,25 s (≈ 45 % kürzer) ·
         Balken-Füllung clip-path power3.out 0,55 s · Status-Wechsel als Slot-Roll 0,35 s expo.out ·
         Zeiger linear · Schnitte zum Vollbild hart (wie Referenz), neues Bild landet 104 % → 100 %.
SHOTS:
  0,25–6,50  `aufnahme`  Karte links (80,100 · 480 breit) baut sich vom Skeleton auf: „Patientenaufnahme“ (0,7) ·
             Papierbogen landet (2,15) · Kuli füllt aus (3,2) · Scan-Linie (4,0) · Tippen „Max Muster“ (5,15) ·
             Status-Pill rollt Ausgefüllt → Eingescannt → Abgetippt.
  6,55–12,0  `empfang`   Rechts zwei Karten wie SMS/WhatsApp der Referenz: „Empfang“ mit Uhr, Balken
             „Wertvolle Zeit“ läuft leer (8,0) · „Behandlungsstart“: Start-Punkt rutscht vom Termin weg (9,7),
             Badge „zu spät“ (10,96).
  12,0–17,15 `dokumente` Harter Schnitt auf Vollbild: Karte „Wichtige Dokumente“, drei Balken füllen sich synchron
             zu Behandlungsvertrag (Unterschrift zeichnet sich) · Ausfallgebühr · Weitere Dokumente, je ein Haken.
  17,15–20,4 `archiv`    Harter Schnitt zurück, Karte links (Heimat-Position): „Aufbewahrung“, die drei Dokumente
             fallen hinein, Sanduhr „Jahrelang“ dreht (17,5), Suche „Behandlungsvertrag“ findet ihn (19,44).
BANNED:  dunkler Grund, Glow, Partikel, Glas, Lila-/Blau-Verläufe, schwebende Loops, Logo in der Ecke,
         Text der sich beim Lesen bewegt, alles gleichzeitig einblenden.
         Erlaubt, weil die Referenz es so nutzt: Serif-Titel, Pills, zentrierte Vollbild-Karte.
QA:      1,5 · 3,7 · 4,4 · 6,0 · 8,6 · 11,3 · 12,05 · 13,8 · 16,9 · 18,2 · 20,3
