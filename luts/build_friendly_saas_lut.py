#!/usr/bin/env python3
"""Build the "Friendly SaaS" 3D LUT (.cube) for the Patientenaufnahme footage.

Input : Rec.709 / BT.1886 SDR (iPhone HEVC, *not* Apple Log)
Output: Rec.709 / BT.1886 SDR

Look: bright, airy, clean warm-white walls, soft (not crushed) blacks,
peachy natural skin, gently muted pastel colours - the clean high-key look
of Notion-style SaaS explainers.

Usage:  python3 build_friendly_saas_lut.py [out.cube] [--size 33]
"""
import argparse
import numpy as np

GAMMA = 2.4  # BT.1886 display gamma
LUMA = np.array([0.2126, 0.7152, 0.0722])  # Rec.709 coefficients

# Measured on the raw clip Patientenaufnahme-1: the grey wall reads
# RGB(176,168,163) -> warm/rosy cast. Another clip passes its own wall via --wall.
WALL_IN = np.array([175.7, 167.9, 163.0]) / 255.0
# Target wall after white balance and exposure match: near neutral, a hint of
# warm paper white, at clip 1's level so the tone curve below fits every clip.
WALL_TARGET = np.array([169.5, 167.9, 165.0]) / 255.0

# Tone curves on the colour "norm" (gamma-encoded), monotone splines.
# NEUTRAL: near-grey pixels (wall, white props) get a strong high-key lift,
#          grey wall ~0.66 -> ~0.84.
# COLOUR:  saturated pixels (skin, wood, hair) get a milder lift so the face
#          keeps its modelling and the red channel doesn't run into clipping.
TONE_X = [0.00, 0.06, 0.15, 0.30, 0.50, 0.66, 0.80, 0.92, 1.00]
TONE_NEUTRAL = [0.00, 0.055, 0.155, 0.365, 0.65, 0.835, 0.93, 0.975, 0.99]
TONE_COLOUR = [0.00, 0.055, 0.15, 0.33, 0.565, 0.725, 0.855, 0.945, 0.99]
BLACK_LIFT = 0.022  # gamma-encoded, ~6/255: soft blacks, not milky


def pchip(x, xp, yp):
    """Monotone cubic (Fritsch-Carlson) interpolation, no SciPy needed."""
    xp, yp = np.asarray(xp, float), np.asarray(yp, float)
    h = np.diff(xp)
    d = np.diff(yp) / h
    m = np.zeros_like(yp)
    m[0], m[-1] = d[0], d[-1]
    for k in range(1, len(xp) - 1):
        if d[k - 1] * d[k] > 0:
            w1, w2 = 2 * h[k] + h[k - 1], h[k] + 2 * h[k - 1]
            m[k] = (w1 + w2) / (w1 / d[k - 1] + w2 / d[k])
    x = np.clip(x, xp[0], xp[-1])
    i = np.clip(np.searchsorted(xp, x) - 1, 0, len(h) - 1)
    t = (x - xp[i]) / h[i]
    h00 = (1 + 2 * t) * (1 - t) ** 2
    h10 = t * (1 - t) ** 2
    h01 = t * t * (3 - 2 * t)
    h11 = t * t * (t - 1)
    return h00 * yp[i] + h10 * h[i] * m[i] + h01 * yp[i + 1] + h11 * h[i] * m[i + 1]


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def soft_clip(x, knee=0.94):
    """Per-channel highlight roll-off: identity below knee, asymptote at 1."""
    over = np.maximum(x - knee, 0.0)
    room = 1.0 - knee
    return np.where(x > knee, knee + room * (1 - np.exp(-over / room)), x)


def to_ycc(g):
    y = g @ LUMA
    return y, (g[..., 2] - y) / 1.8556, (g[..., 0] - y) / 1.5748


def from_ycc(y, cb, cr):
    r = y + 1.5748 * cr
    b = y + 1.8556 * cb
    g = (y - LUMA[0] * r - LUMA[2] * b) / LUMA[1]
    return np.stack([r, g, b], -1)


def hue_dist(hue, centre):
    return np.abs(((hue - centre) + 180) % 360 - 180)


