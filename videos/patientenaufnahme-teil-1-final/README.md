# Patientenaufnahme – Teil 1 (finale Fassung): neues Ende

Grundlage ist `Teil_1_final_.mp4` (abstrakte Animation ohne Footage und ohne Ton, 1920×1080, 60 fps, 20,4 s).
Bis 17,2 s bleibt das Video Bild für Bild unverändert. Ab „müssen jahrelang aufbewahrt werden …“ ist das Ende neu:
Es zeigt jetzt, wie mühsam es ist, nach Jahren das richtige Dokument zu finden (Wunsch der Nutzerin bzw. des Nutzers).

| | |
|---|---|
| Ergebnis | `renders/teil-1-final-neu.mp4` (1920×1080, 60 fps, 20,4 s, kein Ton wie das Original) |
| Original | `assets/original/teil-1-final.mp4` |
| Neues Ende | `compositions/suche.html` (lokale Zeit 0 = 17,2 s), erzeugt von `tools/gen_suche.py` |
| Zusammensetzen | `splice.sh` |

## Ablauf ab 17,2 s

| Zeit | Gesprochen | Bild |
|---|---|---|
| 17,2–17,8 s | „müssen jahrelang …“ | Die drei Karten Behandlungsvertrag, Ausfallgebühr und Andere Dokumente schrumpfen auf einen Stapel. |
| 17,6–19,0 s | „… aufbewahrt werden“ | Links läuft die Jahreszahl 2019 → 2026, immer mehr Blätter fallen auf den Stapel und begraben die drei Karten. |
| 19,1–20,4 s | „und griffbereit sein.“ | Eine Lupe sucht im Stapel; Blatt für Blatt wird herausgezogen, jedes ist das falsche (rotes ✕). Die Suche läuft noch, als der Clip endet. |

## Übergang

Die drei Karten sind 1:1 aus dem letzten ruhigen Bild des Originals (17,18 s) ausgeschnitten, inklusive Schatten
(`assets/cards/`). Das neue Ende wird verlustfrei als PNG-Folge gerendert und zusammen mit dem Original-Anfang in einem
Durchgang kodiert, damit die Farben an der Naht gleich bleiben.

```bash
npx hyperframes render --quality looks --fps 60 --format png-sequence --output renders/ende-frames
```

```bash
./splice.sh
```
