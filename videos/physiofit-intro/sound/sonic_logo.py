"""Physiofit sonic logo — "Blende" (iris). Minimal premium sound design, synthesized and
composed frame-accurately to the intro's beats.

Deterministic: same code + seed -> bit-identical WAV. Every cue time below mirrors the
GSAP timeline in compositions/lockup.html.

    0.10–0.72  close   aperture air shaped by the iris' own velocity + a low tension tone
                       rising into the lock + a faint reverse swell of the bloom chord
    0.72       lock    precise aperture click + short sub thump
    0.72       bloom   glassy open chord (D5 · A5 · E6) over a quiet warm bed, long air
    0.90       foot    soft felt tap as the P's foot steps in
    0.98–1.48  word    a breath of air travelling L->R with the wordmark wipe
    2.20–2.50  out     tails fade to silence with the picture

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
def fm_bell(f, n, ratio=2.0, index=0.8, index_tau=0.1, tau=1.2, attack=0.02, spread=4.0):
    """Glassy FM tone; ratio 2 keeps it harmonic and calm, the index fades to a pure sine.
    Two voices ±spread cents apart give a slow, living beat instead of a static sine."""
    tt = secs(n)
    idx = index * np.exp(-tt / index_tau)
    out = np.zeros(n)
    for c in (-spread, spread):
        fc = f * 2.0 ** (c / 1200.0)
        mod = idx * np.sin(2 * np.pi * fc * ratio * tt)
        out += np.sin(2 * np.pi * fc * tt + mod + rng.uniform(0, 2 * np.pi))
    return 0.5 * out * env_ar(n, attack, tau)


def warm_bed(n, attack=0.06, tau=1.3):
    """A quiet, wide Dmaj9 bed (D3 A3 E4 F#4) — warmth under the glass, never a pad you notice."""
    tt = secs(n)
    L = np.zeros(n)
    R = np.zeros(n)
    for f, a in ((146.83, 1.0), (220.0, 0.7), (329.63, 0.5), (369.99, 0.45)):
        for cents, wl, wr in ((-5.0, 0.85, 0.35), (5.0, 0.35, 0.85)):
            fd = f * 2.0 ** (cents / 1200.0)
            v = np.zeros(n)
            for k in range(1, 9):
                v += np.sin(2 * np.pi * k * fd * tt + rng.uniform(0, 2 * np.pi)) / k**2.1
            L += v * a * wl
            R += v * a * wr
    env = env_ar(n, attack, tau)
    return np.stack([svf(L, 1800.0, 0.6), svf(R, 1800.0, 0.6)]) * env


def bloom_chord(n):
    """D5 · A5 · E6 — an open fifth plus ninth: bright, airy, unresolved-in-a-good-way."""
    x = fm_bell(587.33, n, index=0.9, tau=1.25, attack=0.022)
    x += 0.72 * fm_bell(880.0, n, index=0.7, tau=1.05, attack=0.028)
    x += 0.34 * fm_bell(1318.51, n, index=0.5, index_tau=0.08, tau=0.85, attack=0.034)
    return x


def make_ir(length=2.4, rt60=1.9, predelay=0.02):
    n = int(length * SR)
    tt = secs(n)
    decay = np.exp(-6.9 * tt / rt60)
    chans = []
    for _ in range(2):
        x = noise(n) * decay
        x = svf(x, 9000.0 * np.exp(-tt / 0.8) + 1500.0, 0.6)  # high end dies first
        er = np.zeros(n)
        for d, g in ((0.011, 0.5), (0.019, 0.38), (0.031, 0.3), (0.047, 0.22), (0.063, 0.16)):
            er[int((d + rng.uniform(-0.002, 0.002)) * SR)] = g * rng.choice([-1, 1])
        x = x / np.sqrt(np.sum(x**2)) + er * 0.6
        x = np.concatenate([np.zeros(int(predelay * SR)), x])[:n]
        chans.append(x)
    return np.stack(chans)


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
    w = signal.fftconvolve(mid, IR[0])[: x.shape[1]]
    # each side gets its own all-pass chain, so neither stays phase-locked to the dry signal
    return np.stack([allpass_chain(w, (173, 449, 311, 97)), allpass_chain(w, (241, 389, 557, 113))])


# ── score ────────────────────────────────────────────────────────────────────
def compose():
    bus = Bus()
    close = LOCK - IRIS_START
    k = int(close * SR)
    u = secs(k) / close
    speed = power4_inout_rate(u) / 4.0  # 0..1, the iris' own velocity curve

    # CLOSE — aperture air: brightens and swells with the iris' speed, decorrelated L/R
    fc = 240.0 + 1700.0 * speed**0.8 + 500.0 * u
    amp = speed**0.6
    air = np.stack([svf(noise(k), fc, 0.75, "bp"), svf(noise(k), fc, 0.75, "bp")]) * amp
    air = np.stack([svf(c, 7000.0, 0.7) for c in air])
    bus.add(fade(norm(air), 0.02, 0.006), IRIS_START, -19.0, send=0.12)

    # CLOSE — low tension: D-ish fundamental gliding up a fourth, growing into the lock
    f = 55.0 * (73.42 / 55.0) ** (u**1.6)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR)
    tone = np.tanh(1.6 * tone) / np.tanh(1.6) * u**2.4
    bus.add(fade(norm(tone), 0.05, 0.008), IRIS_START, -13.0)

    # CLOSE — faint reverse swell of the bloom chord, ending a hair before the lock
    m = int(0.45 * SR)
    seed = bloom_chord(m) * env_ar(m, 0.004, 0.18)
    tail = reverb(np.pad(np.stack([seed, seed]), ((0, 0), (0, int(2.0 * SR)))))
    energy = np.convolve(np.sum(tail**2, axis=0), np.ones(int(0.01 * SR)), "same")
    rev = tail[:, int(np.argmax(energy)) :][:, ::-1]
    sw = int(0.42 * SR)
    swell = fade(rev[:, -sw:], fin=0.3, fout=0.004)
    bus.add(norm(swell), LOCK - 0.004 - 0.42, -20.0)

    # LOCK — aperture click: a 4 ms filtered tick with a tiny metallic ring
    m = int(0.08 * SR)
    tick = svf(noise(m), 3600.0, 1.2, "bp") * env_ar(m, 0.0004, 0.0018)
    ring = np.sin(2 * np.pi * 2650.0 * secs(m)) * env_ar(m, 0.0005, 0.022)
    bus.add(norm(norm(tick) + 0.45 * ring), LOCK, -15.0, send=0.18)

    # LOCK — short sub thump
    m = int(0.9 * SR)
    tt = secs(m)
    ff = 44.0 + 34.0 * np.exp(-tt / 0.05)
    thump = np.sin(2 * np.pi * np.cumsum(ff) / SR) * env_ar(m, 0.0015, 0.22)
    thump = svf(np.tanh(1.7 * thump) / np.tanh(1.7), 260.0, 0.7)
    bus.add(norm(thump), LOCK, -7.5)

    # BLOOM — glassy open chord over a quiet warm bed
    m = int((DUR - LOCK) * SR)
    bus.add(norm(bloom_chord(m)), LOCK, -11.0, send=0.38)
    bus.add(norm(warm_bed(m)), LOCK, -15.0, send=0.2)

    # FOOT — soft felt tap
    m = int(0.25 * SR)
    tt = secs(m)
    body = np.sin(2 * np.pi * np.cumsum(115.0 + 85.0 * np.exp(-tt / 0.018)) / SR) * env_ar(m, 0.002, 0.04)
    felt = svf(noise(m), 1400.0, 0.9, "bp") * env_ar(m, 0.0008, 0.007)
    bus.add(norm(norm(body) + 0.3 * norm(felt)), FOOT, -23.0, send=0.25, p=-0.2)

    # WORD — a breath of air travelling with the wipe
    k = int(WIPE_LEN * SR)
    pp = secs(k) / WIPE_LEN
    breath = svf(noise(k), 2400.0 + 3400.0 * pp, 1.3, "bp") * np.sin(np.pi * np.clip(pp * 1.4, 0, 1)) ** 2
    bus.add(norm(breath), WIPE_START, -31.0, send=0.4, p=-0.25 + 0.75 * pp)

    wet = reverb(bus.send)
    sos = signal.butter(2, [190.0, 9500.0], "bandpass", fs=SR, output="sos")
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
    mix = dry + db(-6.0) * wet

    # master: rumble HP, gentle glue, de-click edges, tails fade to silence with the picture
    sos = signal.butter(2, 28.0, "hp", fs=SR, output="sos")
    mix = signal.sosfiltfilt(sos, mix, axis=1)
    mix = norm(mix) * 0.9
    mix = np.tanh(1.1 * mix) / np.tanh(1.1)
    mix = fade(mix, fin=0.004)
    tail0 = int((EXIT - 0.05) * SR)
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
