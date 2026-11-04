# SPEC – Patientenaufnahme, Teil 4 (Aufnahmeformular einrichten)

GOAL:    Die Praxis sieht, wie das digitale Aufnahmeformular entsteht: Stammdaten, Behandlungsvertrag, Hinweise mit
         Pflicht-Bestätigung, und die Patientin bzw. der Patient signiert am Ende per Checkbox.
         Komplett Vollbild; Benaja ist nur zu hören (wie Teil 7, angenommen).
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps. Ohne Musik und Soundeffekte, nur der O-Ton.
TIME:    19,43 s x 30 = 583 Frames. Takt = O-Ton (`transcript.json`).

LOOK:    wie Teil 1, Teil 7 und `finales_video.mp4`: Grund #F0F4F6 · Karten #FFFFFF, Radius 30–34 px ·
         Navy #1E3542 · Petrol #217C93 · Icon-Kreis #DDF2F9 · Cyan #00BAE7 (Haken, Schalter an, Fortschritt) ·
         Button-Verlauf #0084AB → #00A3CF (kontrastsicher) · Lora 500 Titel · Ubuntu 500 UI ≥ 28 px · Lucide-Icons.
         Physiofit-Logo einmal im Kopf des Formular-Fensters. Abstrahiert, keine echten Screens.
OBJECTS: Formular-Fenster „Patientenaufnahme“ mit drei Abschnitten (Stammdaten · Behandlungsvertrag · Hinweise) ·
         Datei-Zeile mit Upload-Balken · Hinweis-Zeilen mit Schalter „Bestätigung nötig“ ·
         Smartphone (Patientensicht) mit zwei Checkboxen und Button „Digital signieren“
MOTION:  wie Teil 7: Ankunft expo.out 0,4–0,55 s mit Blur → 0 · Abgang power2.in 0,2 s · Upload linear ·
         Schalter 0,25 s power3.out · ein Bild, das sich aufbaut (keine Schnitte) · Übergang zur Patientensicht:
         Fenster schrumpft nach links (0,6 s power3.inOut), Smartphone gleitet rechts herein.
SHOTS:
  0,0–3,7    Fenster „Patientenaufnahme“, Abschnitt Stammdaten: Name (1,52) · Adresse (2,0) · Geburtsdatum (2,72).
  3,7–6,3    Behandlungsvertrag: Datei landet in der Ablage (4,4), Upload läuft, „Hochgeladen“ (5,4).
  6,3–10,6   Hinweise: „Gesetzliche Zuzahlung“ (8,88) · „Ausfallgebühren“ (9,76).
  10,6–14,3  Schalter „Bestätigung nötig“ gehen an (12,64 „gesehen“ · 13,44 „akzeptiert“).
  14,3–19,43 Fenster schrumpft nach links, rechts das Smartphone: „Rechtssicher“ (15,76), Checkboxen werden
             angehakt (17,3 / 18,4), Button wird „Signiert“ (18,8 „Checkbox“).
BANNED:  dunkler Grund, Glow, Partikel, Glas, Verläufe außer dem Button, Klick-Ringe, schwebende Loops,
         Logo in der Ecke, erfundene Kennzahlen oder Daten.
QA:      3,3 · 5,9 · 10,2 · 13,9 · 19,2
