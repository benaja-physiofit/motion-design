"""Physiofit Szene 1 — 13 s music bed, rendered offline from GeneralUser GS.

Arc (PAS): A-minor tension under the two stats -> lift under the question ->
C-major payoff on "Alles in einer App." Downbeats sit on the picture beats:
0.55 s (count-up starts) ... 7.64 s (circle) ... 10.0 s (flood) ... 12.36 s (button).
"""
import sys
import numpy as np
import soundfile as sf
import tinysoundfont

SF2, OUT = sys.argv[1], sys.argv[2]
SR = 48000
TOTAL = 13.0
T0 = 0.55          # bar 0 downbeat
BAR = (10.0 - T0) / 4  # 2.3625 s  -> 101.6 BPM
BEAT = BAR / 4


def t(bar, beat=0.0):
    return T0 + bar * BAR + beat * BEAT


# channel -> (bank, preset, drums)
CH = {
    "pad": (0, 0, 89, False),      # Pad 2 (warm)
    "piano": (1, 0, 0, False),     # Acoustic Grand
    "strings": (2, 0, 49, False),  # Slow strings
    "bass": (3, 0, 38, False),     # Synth Bass 1
    "bell": (4, 0, 11, False),     # Vibraphone (payoff sparkle)
    "drums": (9, 128, 25, True),   # TR-808 kit
}

events = []  # (time, kind, chan, key, vel)


def note(inst, key, start, dur, vel):
    ch = CH[inst][0]
    events.append((start, 1, ch, key, vel))
    events.append((start + dur, 0, ch, key, 0))


def hit(key, start, vel, dur=0.2):
    note("drums", key, start, dur, vel)


KICK, SNARE, CLAP, CHH, OHH, CRASH, RIDE, TOM = 36, 38, 39, 42, 46, 49, 51, 45

# ---- Pre-roll + bars 0-2: tension in A minor (Am | F | Dm  E) ----
chords = [
    (-0.233, 0, 4, [57, 60, 64], 45),   # Am (pad swells in from t=0)
    (1, 0, 4, [53, 57, 60], 33),       # F
    (2, 0, 2, [50, 53, 57], 38),       # Dm
    (2, 2, 2, [52, 56, 59], 40),       # E (dominant pull)
]
for bar, beat, beats, keys, root in chords:
    start = 0.0 if bar < 0 else t(bar, beat)
    end = t(0, 4) if bar < 0 else t(bar, beat + beats)
    for k in keys:
        note("pad", k, start, end - start + 0.15, 58)
    if bar >= 0:
        note("bass", root, t(bar, beat), BEAT * beats * 0.95, 70)

# Piano ostinato in eighths — the "ticking clock" of patients not training
ost = {
    0: [57, 64, 60, 64, 57, 64, 60, 64],
    1: [53, 60, 57, 60, 53, 60, 57, 60],
    2: [50, 57, 53, 57, 52, 59, 56, 59],
}
for bar, seq in ost.items():
    for i, k in enumerate(seq):
        vel = 50 if i % 2 == 0 else 38
        note("piano", k + 12, t(bar, i * 0.5), BEAT * 0.45, vel)

# Light 808 pulse under the stats
for bar in (0, 1, 2):
    hit(KICK, t(bar, 0), 70)
    hit(KICK, t(bar, 2.5), 45)
    for i in range(8):
        hit(CHH, t(bar, i * 0.5), 34 if i % 2 else 44, 0.05)
    if bar >= 1:
        hit(CLAP, t(bar, 1), 40)
        hit(CLAP, t(bar, 3), 46)

# ---- Bar 3: the question — drop, then build (F -> G) ----
for k in [53, 57, 60, 65]:
    note("pad", k, t(3, 0), BEAT * 2 + 0.1, 62)
    note("strings", k, t(3, 0), BEAT * 2 + 0.1, 55)
for k in [55, 59, 62, 67]:
    note("pad", k, t(3, 2), BEAT * 2 + 0.1, 68)
    note("strings", k, t(3, 2), BEAT * 2 + 0.1, 64)
note("bass", 41, t(3, 0), BEAT * 1.9, 72)
note("bass", 43, t(3, 2), BEAT * 1.9, 76)
# heartbeat kick on the beats, accent on "DU" (~8.5 s, beat 1.5)
for b in (0, 1, 1.5, 2, 3):
    hit(KICK, t(3, b), 80 if b == 1.5 else 64)
