"""Physiofit sonic logo — synthesized, composed frame-accurately to the intro's beats.

Deterministic: same code + seed -> bit-identical WAV. Every cue time below mirrors
the GSAP timelines in compositions/atmosphere.html and compositions/lockup.html.

    0.12–0.795  inhale   reverse-reverb swell of the hit chord + rising air
    0.80        hit      sub drop + felt transient + Dmaj9 bloom pad + glass bell
    1.18–1.85   slide    air whoosh that follows the mark's velocity and pans left
    1.41–1.56   letters  soft harp-like gliss, one note per letter as it slides out from
                         under the tile (times measured: sound/letter-emergence.json)
    1.85        settle   chime, open fifth (D6 + A6)
    1.98–2.95   sweep    sparkle grains + high air following the light pass L->R
    3.05–3.75   exhale   downward air; tails fade to silence at 4.0

Usage:  python3 sound/sonic_logo.py  (writes assets/audio/physiofit-sonic-logo.wav)
Requires numpy + scipy; ffmpeg for loudness measurement and 24-bit encode.
"""

import json
import os
import subprocess
import sys

import numpy as np
from scipy import signal
from scipy.io import wavfile

SR = 48000
DUR = 4.0
N = int(SR * DUR)
SEED = 20261007

# beats (s) — keep in sync with the compositions
HIT = 0.80
SLIDE, SETTLE = 1.18, 1.85
SWEEP = 2.10
EXIT = 3.05

TARGET_LUFS = -15.0
CEILING_DBTP = -1.0

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
OUT_WAV = os.path.join(PROJECT, "assets", "audio", "physiofit-sonic-logo.wav")

rng = np.random.default_rng(SEED)


# ── helpers ──────────────────────────────────────────────────────────────────
def db(x):
    return 10.0 ** (x / 20.0)


def secs(n):
    return np.arange(n) / SR


def norm(x):
    p = np.max(np.abs(x))
    return x / p if p > 0 else x


def env_ar(n, attack, tau, hold=0.0):
    """Raised-cosine attack, optional hold, exponential decay."""
    tt = secs(n)
    a = np.clip(tt / max(attack, 1e-6), 0.0, 1.0)
    a = 0.5 - 0.5 * np.cos(np.pi * a)
    d = np.exp(-np.maximum(tt - attack - hold, 0.0) / tau)
    return a * d


def fade(x, fin=0.0, fout=0.0):
    x = x.copy()
    n = x.shape[-1]
    if fin > 0:
        k = min(n, int(fin * SR))
        x[..., :k] *= 0.5 - 0.5 * np.cos(np.pi * np.arange(k) / k)
    if fout > 0:
        k = min(n, int(fout * SR))
        x[..., n - k :] *= 0.5 + 0.5 * np.cos(np.pi * np.arange(k) / k)
    return x


def svf(x, fc, q=0.707, mode="lp"):
    """Topology-preserving state-variable filter with per-sample cutoff."""
    fc = np.broadcast_to(np.asarray(fc, dtype=float), x.shape)
    g = np.tan(np.pi * np.clip(fc, 10.0, SR * 0.45) / SR)
    k = 1.0 / q
    a1 = 1.0 / (1.0 + g * (g + k))
    a2 = g * a1
    a3 = g * a2
    y = np.empty_like(x)
    ic1 = ic2 = 0.0
    for i in range(x.shape[0]):
        v3 = x[i] - ic2
        v1 = a1[i] * ic1 + a2[i] * v3
        v2 = ic2 + a2[i] * ic1 + a3[i] * v3
        ic1 = 2.0 * v1 - ic1
        ic2 = 2.0 * v2 - ic2
        if mode == "lp":
            y[i] = v2
        elif mode == "bp":
            y[i] = k * v1
        else:
            y[i] = x[i] - k * v1 - v2
    return y


def pan(x, p):
    """Constant-power pan, centre = unity. p scalar or per-sample array in [-1, 1]."""
    p = np.broadcast_to(np.asarray(p, dtype=float), x.shape)
    th = (p + 1.0) * np.pi / 4.0
    return np.stack([np.cos(th) * x, np.sin(th) * x]) * np.sqrt(2.0)


