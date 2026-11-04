---
format: 1920x1080
duration: 7.06s
message: "Hilfe bei der Einrichtung: Nachricht schreiben oder Termin vereinbaren."
arc: Frage → Nachricht → Termin → Endbild
audience: Physiotherapie-Praxen (Inhaber:innen und Empfang)
---

Benaja bleibt in allen Einstellungen im Bild; es gibt keinen Vollbild-Schnitt. Ton: nur O-Ton, keine Musik, keine Soundeffekte.

Nach dem ersten Render geändert (Feedback): Physiofit-Pille und die beiden Verbindungslinien sind entfernt, die Karten
zeigen nur noch je einen Button („Nachricht schreiben“, „Termin vereinbaren“); Titel und Icon-Kreise sind weg.
Die Standbilder unter `boards/stills/` zeigen noch den freigegebenen Stand vor diesem Feedback.

## Frame 1: Hilfe bei der Einrichtung (0-2.85s)

- act: Akt 1: Hilfe anbieten
- status: animated
- src: compositions/ende.html
- duration: 2.85s
- poster: 1.5
- transition_in: cut
- scene: Nur Benaja, noch keine Karte
- voiceover: "Wenn du Hilfe bei der einmaligen Einrichtung benötigst,"
- reads: Benaja spricht die Frage (0-2.85s)
- sound: nur O-Ton

Bewusst leer, damit die beiden Buttons als Antwort auf die Frage kommen.

## Frame 2: Nachricht schreiben (2.85-4.32s)

- act: Akt 1: Hilfe anbieten
- status: animated
- src: compositions/ende.html
- duration: 1.47s
- poster: 3.3
- transition_in: cut
- scene: Karte links mit dem Cyan-Button „Nachricht schreiben“, wird angetippt
- voiceover: "schreib uns eine Nachricht"
- reads: Karte mit „Nachricht schreiben“ landet (2.85-3.4s); Antippen (3.6-4.0s)
- sound: nur O-Ton

## Frame 3: Termin vereinbaren (4.32-6.0s)

- act: Akt 2: Termin
- status: animated
- src: compositions/ende.html
- duration: 1.68s
- poster: 5.0
- transition_in: cut
- scene: Karte rechts mit dem Cyan-Button „Termin vereinbaren“, wird angetippt
- voiceover: "oder vereinbare einen Gesprächstermin"
- reads: Karte mit „Termin vereinbaren“ gleitet von rechts herein (4.32-4.9s); Antippen (5.36-5.76s)
- sound: nur O-Ton

## Frame 4: Endbild (6.0-7.06s)

- act: Akt 2: Termin
- status: animated
- src: compositions/ende.html
- duration: 1.06s
- poster: 6.9
- transition_in: cut
- scene: Beide Buttons stehen links und rechts neben Benaja
- voiceover: "über dein Portal."
- reads: beide Buttons stehen still bis zum Clipende (6.0-7.06s)
- sound: nur O-Ton

Endbild des Gesamtvideos; der Clip wird nicht verlängert.