# snare roll building into the flood at 10.0 s
roll = np.arange(2.0, 4.0, 0.25)
for i, b in enumerate(roll):
    hit(SNARE, t(3, b), int(30 + 70 * (i / (len(roll) - 1)) ** 1.6), 0.08)

# ---- Bar 4: payoff in C major (C | G), "Alles in einer App." ----
hit(CRASH, t(4, 0), 92, 1.5)
for b in (0, 2):
    hit(KICK, t(4, b), 95)
for b in (1, 3):
    hit(CLAP, t(4, b), 78)
for i in range(8):
    hit(CHH, t(4, i * 0.5), 48 if i % 2 else 60, 0.05)
pay = [(0, [60, 64, 67, 72], 36), (2, [59, 62, 67, 71], 43)]
for beat, keys, root in pay:
    for k in keys:
        note("pad", k, t(4, beat), BEAT * 2 + 0.1, 72)
        note("strings", k, t(4, beat), BEAT * 2 + 0.1, 70)
    for i in range(4):
        note("bass", root, t(4, beat + i * 0.5), BEAT * 0.42, 88)
arp = [72, 76, 79, 84, 79, 76, 74, 79]
for i, k in enumerate(arp):
    note("piano", k, t(4, i * 0.5), BEAT * 0.5, 74 if i % 2 == 0 else 62)
    note("bell", k + 12, t(4, i * 0.5), BEAT * 0.4, 38)

# ---- Button: C add9 rings out on the logo hold (12.36 s -> end) ----
end_t = t(5, 0)
hit(CRASH, end_t, 70, 1.2)
hit(KICK, end_t, 90)
for k in [48, 60, 64, 67, 74, 79]:
    note("strings", k, end_t, TOTAL - end_t, 70)
    note("pad", k, end_t, TOTAL - end_t, 66)
note("piano", 84, end_t, TOTAL - end_t, 70)
note("bell", 91, end_t, TOTAL - end_t, 50)
note("bass", 36, end_t, TOTAL - end_t, 85)

# ---- Render ----
synth = tinysoundfont.Synth(gain=-6, samplerate=SR)
sfid = synth.sfload(SF2)
for name, (ch, bank, preset, drums) in CH.items():
    synth.program_select(ch, sfid, bank, preset, is_drums=drums)

events.sort(key=lambda e: (e[0], e[1]))
total_samples = int(TOTAL * SR)
out = np.zeros((total_samples, 2), dtype=np.float32)
pos = 0
for time, kind, ch, key, vel in events:
    target = min(total_samples, int(round(time * SR)))
    if target > pos:
        buf = np.frombuffer(synth.generate(target - pos), dtype=np.float32).reshape(-1, 2)
        out[pos:target] = buf
        pos = target
    if kind == 1:
        synth.noteon(ch, key, vel)
    else:
        synth.noteoff(ch, key)
if pos < total_samples:
    buf = np.frombuffer(synth.generate(total_samples - pos), dtype=np.float32).reshape(-1, 2)
    out[pos:] = buf

# ---- Convolution reverb (synthetic plate, deterministic seed) ----
rng = np.random.default_rng(7)
ir_len = int(1.6 * SR)
decay = np.exp(-np.linspace(0, 6.5, ir_len))
ir = rng.standard_normal((ir_len, 2)) * decay[:, None]
from numpy.fft import rfft, irfft
n = total_samples + ir_len
nfft = 1 << (n - 1).bit_length()
wet = np.zeros((total_samples, 2), dtype=np.float64)
for c in range(2):
    W = irfft(rfft(out[:, c], nfft) * rfft(ir[:, c], nfft), nfft)[:total_samples]
    wet[:, c] = W
wet /= np.max(np.abs(wet)) + 1e-9
dry_peak = np.max(np.abs(out)) + 1e-9
mix = out / dry_peak * 0.8 + wet * 0.22

# Fade in the first 0.4 s and out over the last 0.5 s (cut at 13.0 s)
env = np.ones(total_samples)
fi = int(0.4 * SR)
env[:fi] = np.linspace(0, 1, fi) ** 2
fo = int(0.5 * SR)
env[-fo:] = np.linspace(1, 0, fo) ** 1.5
mix *= env[:, None]
mix /= np.max(np.abs(mix)) + 1e-9
mix *= 0.89
sf.write(OUT, mix.astype(np.float32), SR, subtype="PCM_24")
print("wrote", OUT, f"{TOTAL}s", f"BPM {60 / BEAT:.1f}", "events", len(events))