def grade(rgb, wall_in=WALL_IN, match=0.0):
    """rgb: (..., 3) gamma-encoded Rec.709 in [0,1] -> graded, same encoding."""
    lin = np.clip(rgb, 0, 1) ** GAMMA

    # 1) White balance in linear light. `match` (0-1) also pulls the clip's
    #    exposure toward clip 1's wall level; 0 keeps the clip's own exposure.
    #    For clip 1 the green gain is exactly 1, so `match` has no effect there.
    gains = (WALL_TARGET ** GAMMA) / (wall_in ** GAMMA)
    gains /= gains[1] ** (1 - match)
    lin = lin * gains

    # 2) Tone curve on a hybrid norm (max + luma), applied as a ratio so hues
    #    stay put instead of skewing per channel. The curve itself blends from
    #    NEUTRAL to COLOUR with chroma; the threshold sits well above the
    #    wall's chroma so sensor noise there can't turn into luma noise.
    _, cb0, cr0 = to_ycc(lin ** (1 / GAMMA))
    colourful = smoothstep(0.035, 0.13, np.hypot(cb0, cr0))
    norm = 0.55 * lin.max(-1) + 0.45 * (lin @ LUMA)
    norm_g = np.maximum(norm, 1e-7) ** (1 / GAMMA)
    curve = (1 - colourful) * pchip(norm_g, TONE_X, TONE_NEUTRAL) + colourful * pchip(
        norm_g, TONE_X, TONE_COLOUR
    )
    lin = lin * (curve ** GAMMA / np.maximum(norm, 1e-7))[..., None]

    # Soft black: lift as an offset in gamma space (a ratio scale can't lift 0).
    g = np.clip(lin, 0, None) ** (1 / GAMMA)
    g = BLACK_LIFT + (1 - BLACK_LIFT) * g

    # 3) Colour work in a Y'CbCr-style plane (gamma-encoded).
    y, cb, cr = to_ycc(g)
    chroma = np.hypot(cb, cr)
    hue = np.degrees(np.arctan2(cr, cb)) % 360  # skin measures ~120 deg here

    skin = (1 - smoothstep(18, 42, hue_dist(hue, 120.0))) * smoothstep(0.01, 0.04, chroma)
    # Nudge skin a couple of degrees from rosy toward peach.
    rot = np.radians(2.5 * skin)
    cb, cr = cb * np.cos(rot) - cr * np.sin(rot), cb * np.sin(rot) + cr * np.cos(rot)

    # Saturation: gently muted pastel overall, skin protected, cleaner
    # neutrals in deep shadows and near-white highlights, cool accents
    # (blue band, UI blues) kept a touch livelier.
    sat = 0.9 + 0.06 * skin
    sat = sat * (1 - 0.25 * smoothstep(0.86, 1.0, y))
    sat = sat * (0.85 + 0.15 * smoothstep(0.03, 0.18, y))
    sat = sat + 0.06 * (1 - smoothstep(25, 60, hue_dist(hue, 330.0)))
    cb, cr = cb * sat, cr * sat

    # 4) Very subtle split tone: cream highlights, neutral-cool shadows.
    hi = smoothstep(0.55, 1.0, y)
    lo = 1 - smoothstep(0.0, 0.35, y)
    cb = cb - 0.002 * hi + 0.003 * lo
    cr = cr + 0.0015 * hi - 0.001 * lo

    # 5) Highlight roll-off and legal range.
    return np.clip(soft_clip(from_ycc(y, cb, cr), 0.94), 0.0, 1.0)


def write_cube(path, size, wall_in=WALL_IN, match=0.0):
    axis = np.linspace(0.0, 1.0, size)
    # .cube order: red varies fastest, then green, then blue.
    b, g, r = np.meshgrid(axis, axis, axis, indexing="ij")
    rgb = np.stack([r, g, b], -1).reshape(-1, 3)
    out = grade(rgb, wall_in, match)
    with open(path, "w") as f:
        # Minimal header (no comments, default 0-1 domain) so stricter
        # importers like CapCut accept it as well as Resolve/Premiere/FCP.
        f.write('TITLE "Friendly SaaS Explainer - Rec709"\n')
        f.write(f"LUT_3D_SIZE {size}\n")
        np.savetxt(f, out, fmt="%.6f")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out", nargs="?", default="friendly-saas-explainer.cube")
    ap.add_argument("--size", type=int, default=33)
    ap.add_argument(
        "--wall",
        type=float,
        nargs=3,
        metavar=("R", "G", "B"),
        help="8-bit RGB of the grey wall in the raw clip (default: Patientenaufnahme-1)",
    )
    ap.add_argument(
        "--match",
        type=float,
        default=0.0,
        help="0-1: how far to pull the clip's exposure toward clip 1 (default 0)",
    )
    a = ap.parse_args()
    wall = np.array(a.wall) / 255.0 if a.wall else WALL_IN
    write_cube(a.out, a.size, wall, a.match)
    print(f"wrote {a.out} ({a.size}^3)")
