# SPEC – Patientenaufnahme, Teil 8 (Ende)

GOAL:    Die Praxis weiß am Ende, wo sie Hilfe für die Einrichtung bekommt: Nachricht oder Gesprächstermin, über das Portal.
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps. Ohne Musik und Soundeffekte (Wunsch), nur der O-Ton.
TIME:    7,06 s x 30 = 212 Frames. Takt = O-Ton (Wortzeiten aus `transcript.json`).

LOOK:    wie Teil 1 und die Abschluss-Karten in `finales_video.mp4` (110–114 s):
         Karten #FFFFFF, Radius 18 px, Schatten 0 24 48 -12 rgba(30,53,66,.18) + 0 4 12 rgba(30,53,66,.06)
         Tinte/Navy #1E3542 · Petrol #217C93 (Icons, Linien) · Icon-Kreis #DDF2F9 · Skeleton #EDF1F3
         Buttons: Verlauf #0088B2 → #00A0CC (dunkler als die Referenz, damit weißer Text 3:1 Kontrast hat), Schatten 0 14 28 -10 rgba(0,186,231,.6), Ubuntu 700 40 px weiß
         Titel: Lora 500 46 px · UI-Text: Ubuntu 500/700 · Icons: Lucide, Strich 2
         Physiofit-Logo: offizielle SVG (BlueDark), 38 px hoch, in einer weißen Pille oben mittig
         Footage: LUT `friendly-saas-explainer-patientenaufnahme2.cube` (Intensität 1) über media-treatment
         (Wand hier RGB 217/215/210, nah an Clip 2 mit 214/212/208).
LAYOUT:  Benaja bleibt immer im Bild, kein Vollbild-Schnitt. Karte links 74,200 · 562×316; Karte rechts 1222,200 · 624×316
         (Positionen der Referenz). Pille oben mittig, y 30–118, über Benajas Kopf (Haaransatz ≈ y 160).
OBJECTS: Rettungsring (Hilfe) · Nachricht-Button · Gespräch-Icon · Kalender-Button · Physiofit-Pille · Verbindungslinien mit Knoten
MOTION:  Karte landet als Skeleton, Inhalt per Blur 8 → 0 (expo.out 0,3–0,5 s) · Button-Füllung clip-path power3.out 0,5 s ·
         Antippen: Button 1 → 0,97 → 1 (0,1 s + 0,3 s), kein Tipp-Ring · Linien zeichnen sich per stroke-dashoffset 0,45 s power2.inOut ·
         Pille öffnet sich nach rechts (clip-path + x, 0,45 s expo.out) · Linien Petrol → Cyan 0,3 s.
SHOTS:
  0,00–2,85  Karte links „Hilfe bei der Einrichtung?“ landet (0,15) und füllt sich (0,7); Button-Platzhalter.
  2,85–4,30  Button „Nachricht schreiben“ füllt sich (2,9) · Physiofit-Pille + Linie links (3,2) · Tipp (3,6).
  4,30–6,15  Karte rechts „Gesprächstermin“ (4,3) · Button „Termin vereinbaren“ (4,6) · Linie rechts (4,6) · Tipp (5,4).
  5,98–7,06  Pille öffnet sich zu „Physiofit | Dein Portal“ (5,98, kurz vor „über“) · beide Linien Cyan (6,2). Endbild.
BANNED:  Vollbild-Schnitte (Wunsch), dunkler Grund, Glow, Partikel, Glas, Logo in der Ecke, Text der sich beim Lesen bewegt,
         alles gleichzeitig einblenden.
         Erlaubt, weil die Referenz es so nutzt: Serif-Titel, Pill-Buttons.
QA:      1,0 · 2,3 · 3,9 · 5,7 · 6,9 · 7,03