class Bus:
    def __init__(self):
        self.dry = np.zeros((2, N))
        self.send = np.zeros((2, N))

    def add(self, x, at, gain_db, send=0.0, p=0.0):
        if x.ndim == 1:
            x = pan(x, p)
        x = x * db(gain_db)
        i0 = int(round(at * SR))
        j0 = 0
        if i0 < 0:
            j0, i0 = -i0, 0
        n = min(x.shape[1] - j0, N - i0)
        if n <= 0:
            return
        self.dry[:, i0 : i0 + n] += x[:, j0 : j0 + n]
        if send > 0:
            self.send[:, i0 : i0 + n] += send * x[:, j0 : j0 + n]


# ── sources ──────────────────────────────────────────────────────────────────
CHORD = [  # Dmaj9, open voicing: D3 A3 E4 F#4 C#5
    (146.83, 1.00),
    (220.00, 0.72),
    (329.63, 0.58),
    (369.99, 0.52),
    (554.37, 0.36),
]


def warm_voice(f, n, cents, nharm=14, tilt=1.75):
    tt = secs(n)
    fd = f * 2.0 ** (cents / 1200.0)
    out = np.zeros(n)
    for k in range(1, nharm + 1):
        if k * fd > 15000:
            break
        out += np.sin(2 * np.pi * k * fd * tt + rng.uniform(0, 2 * np.pi)) / k**tilt
    return out


def chord_pad(n, bright=1.0):
    """Wide detuned pad; the -6c voices lean left, the +6c voices lean right."""
    L = np.zeros(n)
    R = np.zeros(n)
    for f, a in CHORD:
        for cents, wl, wr in ((-6.0, 0.85, 0.35), (0.0, 0.6, 0.6), (6.0, 0.35, 0.85)):
            v = warm_voice(f, n, cents) * a
            L += v * wl
            R += v * wr
    tt = secs(n)
    cutoff = 950.0 + 4300.0 * bright * np.exp(-tt / 0.32)
    L = svf(L, cutoff, 0.6)
    R = svf(R, cutoff, 0.6)
    return np.stack([L, R])


def fm_bell(f, n, ratio=3.5, index=1.8, index_tau=0.22, tau=0.9, attack=0.002):
    tt = secs(n)
    idx = index * np.exp(-tt / index_tau)
    mod = idx * np.sin(2 * np.pi * f * ratio * tt)
    return np.sin(2 * np.pi * f * tt + mod) * env_ar(n, attack, tau)


def pluck(f, n, tau=0.3):
    tt = secs(n)
    x = (
        np.sin(2 * np.pi * f * tt)
        + 0.22 * np.sin(2 * np.pi * 2 * f * tt)
        + 0.06 * np.sin(2 * np.pi * 3 * f * tt)
    )
    return x * env_ar(n, 0.004, tau)


def noise(n):
    return rng.standard_normal(n)


def sub_drop(n):
    tt = secs(n)
    f = 40.0 + 62.0 * np.exp(-tt / 0.07)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * env_ar(n, 0.0015, 0.34)
    x = np.tanh(1.9 * x) / np.tanh(1.9)  # harmonics so it reads on small speakers
    return svf(x, 320.0, 0.7)


def make_ir(length=2.8, rt60=2.2, predelay=0.022):
    n = int(length * SR)
    tt = secs(n)
    decay = np.exp(-6.9 * tt / rt60)
    chans = []
    for _ in range(2):
        x = noise(n) * decay
        x = svf(x, 9000.0 * np.exp(-tt / 0.9) + 1400.0, 0.6)  # high end dies first
        er = np.zeros(n)
        for d, g in ((0.011, 0.5), (0.019, 0.38), (0.031, 0.3), (0.047, 0.22), (0.063, 0.16)):
            er[int((d + rng.uniform(-0.002, 0.002)) * SR)] = g * rng.choice([-1, 1])
        x = x / np.sqrt(np.sum(x**2)) + er * 0.6
        x = np.concatenate([np.zeros(int(predelay * SR)), x])[:n]
        chans.append(x)
    return np.stack(chans)


IR = make_ir()


def reverb(x):
    return np.stack([signal.fftconvolve(x[c], IR[c])[: x.shape[1]] for c in range(2)])


