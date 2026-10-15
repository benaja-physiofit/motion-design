"""Build a count-up SFX stem: soft clicks at each step the on-screen number passes
(GSAP expo.out over COUNT_DUR, the same ease the counter uses), then a ping where the % lands."""
import sys, subprocess, numpy as np, soundfile as sf
sfx_dir, target, step, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
SR, COUNT_DUR, LAND = 48000, 1.2, 1.05  # LAND: % suffix pop, seconds after count start

def load(name):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{sfx_dir}/{name}.mp3", "-ac", "1",
                          "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)

click, ping = load("click-soft"), load("ping")
CLICK_ONSET, PING_ONSET = 0.04, 0.32
stem = np.zeros(int(2.4 * SR), dtype=np.float32)

def place(sample, at, gain):
    i = max(0, int(round(at * SR)))
    n = min(len(sample), len(stem) - i)
    stem[i:i + n] += sample[:n] * gain

# expo.out: v = target * (1 - 2^(-10 p)); invert for each displayed step (Math.round -> v >= k - 0.5)
values = list(range(step, target, step)) + [target]
for idx, k in enumerate(values):
    p = -np.log2(1 - (k - 0.5) / target) / 10
    when = p * COUNT_DUR
    gain = 0.55 + 0.45 * idx / (len(values) - 1)
    place(click, when - CLICK_ONSET, gain)
place(ping, LAND - PING_ONSET, 1.4)
peak = np.max(np.abs(stem))
stem = stem / peak * 0.9
sf.write(out, np.stack([stem, stem], axis=1), SR, subtype="PCM_16")
print(out, len(values), "ticks", f"last tick at {when:.2f}s")
