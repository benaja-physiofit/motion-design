"""Physiofit sonic logo — "Blende" (iris). Calm, premium sound design: round tones, slow
blooms, no hard transients, no saturation. Synthesized and composed frame-accurately to the
intro's beats.

Deterministic: same code + seed -> bit-identical WAV. Every cue time below mirrors the
GSAP timeline in compositions/lockup.html.

    0.10–0.76  close   a soft, dark breath that follows the iris + a gentle swell grown from
                       the bloom chord's own reverb, flowing through the lock (no cut, no riser)
    0.72       lock    a round felt-mallet D4 and a slow-blooming Dmaj9 pad, with a barely-felt
                       D2 underneath
    0.80       air     two soft glass tones (A5 · E6) high above, very quiet
    0.90       foot    one soft high note (F#5) as the foot steps in
    0.98–1.48  word    a whisper of air with the wordmark wipe
    2.10–2.50  out     everything settles into silence with the picture

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
DUR = 2.5
N = int(SR * DUR)
SEED = 20261007

# beats (s) — keep in sync with compositions/lockup.html
IRIS_START, LOCK = 0.10, 0.72
FOOT = 0.90
WIPE_START, WIPE_LEN = 0.98, 0.50
EXIT = 2.20

# a calm sting sits a little below the programme it introduces
TARGET_LUFS = -16.0
CEILING_DBTP = -1.5

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


def noise(n):
    return rng.standard_normal(n)


def power4_inout(u):
    u = np.clip(u, 0.0, 1.0)
    return np.where(u < 0.5, 8 * u**4, 1 - 8 * (1 - u) ** 4)


def power4_inout_rate(u):
    """d/du of GSAP's power4.inOut — the iris' speed, peaking (4.0) at u = 0.5."""
    u = np.clip(u, 0.0, 1.0)
    return np.where(u < 0.5, 32 * u**3, 32 * (1 - u) ** 3)


# ── instruments ──────────────────────────────────────────────────────────────
# Everything is built from sines with a few soft harmonics; attacks are 20 ms at the very
# sharpest, most are 40–150 ms, so nothing "hits" — it blooms.

PAD = [  # Dmaj9, warm open voicing: D3 A3 F#4 C#5 E5
    (146.83, 1.0),
    (220.00, 0.75),
    (369.99, 0.55),
    (554.37, 0.33),
    (659.26, 0.28),
]


def soft_pad(n, attack=0.14, tau=1.5, cutoff=2400.0):
    """Wide, round pad: ±4 cent voice pairs (one leaning left, one right), steep harmonic roll-off."""
    tt = secs(n)
    L = np.zeros(n)
    R = np.zeros(n)
    for f, a in PAD:
        for cents, wl, wr in ((-4.0, 0.85, 0.4), (4.0, 0.4, 0.85)):
            fd = f * 2.0 ** (cents / 1200.0)
            v = np.zeros(n)
            for k in range(1, 7):
                v += np.sin(2 * np.pi * k * fd * tt + rng.uniform(0, 2 * np.pi)) / k**2.6
            L += v * a * wl
            R += v * a * wr
    env = env_ar(n, attack, tau)
    return np.stack([svf(L, cutoff, 0.6), svf(R, cutoff, 0.6)]) * env


def mallet(f, n, tau=0.7, attack=0.005, bright=0.22):
    """A felt mallet on a soft bar: fundamental plus quickly-fading 2nd/3rd partials."""
    tt = secs(n)
    x = np.sin(2 * np.pi * f * tt)
    x += bright * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt / 0.09)
    x += 0.35 * bright * np.sin(2 * np.pi * 3 * f * tt) * np.exp(-tt / 0.05)
    return svf(x * env_ar(n, attack, tau), 2200.0, 0.6)


def glass(f, n, tau=0.9, attack=0.012, spread=3.0):
    """A pure, slowly-beating sine pair — glass without the FM edge."""
    tt = secs(n)
    x = np.zeros(n)
    for c in (-spread, spread):
        x += np.sin(2 * np.pi * f * 2.0 ** (c / 1200.0) * tt + rng.uniform(0, 2 * np.pi))
    return 0.5 * x * env_ar(n, attack, tau)


def make_ir(length=3.0, rt60=2.6, predelay=0.03):
    """A dark, long room: the highs die quickly so the tail is air, not fizz."""
    n = int(length * SR)
    tt = secs(n)
    decay = np.exp(-6.9 * tt / rt60)
    x = noise(n) * decay
    x = svf(x, 6000.0 * np.exp(-tt / 0.5) + 1200.0, 0.6)
    er = np.zeros(n)
    for d, g in ((0.013, 0.32), (0.023, 0.25), (0.037, 0.2), (0.053, 0.15), (0.071, 0.11)):
        er[int((d + rng.uniform(-0.002, 0.002)) * SR)] = g * rng.choice([-1, 1])
    x = x / np.sqrt(np.sum(x**2)) + er * 0.5
    return np.concatenate([np.zeros(int(predelay * SR)), x])[:n]


IR = make_ir()


def allpass_chain(x, delays=(241, 389, 557, 113), g=0.55):
    """Schroeder all-passes: flat magnitude, scrambled phase — decorrelates without changing level."""
    for d in delays:
        b = np.zeros(d + 1)
        a = np.zeros(d + 1)
        b[0], b[d] = -g, 1.0
        a[0], a[d] = 1.0, -g
        x = signal.lfilter(b, a, x)
    return x


def reverb(x):
    """One tail, decorrelated per side by all-passes: wide, yet every pitch has the same
    magnitude left and right (two independent noise IRs would not guarantee that)."""
    mid = 0.5 * (x[0] + x[1])
    w = signal.fftconvolve(mid, IR)[: x.shape[1]]
    return np.stack([allpass_chain(w, (173, 449, 311, 97)), allpass_chain(w, (241, 389, 557, 113))])


# ── score ────────────────────────────────────────────────────────────────────
def compose():
    bus = Bus()
    close = LOCK - IRIS_START

    # CLOSE — a soft, dark breath: smooth rise with the iris, easing into the lock
    k = int((close + 0.12) * SR)
    u = np.clip(secs(k) / close, 0.0, 1.0)
    shape = power4_inout(np.clip(secs(k) / (close + 0.04), 0, 1))  # follows the visible opening
    env = np.sin(np.pi * 0.5 * shape) ** 2 * np.exp(-np.maximum(secs(k) - close, 0) / 0.05)
    fc = 380.0 + 900.0 * u
    breath = np.stack([svf(noise(k), fc, 0.6), svf(noise(k), fc, 0.6)]) * env
    bus.add(fade(norm(breath), 0.05, 0.04), IRIS_START, -27.0, send=0.25)

    # CLOSE — a gentle swell grown from the bloom chord's own reverb, overlapping the bloom
    m = int(0.5 * SR)
    seed = soft_pad(m, attack=0.01, tau=0.25)
    tail = reverb(np.pad(seed, ((0, 0), (0, int(2.2 * SR)))))
    energy = np.convolve(np.sum(tail**2, axis=0), np.ones(int(0.01 * SR)), "same")
    rev = tail[:, int(np.argmax(energy)) :][:, ::-1]
    sw = int(0.6 * SR)
    swell = fade(rev[:, -sw:], fin=0.42, fout=0.12)
    bus.add(norm(swell), LOCK + 0.08 - 0.6, -17.5)

    # LOCK — a round felt mallet (D4, octave above at a whisper) marks the moment, softly
    n = int((DUR - LOCK) * SR)
    note = mallet(293.66, n, tau=0.75, attack=0.02) + 0.18 * mallet(587.33, n, tau=0.5, attack=0.022, bright=0.1)
    bus.add(norm(note), LOCK, -17.5, send=0.4, p=-0.05)

    # BLOOM — slow Dmaj9 pad, and a barely-felt D2 underneath for warmth (no punch)
    bus.add(norm(soft_pad(n)), LOCK, -14.5, send=0.42)
    sub = np.sin(2 * np.pi * 73.42 * secs(n)) * env_ar(n, 0.08, 0.55)
    bus.add(norm(sub), LOCK, -19.0)

    # AIR — two soft glass tones far above
    m = int((DUR - 0.8) * SR)
    air = glass(880.0, m, tau=0.95) + 0.55 * glass(1318.51, m, tau=0.8, attack=0.02)
    bus.add(norm(air), 0.80, -28.0, send=0.6, p=0.1)

    # FOOT — one soft high note instead of a tap
    m = int((DUR - FOOT) * SR)
    bus.add(norm(mallet(739.99, m, tau=0.45, attack=0.015, bright=0.12)), FOOT, -26.0, send=0.5, p=-0.2)

    # WORD — a whisper of air with the wipe
    k = int(WIPE_LEN * SR)
    pp = secs(k) / WIPE_LEN
    whisper = svf(noise(k), 3000.0 + 2000.0 * pp, 0.9, "bp") * np.sin(np.pi * pp) ** 2
    whisper = svf(whisper, 6500.0, 0.7)
    bus.add(norm(whisper), WIPE_START, -38.0, send=0.4, p=-0.25 + 0.6 * pp)

    wet = reverb(bus.send)
    sos = signal.butter(2, [220.0, 7000.0], "bandpass", fs=SR, output="sos")
    wet = signal.sosfiltfilt(sos, wet, axis=1)
    return bus.dry, wet


# ── master ───────────────────────────────────────────────────────────────────
def limiter(x, ceiling, lookahead=0.002, release=0.08):
    peak = np.max(np.abs(x), axis=0)
    need = np.minimum(1.0, ceiling / np.maximum(peak, 1e-12))
    w = int(lookahead * SR)
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
    mix = dry + db(-5.0) * wet

    # master: rumble HP, a soft top so nothing glints harshly, no saturation, tails fade out
    sos = signal.butter(2, 30.0, "hp", fs=SR, output="sos")
    mix = signal.sosfiltfilt(sos, mix, axis=1)
    sos = signal.butter(1, 9000.0, "lp", fs=SR, output="sos")
    mix = signal.sosfiltfilt(sos, mix, axis=1)
    mix = norm(mix) * 0.9
    mix = fade(mix, fin=0.004)
    tail0 = int((EXIT - 0.1) * SR)
    k = N - tail0
    mix[:, tail0:] *= 0.5 + 0.5 * np.cos(np.pi * np.arange(k) / k)

    os.makedirs(os.path.dirname(OUT_WAV), exist_ok=True)
    tmp = OUT_WAV + ".tmp.wav"
    gain = 1.0
    for _ in range(4):
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