# ── score ────────────────────────────────────────────────────────────────────
def compose():
    bus = Bus()

    # HIT — Dmaj9 bloom pad
    n = int((DUR - HIT) * SR)
    pad = chord_pad(n) * env_ar(n, 0.006, 1.55)
    bus.add(norm(pad), HIT, -6.0, send=0.38)

    # HIT — glass bell (A5 + E6)
    bell = fm_bell(880.0, n, tau=0.7) + 0.62 * fm_bell(1318.51, n, ratio=3.5, index=1.4, tau=0.6)
    bus.add(norm(bell), HIT, -17.0, send=0.6)

    # HIT — sub drop + felt transient
    bus.add(norm(sub_drop(int(1.6 * SR))), HIT, -6.5)
    m = int(0.06 * SR)
    felt = svf(noise(m), 3200.0, 0.8, "bp") * env_ar(m, 0.0006, 0.006)
    bus.add(norm(felt), HIT, -21.0, send=0.25)

    # INHALE — reverse reverb of the hit chord, ending a hair before the hit
    m = int(0.5 * SR)
    seed_chord = chord_pad(m, bright=0.7) * env_ar(m, 0.004, 0.22)
    tail = reverb(np.pad(seed_chord, ((0, 0), (0, int(2.6 * SR)))))
    energy = np.convolve(np.sum(tail**2, axis=0), np.ones(int(0.01 * SR)), "same")
    rev = tail[:, int(np.argmax(energy)) :][:, ::-1]  # ends on the reverb's loudest moment
    rev = np.stack([svf(c, 110.0, 0.7, "hp") for c in rev])
    swell_len = HIT - 0.005 - 0.12
    k = int(swell_len * SR)
    swell = fade(rev[:, -k:], fin=0.32, fout=0.004)
    bus.add(norm(swell), 0.12, -10.0)

    # INHALE — rising air, decorrelated L/R
    tt = secs(k)
    prog = tt / swell_len
    fc = 420.0 * (7200.0 / 420.0) ** prog
    amp = prog**2.4
    air = np.stack([svf(noise(k), fc, 0.9, "bp"), svf(noise(k), fc, 0.9, "bp")]) * amp
    bus.add(fade(norm(air), fout=0.004), 0.12, -23.0, send=0.15)

    # SLIDE — whoosh shaped by the mark's expo.inOut velocity, panning left with it
    d = SETTLE - SLIDE
    k = int(d * SR)
    p = secs(k) / d

    def expo_inout(u):
        u = np.clip(u, 0, 1)
        return np.where(u < 0.5, 2.0 ** (20 * u - 10) / 2, (2 - 2.0 ** (-20 * u + 10)) / 2)

    pos = expo_inout(p)
    vel = np.gradient(pos)
    vel = (vel / vel.max()) ** 0.45
    fc = 380.0 + 2300.0 * vel
    wh = svf(noise(k), fc, 1.1, "bp") * vel
    bus.add(fade(norm(wh), 0.01, 0.02), SLIDE, -21.0, send=0.25, p=-0.45 * pos)

    # LETTERS — soft harp gliss, D-major pentatonic, rising as each letter slides out from
    # under the tile (last letter first); each note panned to its letter's resting position
    with open(os.path.join(HERE, "letter-emergence.json")) as fh:
        lm = json.load(fh)
    order = sorted(range(len(lm["emerge_s"])), key=lambda i: lm["emerge_s"][i])
    notes = [440.0, 493.88, 587.33, 659.26, 739.99, 880.0, 987.77, 1174.66, 1318.51]
    for j, i in enumerate(order):
        f = notes[min(j, len(notes) - 1)]
        m = int(1.2 * SR)
        x = svf(pluck(f, m, tau=0.34), 5200.0, 0.7)
        p = float(np.clip((lm["rest_center_x"][i] - 960.0) / 960.0, -0.6, 0.6))
        bus.add(norm(x), lm["emerge_s"][i], -27.0 + j * 0.3, send=0.7, p=p)

    # SETTLE — chime, open fifth D6 + A6, gentler than the hit bell
    m = int((DUR - SETTLE) * SR)
    chime = fm_bell(1174.66, m, ratio=2.0, index=1.0, index_tau=0.12, tau=0.95, attack=0.003)
    chime += 0.55 * fm_bell(1760.0, m, ratio=2.0, index=0.8, index_tau=0.1, tau=0.8, attack=0.003)
    bus.add(norm(chime), SETTLE, -22.0, send=0.7)

    # SWEEP — sparkle grains + high air, travelling L -> R with the light
    start, length = SWEEP - 0.12, 0.97
    tones = [1760.0, 2217.46, 2637.02, 2959.96, 3520.0]
    grains = 30
    u = np.sort(rng.beta(2.2, 2.2, grains))
    for j in range(grains):
        m = int(0.14 * SR)
        f = tones[rng.integers(len(tones))]
        g = np.sin(2 * np.pi * f * secs(m) + rng.uniform(0, 6.28)) * env_ar(m, 0.002, 0.045)
        bus.add(g, start + u[j] * length, -33.0 + rng.uniform(-3, 2), send=0.8, p=-0.55 + 1.1 * u[j])
    k = int(length * SR)
    pp = secs(k) / length
    sh = svf(noise(k), 5200.0 + 3800.0 * pp, 1.6, "bp") * np.sin(np.pi * pp) ** 2
    bus.add(norm(sh), start, -33.0, send=0.5, p=-0.5 + pp)

    # EXHALE — downward air
    k = int(0.75 * SR)
    pp = secs(k) / 0.75
    fc = 2600.0 * (240.0 / 2600.0) ** pp
    env = np.minimum(pp / 0.18, 1.0) ** 1.5 * np.exp(-np.maximum(pp - 0.18, 0) / 0.32)
    ex = np.stack([svf(noise(k), fc, 0.8), svf(noise(k), fc, 0.8)]) * env
    bus.add(norm(ex), EXIT, -21.0, send=0.3)

    wet = reverb(bus.send)
    sos = signal.butter(2, [190.0, 9500.0], "bandpass", fs=SR, output="sos")
    wet = signal.sosfiltfilt(sos, wet, axis=1)
    return bus.dry, wet


