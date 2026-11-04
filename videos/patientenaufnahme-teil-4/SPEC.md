# SPEC – Patientenaufnahme, Teil 4 (Aufnahmeformular einrichten)

GOAL:    Die Praxis sieht, wie das digitale Aufnahmeformular entsteht: Stammdaten, Behandlungsvertrag, Hinweise mit
         Pflicht-Bestätigung, und die Patientin bzw. der Patient signiert am Ende per Checkbox.
         Komplett Vollbild; Benaja ist nur zu hören (wie Teil 7, angenommen).
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps. Ohne Musik und Soundeffekte, nur der O-Ton.
TIME:    19,43 s x 30 = 583 Frames. Takt = O-Ton (`transcript.json`).

LOOK:    wie Teil 1, Teil 7 und `finales_video.mp4`: Grund #F0F4F6 · Karten #FFFFFF, Radius 30–34 px ·
         Navy #1E3542 · Petrol #217C93 · Icon-Kreis #DDF2F9 · Cyan #00BAE7 (Haken-Abzeichen) ·
         Button-Verlauf #0084AB → #00A3CF (kontrastsicher) · Lora 500 Titel · Ubuntu 500 UI ≥ 28 px · Lucide-Icons.
         Stärker abstrahiert (Wunsch): keine Fenster-Kopfzeile, kein Logo, keine Dateinamen oder Schalter, sondern die
         Karten-Sprache aus Teil 1 (Titel, Navy-Balken, die sich füllen, hellblaue Hinweis-Balken, Augen- und Haken-Abzeichen).
OBJECTS: Karte „Patientenaufnahme“: Balken „Stammdaten“ (Name · Adresse · Geburtsdatum darunter) · Balken
         „Behandlungsvertrag“ mit Haken · Hinweis-Balken „Zuzahlung“ / „Ausfallgebühren“ mit Auge (gesehen) und Haken
         (akzeptiert) · Smartphone (Patientensicht) mit zwei Checkboxen, ohne Button
MOTION:  wie Teil 7: Ankunft expo.out 0,4–0,55 s mit Blur → 0 · Abgang power2.in 0,2 s · Upload linear ·
         Balken-Füllung clip-path power3.out · Abzeichen 0,4 s expo.out · ein Bild, das sich aufbaut (keine Schnitte) · Übergang zur Patientensicht:
         Fenster schrumpft nach links (0,6 s power3.inOut), Smartphone gleitet rechts herein.
SHOTS:
  0,0–3,7    Karte „Patientenaufnahme“, Balken „Stammdaten“ (0,45): Name (1,52) · Adresse (2,0) · Geburtsdatum (2,72).
  3,7–6,3    Balken „Behandlungsvertrag“ füllt sich wie ein Upload (4,4), Haken (5,3).
  6,3–10,6   Hinweis-Balken: „Zuzahlung“ (8,88) · „Ausfallgebühren“ (9,76).
  10,6–14,3  Augen-Abzeichen (12,64 „gesehen“) · Haken-Abzeichen (13,44 „akzeptiert“).
  14,3–19,43 Fenster schrumpft nach links, rechts das Smartphone: „Rechtssicher“ (15,76), Checkboxen werden
             angehakt (17,6 / 18,3); kein Button (Wunsch). Checkbox-Texte Ubuntu 400, 24 px, mittig zur Checkbox.
BANNED:  dunkler Grund, Glow, Partikel, Glas, Verläufe außer dem Button, Klick-Ringe, schwebende Loops,
         Logo in der Ecke, erfundene Kennzahlen oder Daten.
QA:      3,3 · 5,9 · 10,2 · 13,9 · 19,2
