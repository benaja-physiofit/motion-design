# SPEC – Patientenaufnahme, Teil 8 (Ende)

GOAL:    Die Praxis weiß am Ende, wie sie Hilfe für die Einrichtung bekommt: Nachricht schreiben oder Termin vereinbaren.
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps. Ohne Musik und Soundeffekte (Wunsch), nur der O-Ton.
TIME:    7,06 s x 30 = 212 Frames. Takt = O-Ton (Wortzeiten aus `transcript.json`).

LOOK:    wie die Abschluss-Karten in `finales_video.mp4` (110–114 s), reduziert auf den Button (Feedback):
         Karte #FFFFFF, Radius 18 px, Innenabstand 34 px rundum, Schatten 0 24 48 -12 rgba(30,53,66,.18) + 0 4 12 rgba(30,53,66,.06)
         Button: Verlauf #0088B2 → #00A0CC (dunkler als die Referenz, damit weißer Text 3:1 Kontrast hat),
         Schatten 0 14 28 -10 rgba(0,186,231,.6), Höhe 92 px, Ubuntu 700 40 px weiß, Lucide-Icon weiß, Strich 2
         Footage: LUT `friendly-saas-explainer-patientenaufnahme2.cube` (Intensität 1) über media-treatment
         (Wand hier RGB 217/215/210, nah an Clip 2 mit 214/212/208).
LAYOUT:  Benaja bleibt immer im Bild, kein Vollbild-Schnitt. Karte links 74,200 · 562×160 (Button 494 breit);
         Karte rechts 1222,200 · 624×160 (Button 556 breit).
OBJECTS: Button „Nachricht schreiben“ (Sprechblase) · Button „Termin vereinbaren“ (Kalender)
MOTION:  Karte links landet mit Button: Opacity 0 → 1, Scale 0,94 → 1, y 20 → 0, Blur 12 → 0 (expo.out 0,55 s) ·
         Karte rechts gleitet von rechts: x 50 → 0, Blur 12 → 0 (expo.out 0,55 s) ·
         Antippen: Button 1 → 0,97 → 1 (0,1 s power2.out + 0,3 s expo.out), kein Tipp-Ring · keine Abgänge, Endbild hält.
SHOTS:
  0,00–2,85  Nur Benaja: „Wenn du Hilfe bei der einmaligen Einrichtung benötigst“.
  2,85–4,32  Karte links „Nachricht schreiben“ landet (2,85) · Antippen (3,6, „Nachricht“).
  4,32–6,00  Karte rechts „Termin vereinbaren“ gleitet herein (4,32, „vereinbare“) · Antippen (5,36, „Gesprächstermin“).
  6,00–7,06  Beide Buttons stehen. Endbild.
BANNED:  Vollbild-Schnitte (Wunsch), Physiofit-Pille und Verbindungslinien (Feedback), Titel/Icon-Kreise in den Karten
         (Feedback), dunkler Grund, Glow, Partikel, Glas, Logo in der Ecke, Tipp-Ringe, schwebende Loops.
QA:      1,5 · 2,95 · 3,3 · 3,65 · 4,45 · 5,0 · 5,42 · 7,03