# ── master ───────────────────────────────────────────────────────────────────
def limiter(x, ceiling, lookahead=0.002, release=0.08):
    peak = np.max(np.abs(x), axis=0)
    need = np.minimum(1.0, ceiling / np.maximum(peak, 1e-12))
    w = int(lookahead * SR)
    # moving minimum over the lookahead window (gain drops before the peak arrives)
    padded = np.concatenate([need, np.ones(w)])
    gmin = np.min(np.lib.stride_tricks.sliding_window_view(padded, w + 1), axis=1)
    a = np.exp(-1.0 / (release * SR))
    g = np.empty_like(gmin)
    s = 1.0
    for i in range(len(gmin)):
        s = gmin[i] if gmin[i] < s else a * s + (1 - a) * gmin[i]
        g[i] = s
    return x * g


def measure(path):
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True,
        text=True,
    )
    txt = r.stderr
    summ = txt[txt.rfind("Summary:") :]
    lufs = float(summ.split("I:")[1].split("LUFS")[0])
    tp = float(summ.split("Peak:")[1].split("dBFS")[0])
    return lufs, tp


def main():
    dry, wet = compose()
    rms = lambda v: np.sqrt(np.mean(v**2))
    print(f"dry rms {20*np.log10(rms(dry)):.1f} dB · wet rms {20*np.log10(rms(wet)):.1f} dB")
    mix = dry + db(-3.0) * wet

    # master: rumble HP, gentle glue saturation, de-click edges, tail fade to silence
    sos = signal.butter(2, 28.0, "hp", fs=SR, output="sos")
    mix = signal.sosfiltfilt(sos, mix, axis=1)
    mix = norm(mix) * 0.9
    mix = np.tanh(1.15 * mix) / np.tanh(1.15)
    mix = fade(mix, fin=0.003)
    tail0 = int(3.45 * SR)
    k = N - tail0
    mix[:, tail0:] *= 0.5 + 0.5 * np.cos(np.pi * np.arange(k) / k)

    os.makedirs(os.path.dirname(OUT_WAV), exist_ok=True)
    tmp = OUT_WAV + ".tmp.wav"

    # loudness pass: measure, gain to target, limit to the true-peak ceiling, verify
    gain = 1.0
    for _ in range(3):
        y = limiter(mix * gain, db(CEILING_DBTP - 0.4))
        wavfile.write(tmp, SR, y.T.astype(np.float32))
        lufs, tp = measure(tmp)
        print(f"pass: gain {20*np.log10(gain):+.2f} dB -> {lufs:.2f} LUFS, TP {tp:.2f} dBFS")
        if abs(lufs - TARGET_LUFS) < 0.3:
            break
        gain *= db(TARGET_LUFS - lufs)

    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", tmp, "-c:a", "pcm_s24le", OUT_WAV],
        check=True,
    )
    os.remove(tmp)
    lufs, tp = measure(OUT_WAV)
    print(json.dumps({"out": os.path.relpath(OUT_WAV, PROJECT), "lufs": lufs, "true_peak_dbfs": tp, "seconds": DUR}))


if __name__ == "__main__":
    sys.exit(main())
