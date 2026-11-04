# SPEC – Patientenaufnahme, Teil 7 (Konfigurator)

GOAL:    Die Praxis sieht: Mit dem Physiofit-Konfigurator baut man eigene Formulare, z. B. Check-in und Feedback.
         Ab 0,85 s komplett Vollbild; Benaja ist in diesem Teil nur am Anfang zu sehen (Wunsch).
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps. Ohne Musik und Soundeffekte, nur der O-Ton.
TIME:    13,56 s x 30 = 407 Frames. Takt = O-Ton (`transcript.json`).

LOOK:    wie Teil 1 und `finales_video.mp4`:
         Vollbild-Grund #F0F4F6 · Karten #FFFFFF, Radius 30–34 px, Schatten 0 24 48 -12 rgba(30,53,66,.18) + 0 4 12 rgba(30,53,66,.06)
         Navy #1E3542 · Petrol #217C93 · Icon-Kreis #DDF2F9 · Cyan #00BAE7 (Button-Verlauf #00A4CC → #00CFFD, Haken, Auswahl)
         Skeleton #EDF1F3 / #CDD6DC · Titel Lora 500 · UI Ubuntu 500 ≥ 28 px · Lucide-Icons Petrol, Strich 2
         Physiofit-Logo (BlueDark, offizielles SVG) einmal: im Kopf des Konfigurators.
         Footage: LUT `friendly-saas-explainer-patientenaufnahme2.cube` (Wand hier 217/215/210 ≈ Clip 2).
OBJECTS: Konfigurator-Fenster mit Bausteinen (Textfeld, Auswahl, Skala, Unterschrift) und Formular-Fläche ·
         Maus-Cursor, der Bausteine zieht · Speichern-Button · Check-in-Karte mit Skala 1–5 ·
         Feedback-Karte mit 5 Sternen und eingehenden Antworten
MOTION:  wie Teil 1: Ankunft expo.out 0,45–0,6 s mit Blur → 0 · Abgang power2.in 0,2 s ·
         Ziehen: Cursor + Baustein 0,5 s power3.inOut, Landung im Formular 0,35 s expo.out ·
         Formular baut sich in einem Bild um (keine Schnitte innerhalb des Konfigurators) ·
         Schnitte Vollbild ↔ Sprecher hart, neues Bild landet 104 % → 100 %.
SHOTS:
  0,0–0,85   Benaja im Bild, noch ohne Grafik („Du kannst mit unserem …“).
  0,85–4,3   `konfigurator` Harter Schnitt auf Vollbild: „Formular-Konfigurator“ mit Physiofit-Logo. Der Cursor zieht
             Textfeld (1,6) · Auswahl (2,4) · Skala (3,2) in ein leeres Formular („ganz individuelle Formulare“).
  4,3–7,25   gleiches Bild baut sich um: Titel wird „Check-in“ (5,85), Felder bekommen echte Fragen,
             Klick auf Speichern → „Gespeichert“ (6,96 „erstellen“).
  7,25–10,1  `checkin`  Vollbild, ohne Benaja (Wunsch): Der Konfigurator tritt zurück, Karte „Check-in“ (1,3×) links,
             rechts die Termine mit Check-in, „Heute“ läuft (8,0 „bei jedem Termin“), Wert gewählt (8,72 „Wohlbefinden“).
  10,1–13,56 `feedback` Vollbild: Die Termine machen Platz, rechts „Feedback“ · „Patientenzufriedenheit“ (1,3×, 11,84):
             Sterne füllen sich, Antworten stapeln sich, Zähler zählt mit (12,96 „einsammeln“). Check-in bleibt links.
BANNED:  dunkler Grund, Glow, Partikel, Glas, Verläufe außer dem Button-Verlauf der Referenz, Klick-Ringe,
         schwebende Loops, Logo in der Ecke, erfundene Kennzahlen (Durchschnittsnoten, Prozent).
QA:      0,5 · 3,9 · 6,9 · 9,7 · 13,3
